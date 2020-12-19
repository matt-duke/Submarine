cmake_minimum_required(VERSION 3.5.0)
project(io_controller C)

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

file(GLOB MPU9150_SRC
    "${THIRDPARTY_DIR}/linux-mpu9150/mpu9150/*.c"
    "${THIRDPARTY_DIR}/linux-mpu9150/eMPL/*.c"
    "${THIRDPARTY_DIR}/linux-mpu9150/glue/*.c"
)

add_library(mpu9150 STATIC
            ${MPU9150_SRC}
)

target_include_directories(mpu9150
    PUBLIC
        ${THIRDPARTY_DIR}/linux-mpu9150/mpu9150
        ${THIRDPARTY_DIR}/linux-mpu9150/eMPL
        ${THIRDPARTY_DIR}/linux-mpu9150/glue
)

target_link_libraries(mpu9150
    PRIVATE 
        m
)

target_compile_options(mpu9150 PRIVATE 
                       -DEMPL_TARGET_LINUX
                       -DMPU9150
                       -DAK8975_SECONDARY
                       -fsingle-precision-constant
)

file(GLOB SRC "${CMAKE_CURRENT_LIST_DIR}/src/*.c")
file(GLOB CMN_SRC "${COMMON_SOURCE_DIR}/src/*.c")
file(GLOB DRIVER_SRC "${COMMON_SOURCE_DIR}/src/*.c")
add_executable( ${PROJECT_NAME}
    ${SRC}
    ${CMN_SRC}
    ${DRIVER_SRC}
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
        mpu9150
)

if (${CMAKE_BUILD_TYPE} STREQUAL Debug)
    message("Copying to /apps")
    add_custom_command(
        TARGET ${PROJECT_NAME} 
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_NAME} /apps/${PROJECT_NAME}
    )
endif()