import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
from masking import utils as masking_utils
from masking import masking_types as types
import time
# from helping_utils.logger import configure_logger, get_logger
# logger = get_logger()
class PositionalEmbedding(nn.Module):
    def __init__(self, demb):
        super(PositionalEmbedding, self).__init__()

        self.demb = demb

        inv_freq = 1 / (10000 ** (torch.arange(0.0, demb, 2.0) / demb))
        self.register_buffer('inv_freq', inv_freq)

    def forward(self, pos_seq, bsz=None):
        sinusoid_inp = torch.ger(pos_seq, self.inv_freq)
        pos_emb = torch.cat([sinusoid_inp.sin(), sinusoid_inp.cos()], dim=-1)

        if bsz is not None:
            return pos_emb[:,None,:].expand(-1, bsz, -1)
        else:
            return pos_emb[:,None,:] # r * None * d_model

class PositionwiseFF(nn.Module):
    def __init__(self, d_model, d_inner, dropout, pre_lnorm=False):
        super(PositionwiseFF, self).__init__()

        self.d_model = d_model
        self.d_inner = d_inner
        self.dropout = dropout

        self.CoreNet = nn.Sequential(
            nn.Linear(d_model, d_inner), nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(d_inner, d_model),
            nn.Dropout(dropout),
        )

        self.layer_norm = nn.LayerNorm(d_model)
        # self.layer_norm = nn.Identity()
        self.pre_lnorm = pre_lnorm

    def forward(self, inp):
        if self.pre_lnorm:
            ##### layer normalization + positionwise feed-forward
            core_out = self.CoreNet(self.layer_norm(inp))

            ##### residual connection
            output = core_out + inp
        else:
            ##### positionwise feed-forward
            core_out = self.CoreNet(inp)

            ##### residual connection + layer normalization
            output = self.layer_norm(inp + core_out)

        return output

class RelMultiHeadAttn(nn.Module):
    def __init__(self, n_head, d_model, d_head, dropout, tgt_len = None, 
                                ext_len = None, mem_len = None, pre_lnorm=False):
        super(RelMultiHeadAttn, self).__init__()

        self.n_head = n_head
        self.d_model = d_model
        self.d_head = d_head
        self.dropout = dropout

        self.qkv_net = nn.Sequential(
            nn.Linear(d_model, 3 * n_head * d_head, bias=False),
            nn.Dropout(dropout)
            )

        self.drop = nn.Dropout(dropout)
        self.dropatt = nn.Dropout(dropout)
        self.o_net = nn.Linear(n_head * d_head, d_model, bias=False)    # output net

        self.layer_norm = nn.LayerNorm(d_model)
        # self.layer_norm = nn.Identity()
        self.scale = 1 / (d_head ** 0.5)

        self.pre_lnorm = pre_lnorm

    def _parallelogram_mask(self, h, w, left=False):
        mask = torch.ones((h, w)).byte()
        m = min(h, w)
        mask[:m,:m] = torch.triu(mask[:m,:m])
        mask[-m:,-m:] = torch.tril(mask[-m:,-m:])

        if left:
            return mask
        else:
            return mask.flip(0)

    def _shift(self, x, qlen, klen, mask, left=False):
        if qlen > 1:
            zero_pad = torch.zeros((x.size(0), qlen-1, x.size(2), x.size(3)),
                                    device=x.device, dtype=x.dtype)
        else:
            zero_pad = torch.zeros(0, device=x.device, dtype=x.dtype)

        if left:
            mask = mask.flip(1)
            x_padded = torch.cat([zero_pad, x], dim=1).expand(qlen, -1, -1, -1)
        else:
            x_padded = torch.cat([x, zero_pad], dim=1).expand(qlen, -1, -1, -1)

        x = x_padded.masked_select(mask[:,:,None,None]) \
                    .view(qlen, klen, x.size(2), x.size(3))

        return x

    def _rel_shift(self, x, zero_triu=False):
        zero_pad = torch.zeros((x.size(0), 1, *x.size()[2:]),
                               device=x.device, dtype=x.dtype)
        x_padded = torch.cat([zero_pad, x], dim=1)

        x_padded = x_padded.view(x.size(1) + 1, x.size(0), *x.size()[2:])

        x = x_padded[1:].view_as(x)

        if zero_triu:
            ones = torch.ones((x.size(0), x.size(1)))
            x = x * torch.tril(ones, x.size(1) - x.size(0))[:,:,None,None]

        return x

    def forward(self, w, r, attn_mask=None, mems=None):
        raise NotImplementedError

