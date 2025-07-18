# begin tests/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(ExerciseTests)
# Allow passing STUDENT_DIR via -D
set(STUDENT_DIR "" CACHE PATH "Path to student workspace")
# Compile student's main.c into a shared library (libexercise.so)
# This includes the functions; main() is compiled but not executed
add_library(exercise SHARED ${STUDENT_DIR}/src/main.c)
# Set output directory to current (for easy access in tests)
set_target_properties(exercise PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
# end tests/CMakeLists.txt
