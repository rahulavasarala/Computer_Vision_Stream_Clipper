import time
import cv2
import os

def main():
    print("Proceeding to check the rtsp stream")

    RTSP_URL = 'rtsp://localhost:8554/retail.mp4'
    #Edit This ip

    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

    time.sleep(10)

    for i in range(0, 10):
        cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

        if cap.isOpened():
            print("RTSP stream is running successfully")
        else:
            print("RTSP stream cannot be opened")

        cap.release()

        time.sleep(2)

if __name__ == "__main__":
    main()

#This script will validate whether the rtsp stream is running 10 times over the course of 20 seconds
