# begin tests/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(TestProject C)

# Default student code directory (can be overridden with -DSTUDENT_DIR)
set(STUDENT_DIR /app/workspace CACHE PATH "Path to student's code directory")

# Build the shared library from student's code
add_library(my_lib SHARED ${STUDENT_DIR}/src/exercise.c)
target_include_directories(my_lib PUBLIC ${STUDENT_DIR}/include)

# Build the test executable
add_executable(my_tests test_dynamic.c)
target_link_libraries(my_tests my_lib)
target_include_directories(my_tests PRIVATE ${STUDENT_DIR}/include)

# end tests/CMakeLists.txt
