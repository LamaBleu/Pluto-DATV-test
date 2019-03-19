# Edit this file modify path to audio and TX (for OSD) file, change CALLSIGN

AUDIOFILE=/home/user/Musique/audio.mp3
TEXTFILE=/home/user/datv_text.txt
CALSIGN=CALLSIGN

ffmpeg -r 10 -i '/dev/video0' -i $AUDIOFILE -acodec mp2  -f mpegts -b:v 0.7M \
-vf "drawtext=textfile=$TEXTFILE:x=60:y=34:fontsize=40:shadowx=3:shadowy=3:fontcolor=red:shadowcolor=white" \
-b:a 128k -ar 44100 -ac 2 -af asetpts=N/SR/TB \
-mpegts_service_id 1 -metadata service_provider=”$CALLSIGN” -metadata service_name=$CALLSIGN \
-r 15 -ignore_unknown -pix_fmt yuv420p udp://127.0.0.1:58000

