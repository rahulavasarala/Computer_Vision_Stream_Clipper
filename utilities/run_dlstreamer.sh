#!/bin/bash

sudo docker run -it --privileged --net=host \
   --device /dev/dri \
   -v ~/.Xauthority:/home/dlstreamer/.Xauthority \
   -v /home/rahul/Desktop/stream_clip_app2/graphic_app:/home/dlstreamer/graphic_app \
   -v /tmp/.X11-unix \
   -e DISPLAY=$DISPLAY \
   -v /dev/bus/usb \
   --rm dlstreamer/dlstreamer:devel /bin/bash