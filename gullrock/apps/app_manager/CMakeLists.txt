cmake_minimum_required(VERSION 3.8.0)

project(app_manager C)

get_filename_component(COMMON_SOURCE_DIR
                       "${CMAKE_SOURCE_DIR}/../../common"
                       ABSOLUTE)
get_filename_component(THIRDPARTY_DIR
                       "${CMAKE_SOURCE_DIR}/../../thirdparty"
                       ABSOLUTE)
get_filename_component(DRIVER_DIR
                       "${CMAKE_SOURCE_DIR}/../../drivers"
                       ABSOLUTE)
# c-logger
add_subdirectory(${THIRDPARTY_DIR}/c-logger ${CMAKE_CURRENT_BINARY_DIR}/c-logger)
# hiredis
add_subdirectory(${THIRDPARTY_DIR}/hiredis ${CMAKE_CURRENT_BINARY_DIR}/hiredis)

#libevent
option(EVENT__DISABLE_OPENSSL
    "Define if libevent should build without support for OpenSSL encryption" ON)
option(EVENT__DISABLE_MBEDTLS
    "Define if libevent should build without support for mbed TLS encryption" ON)
add_subdirectory(${THIRDPARTY_DIR}/libevent ${CMAKE_CURRENT_BINARY_DIR}/libevent)

file(GLOB HDLC_SRC "${THIRDPARTY_DIR}/minihdlc/*.c")
add_library(minihdlc STATIC ${HDLC_SRC})
target_include_directories(minihdlc PUBLIC ${THIRDPARTY_DIR}/minihdlc)

file(GLOB SRC "${CMAKE_CURRENT_LIST_DIR}/src/*.c")
file(GLOB CMN_SRC "${COMMON_SOURCE_DIR}/src/*.c")
file(GLOB DRIVER_SRC "${DRIVER_DIR}/src/*.c")
add_executable( ${PROJECT_NAME}
    ${SRC}
    ${CMN_SRC}
    ${DRIVER_SRC}
)

target_compile_features(${PROJECT_NAME} PUBLIC c_std_99)

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
        serialport
        minihdlc
)