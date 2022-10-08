import sys
import os
import subprocess
import time


def main():


    print("Running streamer.py...")

    rtsp_subp = subprocess.Popen(["ffmpeg", "-re", "-stream_loop", "-1", "-i", "/retail.mp4", "-c",
                                "copy", "-f", "rtsp", "rtsp://localhost:8554/retail.mp4"])

    try:
        for i in range(0,90):
            print("Running the Stream Loop...")
            time.sleep(2)

    except KeyboardInterrupt:

        rtsp_subp.kill()
        sys.exit(0)
    
    rtsp_subp.kill()
    sys.exit(0)

#What this program does is it launches the ffmpeg stream loop,and waits for 40 seconds before killing it

if __name__ == "__main__":
    main()