# Application Manager

## Overview
This application starts and monitors other apps to watch for faults and crashes. It also starts thirdparty apps such as redis-server. As the main entrypoint for submarine software, it should be run at startup and launch applications in the correct sequence.

## Redis Details
Device code is either `mpc` or `apc`.
### Keys:
`<device_code>_app_manager:` Current app status
### Publishers:
N/A
### Subscriptions:
`<device_code>_app_manager.transition`: Request transition to given state ID
## Requirements
```
    logger
    hiredis
    pthread
    event
    event_pthreads
```