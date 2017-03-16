cmake_minimum_required(VERSION 3.6)
project(levenshtein_c)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES main.cpp)
add_executable(levenshtein_c ${SOURCE_FILES})