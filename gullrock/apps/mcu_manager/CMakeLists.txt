cmake_minimum_required(VERSION 3.8.0)

project(mcu_manager)

include(ExternalProject)

# Compiler options
# =================================================================

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

get_filename_component(COMMON_SOURCE_DIR "../../common" ABSOLUTE)
get_filename_component(THIRDPARTY_DIR
                       "../../thirdparty"
                       ABSOLUTE)
get_filename_component(DRIVER_DIR
                       "../../drivers"
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

# libserialport
get_filename_component(SERIALPORT_DIR ${THIRDPARTY_DIR}/libserialport ABSOLUTE)
get_filename_component(SERIALPORT_BIN ${CMAKE_CURRENT_BINARY_DIR}/libserialport ABSOLUTE)
set(SERIALPORT_STATIC_LIB ${SERIALPORT_BIN}/lib/libserialport.a)
set(SERIALPORT_INCLUDES ${SERIALPORT_BIN}/include)

file(MAKE_DIRECTORY ${SERIALPORT_INCLUDES})

ExternalProject_Add(libserialport
    SOURCE_DIR ${SERIALPORT_DIR}
    PREFIX ${SERIALPORT_BIN}
    DOWNLOAD_COMMAND cd ${SERIALPORT_DIR} && git clean -dfX && ${SERIALPORT_DIR}/autogen.sh
    CONFIGURE_COMMAND ${CMAKE_COMMAND} -E env CC=${CMAKE_C_COMPILER} ${SERIALPORT_DIR}/configure --prefix=${SERIALPORT_BIN} --with-sysroot=${CMAKE_SYSROOT} --host=armv8-rpi3-linux-gnueabihf --enable-static=yes --disable-shared
    BUILD_COMMAND make
    BUILD_BYPRODUCTS ${SERIALPORT_STATIC_LIB}
)

add_library(serialport STATIC IMPORTED GLOBAL)
add_dependencies(serialport libserialport)
set_target_properties(serialport PROPERTIES IMPORTED_LOCATION ${SERIALPORT_STATIC_LIB})
set_target_properties(serialport PROPERTIES INTERFACE_INCLUDE_DIRECTORIES ${SERIALPORT_INCLUDES})

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
        ${SERIALPORT_DIR}
)

set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD 99)
target_link_libraries( ${PROJECT_NAME}
    PRIVATE 
        logger
        hiredis
        pthread
        event
        event_pthreads
        minihdlc
        serialport
)