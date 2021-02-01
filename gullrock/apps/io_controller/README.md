# IO Controller

## Overview
Manages all functionality regarding the MPC or APc and its physical surroudnings or hardware status. Used mainly for gathering and updating the Redis database with sensor data, including CPU temperature and IMU sensor results.

The main loop in this app should be very fast to minimize data lag.

## Redis Details
Device code is either `mpc` or `apc`.
### Keys:
`<device_code>_io_controller`: Current app status
`accel_x`: X-wise acceleration
`accel_y`: Y-wise acceleration
`accel_z`: Z-wise acceleration (including gravity)
`<device_code>_cpu_temp`: vcgencmd reported CPU temperature
`<device_code>_volts`: vcgencmd reported core voltage
`<device_code>_cpu_idle`: CPU idle time since last startup
`<device_code>_load_avg_1min`: CPU load avg over previous 1min (total, not per core)
`<device_code>_load_avg_5min`: CPU load avg over previous 5min (total, not per core)
`<device_code>_load_avg_15min`: CPU load avg over previous 15min (total, not per core)
`<device_code>_under_volt`: vcgencmd CPU undervolt detected
`<device_code>_freq_cap`: vcgencmd CPU frequency capped
`<device_code>_throttled`: vcgencmd CPU currently throttled
`<device_code>_soft_temp_limit`: vcgencmd CPU soft temp limit reached
### Publishers:
N/A
### Subscriptions:
`<device_code>_io_controller.transition`: Request transition to given state ID
## Requirements
```
    logger
    hiredis
    pthread
    event
    event_pthreads
    mpu9150
```