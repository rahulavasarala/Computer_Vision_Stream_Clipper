from threading import Thread

import sys
import gi
import time
import cv2
import os

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib

args = sys.argv[1:]

if len(args) != 2:
    print("Usage: RTSP_URL, num_time")
    exit(1)

num_time = int(args[1])
RTSP_URL = args[0]
MODEL_PATH = "/home/dlstreamer/intel/dl_streamer/models"
FULL_MODEL_PATH = "{a}/intel/face-detection-adas-0001/FP32/face-detection-adas-0001.xml".format(a = MODEL_PATH)

Gst.init(sys.argv)

print("Pipeline will be started shortly")

time.sleep(10)

#_____________________________________________________________________________

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if cap.isOpened():
    print("RTSP stream is running successfully")
else:
    print("RTSP stream cannot be opened")

cap.release()

#_________________________________________________________________________________



main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline = Gst.parse_launch("uridecodebin uri={a} ! gvadetect model={b} device=CPU ! queue ! gvawatermark ! videoconvert ! jpegenc ! multifilesink location=./test-images/frame%d.jpeg".format(a = RTSP_URL, b = FULL_MODEL_PATH))
#Change the location of the jpeg files or something
pipeline.set_state(Gst.State.PLAYING)

try:
    for i in range(0,num_time):
        print("Running pipeline...")
        time.sleep(2)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()