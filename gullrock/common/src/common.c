#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <stdbool.h>
#include <logger.h>

#include "redis.h"
#include "baseapp.h"
#include "common.h"

#define BUFSIZE 500

// Variables
extern const char *__progname;

int run_cmd(char *cmd, char *buffer, int size) {
	FILE *fp;
	LOG_DEBUG("running command: %s", cmd);
    fp = popen(cmd, "r");
	if (fp != NULL) {
		//while (NULL != fgets(buffer, BUFSIZE, fp)) {
		//}
		size_t newLen = fread(buffer, sizeof(char), size, fp);
    	if ( ferror( fp ) != 0 ) {
        	LOG_ERROR("Error reading file");
    	} else {
        	buffer[newLen++] = '\0'; /* Just to be safe. */
   		}
    } else {
		LOG_ERROR("popen() failed.");
		pclose(fp);
		return(-1);
	}
    pclose(fp);
	return(0);
}

int read_file(char* filename, char **buffer) {
	LOG_DEBUG("Reading %s", filename);
	FILE *fp = fopen (filename, "rb");

	if (fp != NULL) {
		/* Go to the end of the file. */
		if (fseek(fp, 0L, SEEK_END) == 0) {
			/* Get the size of the file. */
			long bufsize = ftell(fp);
			if (bufsize == -1) { /* Error */ }

			/* Allocate our buffer to that size. */
			*buffer = malloc(sizeof(char) * (bufsize + 1));
			/* Go back to the start of the file. */
			if (fseek(fp, 0L, SEEK_SET) != 0) {
				LOG_ERROR("Error returning to file start");
			}

			/* Read the entire file into memory. */
			size_t newLen = fread(*buffer, sizeof(char), bufsize, fp);
			if ( ferror( fp ) != 0 ) {
				LOG_ERROR("Error reading file");
			} else {
				(*buffer)[newLen++] = '\0'; /* Just to be safe. */
			}
		}
		fclose(fp);
	}
}

bool file_exists(char *fname) {
	if(access( fname, F_OK ) != -1) {
		return true;
	} else {
		return false;
	}
}

void init_logging() {
	const char *logfile = "/tmp/debug.log";
  	remove(logfile);
	logger_initConsoleLogger(stderr);
	logger_initFileLogger(logfile, 10e6, 5);
	logger_setLevel(LogLevel_DEBUG);
}

char* get_match(char *output, regmatch_t *pmatch) {
	int size = pmatch->rm_eo - pmatch->rm_so;
	char *substr = (char*)malloc(size+1);
	if (substr == NULL) return NULL;
	substr[size] = '\0';
	strncpy(substr, &output[pmatch->rm_so], size);
	return strdup(substr);
}