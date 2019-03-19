Transmit DVB-S video+audio stream from ADALM-Pluto using ffmpgeg and GNUradio
=============================================================================



Make sure your can access your webcam, test it first : ffplay /dev/video  
  
Start TS streaming using ffmpeg, in this example adding the local webcam /dev/vide0, and mp3 file as audio.  
  Also add OSD text (content of /home/user/datv_text.txt).  
 This line works well for me, but you will perhaps need to adapt/improve parameters.  

    ffmpeg -r 10 -i '/dev/video0' -i '/home/user/Musique/podcast_-_16bits.mp3' \
    -acodec mp2  -ac 1  -f mpegts -b:v 0.7M \  
    -vf "drawtext=textfile=/home/user/datv_text.txt:x=60:y=34:fontsize=40:shadowx=3:shadowy=3:fontcolor=red:shadowcolor=white" \  
    -b:a 128k -ar 44100 -ac 2 -af asetpts=N/SR/TB \  
    -mpegts_service_id 1 -metadata service_provider=”CALLSIGN” -metadata service_name=CALLSIGN \  
    -r 15 -ignore_unknown -pix_fmt yuv420p udp://127.0.0.1:58000  

You can also use ffmpeg-start.sh script to perform this task. Edit paths on this file before running it.  
Keep the task running on the terminal.  

- Start GNUradio, and run  dvbs_tx_udp_monitor.GRC script. Pluto should start transmit on 970 MHz.  
  
  
  
### Testing only : monitoring video/audio stream on local computer (GNUradio input)  
  
You don't need to apply this step except if you want to have a look at the GNUradio TS input stream   
  
   * Enabling UDP sink block : run the dvbs_tx_udp_monitor.GRC script, then "nc -lu 127.0.0.1 57000 | mplayer -" or "nc -lu 127.0.0.1 57000 | cvlc -" from a terminal console.  
   * Enabling TCP sink block : result is far better, however you have to respect following order.  
        - open Gnuradio, launch dvbs_tx_tcp_monitor.GRC script  
        - from a terminal window run webcam monitoring: "nc 127.0.0.1 57000 | cvlc -" or "nc 127.0.0.1 57000 | mplayer -"  
        - only from this moment gnuradio will start to transmit !  
        - stopping cvlc/mplayer will STOP RF transmission and you have to restart GRC script.  


### Running from shell :  
Use  'python dvbs_tx_udp_monitor.py'  
or : 'python python dvbs_tx_tcp_monitor.py' (then in second console start "nc 127.0.0.1 57000 - cvlc -" to start transmit and monitoring)  
  
  
  
  
### Bug :  
Sometimes audio discontinuity after few minutes, not always. More related to ffmpeg than gnuradio  
  
### First conclusion :  
Works well for video, but still need tweaking on ffmpeg settings and bandwidth.  
Enabling TCP sink for monitoring gives good result, however you have to follow the sequence and restart the gnuradio script every time.  













