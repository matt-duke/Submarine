#ifndef Imu_H
#define Imu_H

#include <mpu9150.h>
#include <linux_glue.h>
#include <local_defaults.h>

typedef struct ImuClass {
    int(*set_cal)(struct ImuClass *self, int mag, char *cal_file);
	int(*read)(struct ImuClass *self);
	int(*init)(struct ImuClass *self);
	mpudata_t mpudata;
    uint64_t prev_clock_time_ms;
    int sample_rate_hz;
	int i2c_bus;
	int yaw_mix_factor;
	char *mag_cal_file;
	char *accel_cal_file;
} ImuClass_t;

void ImuClassInit(ImuClass_t *imu);

#endif