cmake_minimum_required(VERSION 3.10)
project(orgChartUnitTestGen)

# Enable coverage
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage")

# Google Test
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
link_directories(/usr/lib)

enable_testing()

# Collect all test files automatically
file(GLOB TEST_SOURCES "tests/test_*.cpp")

# Create the test runner executable
add_executable(runTests ${TEST_SOURCES})

# Link with GTest and pthread
target_link_libraries(runTests
    ${GTEST_LIBRARIES}
    gtest_main
    pthread
)

# Register the tests with CTest
add_test(NAME AllUnitTests COMMAND runTests)
