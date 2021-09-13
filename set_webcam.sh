#!/bin/bash
v4l2-ctl -d /dev/video0 -c brightness=-15
v4l2-ctl -d /dev/video0 -c zoom_absolute=3
v4l2-ctl -d /dev/video0 -c pan_absolute=32500
v4l2-ctl -d /dev/video0 -c tilt_absolute=15000
v4l2-ctl -d /dev/video0 --list-ctrls

v4l2-ctl -d /dev/video2 -c brightness=-15
v4l2-ctl -d /dev/video2 -c zoom_absolute=3
v4l2-ctl -d /dev/video2 -c pan_absolute=32500
v4l2-ctl -d /dev/video2 -c tilt_absolute=15000
v4l2-ctl -d /dev/video2 --list-ctrls
