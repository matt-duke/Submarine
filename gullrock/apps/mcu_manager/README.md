# MCU Manager

## Overview
The MCU manager acts as a bridge between the Rasberry Pi based MPC and the ATmega2560 based MCU. A serial connection between the two devices uses the HDLC message format to form data packets, which includes start and stop bytes plus a CRC embeded in the payload. To simplify the protocol, the MCU acts as a slave, and only responds to messages following a request for data from the MPC. 
This app needs relatively high speed to update the Redis server in near real-time.

## Redis Details
Device code is either `mpc` or `apc`.
### Keys:
`<device_code>_mcu_manager`: Current app status
`m1_speed`: Left motor speed (0-255)
`m2_speed`: Right motor speed (0-255)
`m1_curr`: Left motor current in volts
`m2_curr`: Right motor current in volts
`mcu_state`: Internal state reported by MCU firmware
`water temp`: Submarine water temperature (sensor onboard)
`total_current`: Total current draw from submarine batteries
### Publishers:
N/A
### Subscriptions:
`<device_code>_mcu_manager.transition`: Request transition to given state ID
`set.io.*`: Listens to requests to set MCU settings such as `m1_speed` or `cam_yaw`

## Requirements
```
    logger
    hiredis
    pthread
    event
    event_pthreads
    serialport
    minihdlc
```