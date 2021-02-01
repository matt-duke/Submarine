# Config Manager

## Overview
This application is used to detect software validity and iniiliaze common variables from configuration files. It is heavily involved in the firmware update procedure by reading app CRC values and comparing to expected values. This feature is less critical for development and can be disabled or ignored.

## Redis Details
Device code is either `mpc` or `apc`.
### Keys:
`<device_code>_config_manager`: Current app status
### Publishers:
N/A
### Subscriptions:
`<device_code>_config_manager.transition`: Request transition to given state ID
## Requirements
```
    logger
    hiredis
    pthread
    event
    event_pthreads
```