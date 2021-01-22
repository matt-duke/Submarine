#ifndef IOSTAT_H
#define IOSTAT_H

typedef struct uptime_s {
    char *time;
    float _1min;
    float _5min;
    float _15min;
} uptime_t;


// FUNCTIONS
float iostat_cpu_idle();
uptime_t uptime();

#endif