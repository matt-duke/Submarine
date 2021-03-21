cmake_minimum_required(VERSION 3.5.0)
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

project(mcu_manager C)
include(ExternalProject)

SET(CMAKE_CXX_FLAGS  "-g")

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
option(EVENT__DISABLE_OPENSSL
    "Define if libevent should build without support for OpenSSL encryption" ON)
option(EVENT__DISABLE_MBEDTLS
    "Define if libevent should build without support for mbed TLS encryption" ON)
add_subdirectory(${THIRDPARTY_DIR}/libevent ${CMAKE_CURRENT_BINARY_DIR}/libevent)

set(SERIALPORT_DIR ${THIRDPARTY_DIR}/libserialport)
set(SERIALPORT_BIN ${CMAKE_CURRENT_BINARY_DIR}/libserialport)
set(SERIALPORT_STATIC_LIB ${SERIALPORT_BIN}/lib/libserialport.a)
set(SERIALPORT_INCLUDES ${SERIALPORT_BIN}/include)

file(MAKE_DIRECTORY ${SERIALPORT_INCLUDES})

ExternalProject_Add(
    libmodbus
    PREFIX ${SERIALPORT_BIN}
    SOURCE_DIR ${SERIALPORT_DIR}
    CONFIGURE_COMMAND ${SERIALPORT_DIR}/autogen.sh && ${SERIALPORT_DIR}/configure --srcdir=${SERIALPORT_DIR} --prefix=${SERIALPORT_BIN} --enable-static=yes --disable-shared
    BUILD_COMMAND make
    INSTALL_COMMAND make install
    BUILD_BYPRODUCTS ${MODBUS_STATIC_LIB}
)

add_library(serialport STATIC IMPORTED GLOBAL)
add_dependencies(serialport libmodbus)
set_target_properties(serialport PROPERTIES IMPORTED_LOCATION ${SERIALPORT_STATIC_LIB})
set_target_properties(serialport PROPERTIES INTERFACE_INCLUDE_DIRECTORIES ${SERIALPORT_INCLUDES})

#set (SERIAL_DIR ${THIRDPARTY_DIR}/libserialport)
#set(SERIAL_SRC 
#    ${SERIAL_DIR}/serialport.c
#    ${SERIAL_DIR}/libserialport_internal.h
#    ${SERIAL_DIR}/libserialport.h
#    ${SERIAL_DIR}/linux.c
#    ${SERIAL_DIR}/linux_termios.c
#    ${SERIAL_DIR}/linux_termios.h
#)
#add_library(libserialport STATIC ${SERIAL_SRC})

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

target_include_directories( ${PROJECT_NAME}
    PUBLIC 
        ${PROJECT_SOURCE_DIR}/include
        ${COMMON_SOURCE_DIR}/include
        ${DRIVER_DIR}/include
)

add_custom_command(
    TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_NAME} /apps/${PROJECT_NAME}
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

add_custom_command(
    TARGET ${PROJECT_NAME} 
    POST_BUILD
    COMMAND echo 'Copying to /apps' && ${CMAKE_COMMAND} -E copy ${PROJECT_NAME} /apps/${PROJECT_NAME}
)