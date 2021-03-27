project(mpc)

cmake_minimum_required(VERSION 3.8.0)

add_subdirectory(${CMAKE_SOURCE_DIR}/apps/mcu_manager ${CMAKE_CURRENT_BINARY_DIR}/mcu_manager)
add_subdirectory(${CMAKE_SOURCE_DIR}/apps/app_manager ${CMAKE_CURRENT_BINARY_DIR}/app_manager)