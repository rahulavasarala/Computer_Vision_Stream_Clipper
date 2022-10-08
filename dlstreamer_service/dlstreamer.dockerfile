
FROM dlstreamer/dlstreamer:devel

RUN bash /opt/intel/dlstreamer/samples/download_models.sh

WORKDIR /home/dlstreamer/graphic_app

ENTRYPOINT ["python3", "gst-img-filler.py", "rtsp://127.0.0.1:8554/retail.mp4", "30"]