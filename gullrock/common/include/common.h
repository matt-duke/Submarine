#ifndef COMMON_H
#define COMMON_H

#include <hiredis.h>
#include <stdbool.h>

// function prototypes
int run_cmd(char **cmd, char **output);
int read_file(char* filename, char **buffer);
bool file_exists(char *fname);
char* concat(const char *s1, const char *s2);
int redis_fn_callback (void (*f)(), char *topic);
int init_redis(redisContext **c, const char *hostname, const int port);
void init_logging();

#endif