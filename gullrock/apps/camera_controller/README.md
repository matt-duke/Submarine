# Camera Controller

## Overview
This application handles camera specific functionality. It controls the RaspiCam and a gstream server to send video to the APC using IP level protocols. This method is the best I've found for low latency, high quality digital video streaming, and allows for a very fine level of control.

## Redis Details
Device code is either `mpc` or `apc`.
### Keys:
`<device_code>_camera_controller`: Current app status
`cam_status`: Output of vcgencmd camera status (supported and detected)
### Publishers:
N/A
### Subscriptions:
`<device_code>_camera_controller.transition`: Request transition to given state ID
`start_camera_server`: Initialize camera server (gstream) to send video to APC
`stop_camera_server`: Stop camera stream
## Requirements
```
    logger
    hiredis
    pthread
    event
    event_pthreads
```