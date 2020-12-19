cmake_minimum_required(VERSION 3.5.0)
project(mcu_manager C)

find_library(EVENT_LIBRARY NAMES libevent libevent-dev)

get_filename_component(COMMON_SOURCE_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/../../common"
                       ABSOLUTE)
get_filename_component(THIRDPARTY_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/../../thirdparty"
                       ABSOLUTE)
get_filename_component(DRIVER_DIR
                       "${CMAKE_CURRENT_LIST_DIR}/../../drivers"
                       ABSOLUTE)

add_subdirectory(${THIRDPARTY_DIR}/c-logger ${CMAKE_CURRENT_BINARY_DIR}/c-logger)
add_subdirectory(${THIRDPARTY_DIR}/hiredis ${CMAKE_CURRENT_BINARY_DIR}/hiredis)

file(GLOB SRC "${CMAKE_CURRENT_LIST_DIR}/src/*.c")
file(GLOB CMN_SRC "${COMMON_SOURCE_DIR}/src/*.c")
file(GLOB DRIVER_SRC "${DRIVER_DIR}/src/*.c")
add_executable( ${PROJECT_NAME}
    ${SRC}
    ${CMN_SRC}
    ${DRIVER_SRC}
)

target_include_directories( ${PROJECT_NAME}
    PUBLIC 
        ${PROJECT_SOURCE_DIR}/include
        ${COMMON_SOURCE_DIR}/include
        ${DRIVER_DIR}/include
)

target_link_libraries( ${PROJECT_NAME}
    PRIVATE 
        logger
        hiredis
        pthread
        event
        event_pthreads
)

if (${CMAKE_BUILD_TYPE} STREQUAL Debug)
    message("Copying to /apps")
    add_custom_command(
        TARGET ${PROJECT_NAME} 
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_NAME} /apps/${PROJECT_NAME}
    )
endif()