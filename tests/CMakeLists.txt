# begin tests/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(TestProject C)

# Default student code directory
set(STUDENT_DIR /app/workspace CACHE PATH "Path to student's code directory")

# Build the main executable
add_executable(hello ${STUDENT_DIR}/src/main.c)
target_include_directories(hello PRIVATE ${STUDENT_DIR}/include)

# Print the executable path
get_target_property(HELLO_OUTPUT_DIR hello RUNTIME_OUTPUT_DIRECTORY)
if(NOT HELLO_OUTPUT_DIR)
    set(HELLO_OUTPUT_DIR ${CMAKE_BINARY_DIR})
endif()
message(STATUS "Hello executable path: ${HELLO_OUTPUT_DIR}/hello")

# end tests/CMakeLists.txt
