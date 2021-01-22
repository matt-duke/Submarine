#include <regex.h>
#include <stdlib.h>
#include <logger.h>

#include "common.h"
#include "vcgencmd.h"

#define CAMERA_REGEX "supported=([[:digit:]])[[:space:]]detected=([[:digit:]])"
#define VOLTAGE_REGEX "volt=([[:digit:].]+)V"
#define THROTTLED_REGEX "throttled=([x[:digit:]]+)"
#define TEMP_REGEX "temp=([[:digit:].]+)'C"
#define VCGENCMD "/opt/vc/bin/vcgencmd "

#define BUFFERSIZE 248

#define BIT(hex, i) ((hex >> i) & 1)

cam_status_t vcgencmd_camera_status() {
    char output[BUFFERSIZE];
    char *pattern = CAMERA_REGEX;

    cam_status_t result;
    result.supported = -1;
    result.detected = -1;
    regex_t regex;
    regmatch_t pmatch[2];

    if(run_cmd(VCGENCMD"get_camera", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 2, pmatch, 0);
    regfree(&regex);
    if (!status) {
        //result.supported = atoi(get_match(output, &pmatch[1]));
        //result.detected = atoi(get_match(output, &pmatch[2]));
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}

char* vcgencmd_version() {
    char output[BUFFERSIZE];
    char* result;
    if(run_cmd(VCGENCMD"version", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }
}

throttled_t vcgencmd_throttled() {
    char output[BUFFERSIZE];
    char *pattern = THROTTLED_REGEX;

    throttled_t result = {-1,-1,-1,-1,-1,-1,-1,-1};
    regex_t regex;
    regmatch_t pmatch[1];

    if(run_cmd(VCGENCMD"get_throttled", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 1, pmatch, 0);
    regfree(&regex);
    if (!status) {
        int hex = (int)strtol(get_match(output, &pmatch[1]), NULL, 0);
        result.under_volt = BIT(hex, 0);
        result.freq_cap = BIT(hex, 1);
        result.throttled = BIT(hex, 2);
        result.soft_temp_limit = BIT(hex, 3);
        result.under_volt_oc = BIT(hex, 16);
        result.freq_cap_oc = BIT(hex, 17);
        result.throttled_oc = BIT(hex, 18);
        result.soft_temp_limit_oc = BIT(hex, 19);
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}

float vcgencmd_measure_temp() {
    char output[BUFFERSIZE];
    char *pattern = TEMP_REGEX;

    float result =-1;
    regex_t regex;
    regmatch_t pmatch[2];

    if(run_cmd(VCGENCMD"measure_temp", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 2, pmatch, 0);
    regfree(&regex);
    if (!status) {
        result = atof(get_match(output, &pmatch[1]));
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}

float vcgencmd_measure_volts() {
    char output[BUFFERSIZE];
    char *pattern = VOLTAGE_REGEX;

    float result =-1;
    regex_t regex;
    regmatch_t pmatch[2];

    if(run_cmd(VCGENCMD"measure_volts", output, BUFFERSIZE)) {
        LOG_ERROR("Error running cmd");
        return result;
    }

    if (regcomp(&regex, pattern, REG_EXTENDED) != 0)
        LOG_ERROR("regcomp error");
    int status = regexec(&regex, output, 2, pmatch, 0);
    regfree(&regex);
    if (!status) {
        result = atof(get_match(output, &pmatch[1]));
    } else {
        LOG_ERROR("No match found: %s in %s", pattern, output);
        return result;
    }
    return result;
}