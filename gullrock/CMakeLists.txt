cmake_minimum_required(VERSION 3.5.0)
project(submarine C)

find_library(EVENT_LIBRARY NAMES libevent libevent-dev)

get_filename_component(APP_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/apps"
					   ABSOLUTE)
					   
add_subdirectory(${THIRDPARTY_DIR}/app_manager ${CMAKE_CURRENT_BINARY_DIR}/app_manager)