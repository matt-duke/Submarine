cmake_minimum_required(VERSION 3.5.0)
project(config_controller C)

find_library(EVENT_LIBRARY NAMES libevent libevent-dev)

get_filename_component(COMMON_SOURCE_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/../../common"
                       ABSOLUTE)
get_filename_component(THIRDPARTY_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/../../thirdparty"
                       ABSOLUTE)

add_subdirectory(${THIRDPARTY_DIR}/c-logger ${CMAKE_CURRENT_BINARY_DIR}/c-logger)
add_subdirectory(${THIRDPARTY_DIR}/hiredis ${CMAKE_CURRENT_BINARY_DIR}/hiredis)
add_subdirectory(${THIRDPARTY_DIR}/cJSON ${CMAKE_CURRENT_BINARY_DIR}/cJSON)
include_directories(${THIRDPARTY_DIR}/cJSON)

file(GLOB COMMON "${COMMON_SOURCE_DIR}/src/*.c")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/*.c")
add_executable( ${PROJECT_NAME}
    ${SOURCES}
    ${COMMON}
)

target_include_directories( ${PROJECT_NAME}
    PUBLIC 
        ${PROJECT_SOURCE_DIR}/include
        ${COMMON_SOURCE_DIR}/include
)

target_link_libraries( ${PROJECT_NAME}
    PRIVATE 
        logger
        hiredis
        pthread
        event
        event_pthreads
        cjson
)

if (CMAKE_BUILD_TYPE STREQUAL Debug)
    add_custom_command(
        TARGET ${PROJECT_NAME} 
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_NAME} /apps/${PROJECT_NAME}
    )
endif()