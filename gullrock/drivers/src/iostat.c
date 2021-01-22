#include <regex.h>
#include <stdlib.h>
#include <logger.h>

#include "common.h"
#include "iostat.h"

#define IDLE_REGEX "[[:space:]]+([[:digit:].]+)[[:space:]]*$"
#define UPTIME_REGEX "^([[:digit:]:]+).+:[[:space:]]([[:digit:].]{4}),[[:space:]]([[:digit:].]{4}),[[:space:]]([[:digit:].]{4})$"
#define BUFFERSIZE 248

float iostat_cpu_idle() {
    char output[BUFFERSIZE];
    char *pattern = IDLE_REGEX;

    float result =-1;
    regex_t regex;
    regmatch_t pmatch[2];

    if(run_cmd("iostat -c", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 2, pmatch, 0);
    regfree(&regex);
    if (!status) {
        LOG_INFO("%s", output);
        result = atof(get_match(output, &pmatch[1]));
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}

uptime_t uptime() {
    char output[BUFFERSIZE];
    char *pattern = IDLE_REGEX;

    uptime_t result = {};
    regex_t regex;
    regmatch_t pmatch[5];

    if(run_cmd("iostat -c", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 5, pmatch, 0);
    regfree(&regex);
    if (!status) {
        LOG_INFO("%s", output);
        result.time = get_match(output, &pmatch[1]);
        result._1min = atof(get_match(output, &pmatch[2]));
        result._5min = atof(get_match(output, &pmatch[3]));
        result._15min = atof(get_match(output, &pmatch[4]));
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}