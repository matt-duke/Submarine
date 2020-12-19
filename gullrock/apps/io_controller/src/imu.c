#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

#include "imu.h"

static uint64_t get_posix_clock_time();
void ImuClassInit(ImuClass_t *imu);
static int set_cal(ImuClass_t *imu, int mag, char *cal_file);
static int read(ImuClass_t *imu);
static int init(ImuClass_t *imu);

void ImuClassInit(ImuClass_t *imu) {
	imu->set_cal = &set_cal;
	imu->read = &read;
	imu->init = &init;

	imu->i2c_bus = DEFAULT_I2C_BUS;
	imu->sample_rate_hz = DEFAULT_SAMPLE_RATE_HZ;
	imu->yaw_mix_factor = DEFAULT_YAW_MIX_FACTOR;
	imu->mag_cal_file = NULL;
	imu->accel_cal_file = NULL;
	imu->prev_clock_time_ms = 0;
	memset(&imu->mpudata, 0, sizeof(mpudata_t));
}

int init(ImuClass_t *imu) {
	mpu9150_set_debug(1);
	int result = mpu9150_init(imu->i2c_bus, imu->sample_rate_hz, imu->yaw_mix_factor);
	return result;
}

int read(ImuClass_t *imu) {
	memset(&imu->mpudata, 0, sizeof(mpudata_t));
	uint64_t curr_time_ms = get_posix_clock_time();
	uint64_t sample_period_ms = 1000 / imu->sample_rate_hz;
	uint64_t timer_expiry_ms = imu->prev_clock_time_ms + sample_period_ms;
	int result = 1;
	if (curr_time_ms < timer_expiry_ms) {
		result = mpu9150_read(&imu->mpudata);
	}
	return result;
}

int set_cal(ImuClass_t *imu, int mag, char *cal_file) {
	int i;
	FILE *f;
	char buff[32];
	long val[6];
	caldata_t cal;

	if (cal_file) {
		f = fopen(cal_file, "r");
		
		if (!f) {
			perror("open(<cal-file>)");
			return -1;
		}
	}
	else {
		if (mag) {
			f = fopen("./magcal.txt", "r");
		
			if (!f) {
				printf("Default magcal.txt not found\n");
				return 0;
			}
		}
		else {
			f = fopen("./accelcal.txt", "r");
		
			if (!f) {
				printf("Default accelcal.txt not found\n");
				return 0;
			}
		}		
	}

	memset(buff, 0, sizeof(buff));
	
	for (i = 0; i < 6; i++) {
		if (!fgets(buff, 20, f)) {
			printf("Not enough lines in calibration file\n");
			break;
		}

		val[i] = atoi(buff);

		if (val[i] == 0) {
			printf("Invalid cal value: %s\n", buff);
			break;
		}
	}

	fclose(f);

	if (i != 6) 
		return -1;

	cal.offset[0] = (short)((val[0] + val[1]) / 2);
	cal.offset[1] = (short)((val[2] + val[3]) / 2);
	cal.offset[2] = (short)((val[4] + val[5]) / 2);

	cal.range[0] = (short)(val[1] - cal.offset[0]);
	cal.range[1] = (short)(val[3] - cal.offset[1]);
	cal.range[2] = (short)(val[5] - cal.offset[2]);
	
	if (mag) 
		mpu9150_set_mag_cal(&cal);
	else 
		mpu9150_set_accel_cal(&cal);

	return 0;
}

uint64_t get_posix_clock_time() {
    struct timespec ts;

    if (clock_gettime (CLOCK_MONOTONIC, &ts) == 0)
        return (uint64_t) (ts.tv_sec * 1000000 + ts.tv_nsec / 1000);
    else
        return 0;
}