class RelPartialLearnableMultiHeadAttn(RelMultiHeadAttn):
    def __init__(self, *args, **kwargs):
        super(RelPartialLearnableMultiHeadAttn, self).__init__(*args, **kwargs)

        self.r_net = nn.Linear(self.d_model, self.n_head * self.d_head, bias=False)

    def forward(self, w, r, r_w_bias, r_r_bias, attn_mask=None, attn_relpos=None, min_len=None, max_len=None, mems=None, terminal=False):
        qlen, rlen, bsz = w.size(0), r.size(0), w.size(1)  # L, M-m, B
        # print(qlen, rlen)
        # r: M-m * None * d_model
        if mems is not None:
            cat = torch.cat([mems, w], 0)
            if self.pre_lnorm:
                w_heads = self.qkv_net(self.layer_norm(cat))
            else:
                w_heads = self.qkv_net(cat)
            r_head_k = self.r_net(r) # M-m * None * (n_head * d_head) // M-m * B * (n_head * d_head)

            w_head_q, w_head_k, w_head_v = torch.chunk(w_heads, 3, dim=-1)
            w_head_q = w_head_q[-qlen:]
        else:
            if self.pre_lnorm:
                w_heads = self.qkv_net(self.layer_norm(w))
            else:
                # print(w.shape)
                w_heads = self.qkv_net(w)
            r_head_k = self.r_net(r)
            
            w_head_q, w_head_k, w_head_v = torch.chunk(w_heads, 3, dim=-1)
        # #test    
        # r_heads = self.qkv_net(r)
        # r_head_q, r_head_k, r_head_v = torch.chunk(r_heads, 3, dim=-1)
        # r_head_q = r_head_q.view(rlen, self.n_head, self.d_head)
        # r_head_k = r_head_k.view(rlen, self.n_head, self.d_head)
        # #---
        klen = w_head_k.size(0)

        w_head_q = w_head_q.view(qlen, bsz, self.n_head, self.d_head)           # qlen x bsz x n_head x d_head
        w_head_k = w_head_k.view(klen, bsz, self.n_head, self.d_head)           # qlen x bsz x n_head x d_head
        w_head_v = w_head_v.view(klen, bsz, self.n_head, self.d_head)           # klen x bsz x n_head x d_head

        # if composed and rlen == qlen:
        #     r_head_k = r_head_k.view(rlen, bsz, self.n_head, self.d_head)       # rlen x bsz x n_head x d_head
        # else:
        r_head_k = r_head_k.view(rlen, self.n_head, self.d_head)                # rlen x n_head x d_head
        # #test
        # r_w_bias = r_head_q[-1]
        # r_r_bias = r_head_q[-1]
        # #---
        #### compute attention score
        rw_head_q = w_head_q + r_w_bias # L * B * n_head * d_head               # qlen x bsz x n_head x d_head
        AC = torch.einsum('ibnd,jbnd->ijbn', (rw_head_q, w_head_k))             # qlen x klen x bsz x n_head

        rr_head_q = w_head_q + r_r_bias
        # if composed and rlen == qlen:
        #     BD = torch.einsum('ibnd,jbnd->ijbn', (rr_head_q, r_head_k))         # qlen x rlen x bsz x n_head
        # else:
        BD = torch.einsum('ibnd,jnd->ijbn', (rr_head_q, r_head_k))              # qlen x rlen x bsz x n_head
         
        if attn_relpos is None:
            BD = self._rel_shift(BD)
        else:
            # BD = self._rel_shift(BD)
            attn_relpos = torch.clip(attn_relpos, min_len, max_len).long()
            # print(attn_relpos.shape)
            # print(attn_relpos.min(), attn_relpos.max())
            # print(attn_relpos[0])
            attn_relpos = (max_len - attn_relpos).long()
            # print(rlen)
            # print(attn_relpos.size(0), rlen)
            # relpos_one_hot = torch.Tensor(F.one_hot(attn_relpos, num_classes=rlen)).float()               # bsz x qlen x klen x rlen
            # print(relpos_one_hot.shape)
            attn_relpos = attn_relpos.permute(1, 2, 0)

            BD = BD.gather(1, attn_relpos.unsqueeze(-1).expand(-1, -1, -1, BD.shape[-1]))
            # BD = torch.einsum('ijbn,bisj->isbn', BD, relpos_one_hot)                # qlen x klen x bsz x n_head
        
        attn_score = AC + BD
        attn_score.mul_(self.scale)

        
        #### compute attention probability
        if attn_mask is not None and attn_mask.any().item():
            if attn_mask.dim() == 2:
                attn_score = attn_score.float().masked_fill(
                    ~attn_mask[:,:,None,None], -float('inf')).type_as(attn_score)
            elif attn_mask.dim() == 3:
                attn_score = attn_score.float().masked_fill(
                    ~attn_mask[:,:,:,None], -float('inf')).type_as(attn_score)

        # [qlen x klen x bsz x n_head]
        attn_prob = F.softmax(attn_score, dim=1)
        attn_prob = self.drop(attn_prob)

        #### compute attention vector
        attn_vec = torch.einsum('ijbn,jbnd->ibnd', (attn_prob, w_head_v))

        # [qlen x bsz x n_head x d_head]
        attn_vec = attn_vec.contiguous().view(
            attn_vec.size(0), attn_vec.size(1), self.n_head * self.d_head)

        ##### linear projection
        attn_out = self.o_net(attn_vec)
        attn_out = self.dropatt(attn_out)

        if self.pre_lnorm:
            ##### residual connection
            output = w + attn_out
        else:
            ##### residual connection + layer normalization
            output = self.layer_norm(w + attn_out)
        
        return output

