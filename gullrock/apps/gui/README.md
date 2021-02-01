## GUI Interface

## Overview
This Python based GUI is meant to be used from a device on the water's surface, connected by ethernet tether to the ROV. It is designed to be used on the APC, which is a Raspberry Pi touchscreen tablet meant to act as a cheap, portable and replacable alternative to and laptop or tablet.

This GUi is relatively simple and has 3 tasks:
- Read and display data from a Redis database
- Send commands to the ROV using Redis PUBSUB
- Display video by connecting to the GStream server

GUI input is meant to come from a touchscreen or (preferably) an off-the-shelf USB game controller.

## Redis Details
### Keys:
`qt5_gui_status`: Current app status
### Publishers:
`set.io.m1_speed`
`set.io.m2_speed`
`set.io.cam_pitch`
`set.io.cam_yaw`
`set.io.headlight`
### Subscriptions:
`mcu_refresh`: ? Uncertain whether to use polling or notifications for GUI refresh
## Requirements
`python3-gi python3-gi-cairo gir1.2-gtk-3.0`: PyGObject support on Debian based distro
See requirements.txt for PIP packages