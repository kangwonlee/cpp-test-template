# begin tests/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(TestProject CXX)

# Default student code directory
set(STUDENT_DIR /app/workspace CACHE PATH "Path to student's code directory")

# Build the main executable
add_executable(test_exec ${STUDENT_DIR}/src/main.cpp)

# Print the executable path
get_target_property(EXE_OUTPUT_DIR test_exec RUNTIME_OUTPUT_DIRECTORY)
if(NOT EXE_OUTPUT_DIR)
    set(EXE_OUTPUT_DIR ${CMAKE_BINARY_DIR})
endif()
message(STATUS "Test executable path: ${EXE_OUTPUT_DIR}/test_exec")

# end tests/CMakeLists.txt
