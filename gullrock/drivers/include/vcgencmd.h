#ifndef VCGENCMD_H
#define VCGENCMD_H

enum VCGENCMD_STATUS {
    VCGENCMD_FAILED,
    VCGENCMD_PASSED
};

typedef struct cam_status {
    int supported;
    int detected;
} cam_status_t;

typedef struct throttled {
    int under_volt;
    int freq_cap;
    int throttled;
    int soft_temp_limit;
    int under_volt_oc;
    int freq_cap_oc;
    int throttled_oc;
    int soft_temp_limit_oc;
} throttled_t;

cam_status_t vcgencmd_camera_status();
throttled_t vcgencmd_throttled();
int vcgencmd_measure_temp();

#endif