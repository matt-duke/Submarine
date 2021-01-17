#ifndef COMMON_H
#define COMMON_H

#include <hiredis.h>
#include <stdbool.h>
#include <regex.h>

// function prototypes
int run_cmd(char *cmd, char *buffer);
int read_file(char* filename, char **buffer);
bool file_exists(char *fname);
char* concat(const char *s1, const char *s2);
void init_logging();
char* get_match(char *output, regmatch_t *pmatch);

#endif