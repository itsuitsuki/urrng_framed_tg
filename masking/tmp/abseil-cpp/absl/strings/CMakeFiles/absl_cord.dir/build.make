# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /public/software/cmake/cmake-3.22.0/bin/cmake

# The command to remove a file.
RM = /public/software/cmake/cmake-3.22.0/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /public/home/zhaoyd1/TG_pytorch/masking

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /public/home/zhaoyd1/TG_pytorch/masking/tmp

# Include any dependencies generated for this target.
include abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/compiler_depend.make

# Include the progress variables for this target.
include abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/progress.make

# Include the compile flags for this target's objects.
include abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/flags.make

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/flags.make
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o: /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord.cc
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/public/home/zhaoyd1/TG_pytorch/masking/tmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o -MF CMakeFiles/absl_cord.dir/cord.cc.o.d -o CMakeFiles/absl_cord.dir/cord.cc.o -c /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord.cc

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/absl_cord.dir/cord.cc.i"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord.cc > CMakeFiles/absl_cord.dir/cord.cc.i

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/absl_cord.dir/cord.cc.s"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord.cc -o CMakeFiles/absl_cord.dir/cord.cc.s

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/flags.make
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o: /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_analysis.cc
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/public/home/zhaoyd1/TG_pytorch/masking/tmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o -MF CMakeFiles/absl_cord.dir/cord_analysis.cc.o.d -o CMakeFiles/absl_cord.dir/cord_analysis.cc.o -c /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_analysis.cc

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/absl_cord.dir/cord_analysis.cc.i"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_analysis.cc > CMakeFiles/absl_cord.dir/cord_analysis.cc.i

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/absl_cord.dir/cord_analysis.cc.s"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_analysis.cc -o CMakeFiles/absl_cord.dir/cord_analysis.cc.s

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/flags.make
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o: /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_buffer.cc
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/public/home/zhaoyd1/TG_pytorch/masking/tmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o -MF CMakeFiles/absl_cord.dir/cord_buffer.cc.o.d -o CMakeFiles/absl_cord.dir/cord_buffer.cc.o -c /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_buffer.cc

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/absl_cord.dir/cord_buffer.cc.i"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_buffer.cc > CMakeFiles/absl_cord.dir/cord_buffer.cc.i

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/absl_cord.dir/cord_buffer.cc.s"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && /public/software/gcc/gcc-10.2.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings/cord_buffer.cc -o CMakeFiles/absl_cord.dir/cord_buffer.cc.s

# Object files for target absl_cord
absl_cord_OBJECTS = \
"CMakeFiles/absl_cord.dir/cord.cc.o" \
"CMakeFiles/absl_cord.dir/cord_analysis.cc.o" \
"CMakeFiles/absl_cord.dir/cord_buffer.cc.o"

# External object files for target absl_cord
absl_cord_EXTERNAL_OBJECTS =

abseil-cpp/absl/strings/libabsl_cord.a: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord.cc.o
abseil-cpp/absl/strings/libabsl_cord.a: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_analysis.cc.o
abseil-cpp/absl/strings/libabsl_cord.a: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/cord_buffer.cc.o
abseil-cpp/absl/strings/libabsl_cord.a: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/build.make
abseil-cpp/absl/strings/libabsl_cord.a: abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/public/home/zhaoyd1/TG_pytorch/masking/tmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX static library libabsl_cord.a"
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && $(CMAKE_COMMAND) -P CMakeFiles/absl_cord.dir/cmake_clean_target.cmake
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/absl_cord.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/build: abseil-cpp/absl/strings/libabsl_cord.a
.PHONY : abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/build

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/clean:
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings && $(CMAKE_COMMAND) -P CMakeFiles/absl_cord.dir/cmake_clean.cmake
.PHONY : abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/clean

abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/depend:
	cd /public/home/zhaoyd1/TG_pytorch/masking/tmp && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /public/home/zhaoyd1/TG_pytorch/masking /public/home/zhaoyd1/TG_pytorch/.dependencies/abseil-cpp/absl/strings /public/home/zhaoyd1/TG_pytorch/masking/tmp /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings /public/home/zhaoyd1/TG_pytorch/masking/tmp/abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : abseil-cpp/absl/strings/CMakeFiles/absl_cord.dir/depend