class TransformerGrammarLayer(nn.Module):
    def __init__(self, n_head, d_model, d_head, d_inner, dropoutf, dropouta,
                 **kwargs):
        super(TransformerGrammarLayer, self).__init__()

        self.dec_attn = RelPartialLearnableMultiHeadAttn(n_head, d_model,
                            d_head, dropouta, **kwargs)
        self.pos_ff = PositionwiseFF(d_model, d_inner, dropoutf, 
                                     pre_lnorm=kwargs.get('pre_lnorm'))
    def forward(self, dec_inp, r, r_w_bias, r_r_bias, attn_mask=None, attn_relpos=None, min_len=None, max_len=None, mems=None, terminal=False):

        output = self.dec_attn(dec_inp, r, r_w_bias, r_r_bias,
                               attn_mask=attn_mask, attn_relpos=attn_relpos,
                               min_len=min_len, max_len=max_len, mems=mems, terminal=terminal)
        output = self.pos_ff(output)

        return output

class TransformerGrammar(nn.Module):
    def __init__(self, vocab_size = 10000,
                 w_dim = 380,
                 n_head = 10,
                 d_head = 38,
                 d_inner = 900,
                 num_layers = 16,
                 dropout = 0.1,
                 dropoutatt = 0.0,
                 pad_id = 0,
                 bos_id = 1,
                 eos_id = 2,
                 opening_id = None,
                 closing_id = None,
                 pre_lnorm = False):
        super(TransformerGrammar, self).__init__()
        self.vocab_size = vocab_size
        self.d_model = w_dim
        self.n_head = n_head
        self.d_head = d_head
        self.d_inner = d_inner
        self.num_layers = num_layers


        self.dropout = nn.Dropout(dropout)

        self.emb = nn.Embedding(vocab_size, w_dim)
        self.emb_scale = w_dim ** 0.5
        self.projection = nn.Linear(w_dim, vocab_size)
        self.projection.weight = self.emb.weight

        self.num_layers = num_layers
        self.w_dim = w_dim
            
        self.layers = nn.ModuleList()

        for _ in range(num_layers):
            self.layers.append(TransformerGrammarLayer(n_head, w_dim, d_head, 
                                d_inner, dropout, dropoutatt, tgt_len = None, 
                                ext_len = None, mem_len = None,
                                pre_lnorm = pre_lnorm))
        
        self.pos_emb = PositionalEmbedding(w_dim)
        self.r_w_bias = nn.Parameter(torch.Tensor(self.n_head, self.d_head))
        self.r_r_bias = nn.Parameter(torch.Tensor(self.n_head, self.d_head))

        self.pad_id = pad_id
        self.bos_id = bos_id
        self.eos_id = eos_id
        self.opening_id = opening_id # tuple (opening_start, opening_end + 1)
        self.closing_id = closing_id # tuple (closing_start, closing_end + 1)

    def forward(self, x, length, use_mask=None, document_level=False, return_h=False, max_relative_length=None, min_relative_length=None):
        
        attn_mask = []
        attn_relpos = []
        inputs = []
        targets = []
        batch = len(x)
        if use_mask is None:
            length_i = max([len(sent) for sent in x])
            for sent in x:
                src_ = sent[:-1]
                tgt_ = sent[1:]
                src_p = src_ + [self.pad_id] * (length_i - len(src_))
                inputs.append(np.array(src_p))
                tgt_p = tgt_ + [self.pad_id] * (length_i - len(tgt_))
                targets.append(np.array(tgt_p))
            inputs = torch.LongTensor(np.array(inputs)).cuda()
            targets = torch.LongTensor(np.array(targets)).cuda()

            attn_mask = torch.tril(torch.ones((length_i, length_i), dtype = torch.uint8)).cuda().bool()
            attn_mask = attn_mask.unsqueeze(0).expand(batch, -1, -1)
            attn_relpos = None
        else:
            ranges = masking_utils.TokenTypeRanges(self.bos_id, self.pad_id, self.eos_id, self.opening_id, self.closing_id)
            maskrules = masking_utils.get_masking_rules(
                "stack_compose_double_closing_nt", 
                sequence_length=512, 
                memory_length=512, 
                transparency_prob=0.0,
                gather_into_new_memory=True, 
                transparency_depth_threshold=-1
            )

            for sent in x:
                src_ = torch.LongTensor(sent[:-1])
                tgt_ = torch.LongTensor(sent[1:])
                info_tuple = masking_utils.compute_token_types(
                    {"inputs": src_, "labels": tgt_}, ranges
                )
                chunks = maskrules.chunks_for_sequence(info_tuple['inputs'], info_tuple['inputs_ttypes'],
                                                       info_tuple['labels'], info_tuple['labels_ttypes'])
                chunks = [types.Chunk(None, *chunk) for chunk in chunks]
                
                if not document_level:
                    # only consider the first chunk
                    chunk = chunks[0]
                    src_p = chunk.inputs[:length-1]
                    inputs.append(np.array(src_p))
                    tgt_p = chunk.labels[:length-1]
                    targets.append(np.array(tgt_p))
                    mask = chunk.attn_mask[:length-1, :length-1]
                    for i in range(len(mask)):
                        mask[i, i] = 1
                    attn_mask.append(np.array(mask))
                    chunk_len = len(chunk.attn_mask[0])
                    relpos = chunk.attn_relpos[:len(mask), chunk_len:chunk_len + len(mask)]
                    attn_relpos.append(np.array(relpos))
                else:
                    pass #remain to be implemented
            inputs = torch.LongTensor(np.array(inputs)).cuda()
            targets = torch.LongTensor(np.array(targets)).cuda()
            attn_mask = torch.LongTensor(np.array(attn_mask)).cuda().bool()
            attn_relpos = torch.LongTensor(np.array(attn_relpos)).cuda()

        inputs = inputs.permute(1, 0).contiguous()
        targets = targets.permute(1, 0).contiguous()
        attn_mask = attn_mask.permute(1, 2, 0).contiguous()

        seq_len = inputs.size(0)

        
        word_emb = self.emb(inputs)
        
        if use_mask == None:
            pos_emb = self.pos_emb(torch.arange(seq_len, -1, -1.0, device=word_emb.device))
        else:
            if max_relative_length is None:
                max_relative_length = seq_len
            if min_relative_length is None:
                min_relative_length = -seq_len
            else:
                min_relative_length = min_relative_length - 1
            pos_emb = self.pos_emb(torch.arange(max_relative_length, min_relative_length, -1.0, device=word_emb.device))
        
        core_out = self.dropout(word_emb)
        pos_emb = self.dropout(pos_emb)
        hiddens = []
        hiddens.append(core_out)
        for i, layer in enumerate(self.layers):
            core_out = layer(core_out, pos_emb, self.r_w_bias, self.r_r_bias, attn_mask=attn_mask, attn_relpos=attn_relpos, min_len=min_relative_length, max_len=max_relative_length)
            hiddens.append(core_out)
            if i < len(self.layers) - 1:
                core_out = self.dropout(core_out)
        core_out = self.dropout(core_out)

        logits = self.projection(core_out) 
        crit = nn.CrossEntropyLoss(reduction='none', ignore_index=self.pad_id)
        prob = logits.view(seq_len, batch, -1)
        prob = prob.permute(0, 2, 1)
        loss = crit(prob, targets)
        loss = loss.permute(1, 0).contiguous()
        loss = loss.sum(1)

        if return_h:
            return loss, core_out
        else:
            return loss


