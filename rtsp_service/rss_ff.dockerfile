#Constructing the dockerfile to create an image with rtsp-ss and ffmpeg

#ffmpeg command to launch: ffmpeg -re -stream_loop -1 -i /cat.jpeg -c copy -f rtsp rtsp://localhost:8554/cat.jpeg

#This is working

FROM aler9/rtsp-simple-server AS rtsp
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y -q --no-install-recommends python3 \
    python3-opencv ffmpeg
COPY --from=rtsp /rtsp-simple-server /
COPY --from=rtsp /rtsp-simple-server.yml /

WORKDIR /

EXPOSE 8554

COPY retail.mp4 .
COPY run-script.sh . 
COPY streamer.py .

#You need an entrypoint or else nothing will happen

ENTRYPOINT ["sh", "run-script.sh"]



#Instructions to deploy this docker file
#Move it to the home directory
#Then build the docker file with the command docker build name_tbd .
#Then run the docker image with the appropriate flags: docker run --rm -it --network=host name_tbd
