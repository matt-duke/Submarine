#ifndef COMMON_H
#define COMMON_H

#include <hiredis.h>
#include <stdbool.h>
#include <stdint.h>
#include <regex.h>

// variables

enum t_type {
    TYPE_UINT8 = 0,
    TYPE_INT8,
    TYPE_UINT16,
    TYPE_INT16,
    TYPE_UINT32,
    TYPE_INT32,
    TYPE_BOOL,
    TYPE_FLOAT,
    TYPE_CHAR_POINTER,
    TYPE_VOID_POINTER,
    TYPE_OTHER
};

#define type(x) _Generic((x),                                                       \
    _Bool: TYPE_BOOL, \
    unsigned char: TYPE_UINT8, signed char: TYPE_INT8, \
    unsigned short int: TYPE_UINT16, short int: TYPE_INT16, \
    unsigned long int: TYPE_INT32, long int: TYPE_UINT32, \
    float: TYPE_FLOAT, \
    char*: TYPE_CHAR_POINTER, \
    void*: TYPE_VOID_POINTER, \
    default: TYPE_OTHER \
)

// function prototypes
int run_cmd(char *cmd, char *buffer, int size);
int read_file(char* filename, char **buffer);
bool file_exists(char *fname);
char* concat(const char *s1, const char *s2);
void init_logging();
char* get_match(char *output, regmatch_t *pmatch);

#endif