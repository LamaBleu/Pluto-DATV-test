Instead of using a .ts video file as source, we replace the file source block in GNUradio by UDP source.  
Also adding TCP (or UDP) sink to get a local monitor of the video stream received by GNUradio.
  
  
  
![image](https://user-images.githubusercontent.com/26578895/54875469-4c627c00-4e00-11e9-9744-75ef4999eb1e.png)
  
  
  

Webcam : Transmit DVB-S video+audio stream from ADALM-Pluto using ffmpgeg and GNUradio
======================================================================================



Make sure your can access your webcam, test it first : ffplay /dev/video0  
  
Start TS streaming using ffmpeg, in this example adding the local webcam /dev/video0, and mp3 file as audio.  
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



Mobile phone camera : Transmit video stream to ADALM-Pluto using ffmpgeg and GNUradio
=======================================================================================

Applying same recipe, and using [same GRC](https://github.com/LamaBleu/Pluto-DATV-test/blob/master/scripts/gnuradio-webcam/dvbs_tx_udp_monitor.grc) script.  
You have to install (Android...) application on your phone to stream camera over the (wifi) network.  
ffmpeg will connect to the phone to get the video/MJPEG stream, then forward it to GNUradio as TS stream after processing.  
GNUradio will convert TS stream to IQ stream, then send it to Pluto.  

### Android apps to stream your camera over the network  

I tested few Android apps to stream the mobile camera to network.
So far I had success with all these apps after some tuning.
It's important to start first at low resolution (352x288, 640x480): we don't need to stream HD or 4K !

- Ip Webcam :
Lot of features. Once started will display current IP on the screen, useful.  
Connecting to the homepage you can toggle frontal/back camera, change resolution and camera orientation on the fly. Can display current time OSD.  
Main homepage is at : http://<mobile_ip:8080>  
Video stream is available at : http://<mobile_ip:8080>/video  
Audio stream : http://<mobile_ip>:8080/audio.wav  
  
- BL IP-Camera free  
Another nice app,easy to use  
Link to video stream : http://<mobile_ip:8080>/video  
  
- Camera streamer  
Another one.  
To video stream is available via your browser : http://<mobile_ip:8080>  
Tell your VLC client or ffmpeg to connect here : http://<mobile_ip:8081>    


### ffmpeg   
  
The most complex part ! The settings I give here are totally empirics, worked for me.   
First run the GRC script to have your Pluto ready to transmit.  
  
Example using BL IP-Camera (and streaming public french radio 'France Inter' as audio channel)  

    ffmpeg -thread_queue_size 512 -r 3 -i http://192.168.40.16:8080/mjpeg  -i 'http://direct.franceinter.fr/live/franceinter-midfi.mp3' \
    -b:a 64k -ac 1 -f mpegts -vf "drawtext=text=LamaBleu:x=60:y=60:fontsize=50:shadowx=2:shadowy=2:fontcolor=blue:shadowcolor=white" \
    -acodec mp2 -mpegts_service_id 1 -metadata service_provider=”TEST” -metadata service_name=TEST -r 3 -b:v 1.2M \
    -muxrate 1.5M  -pix_fmt yuv420p  udp://127.0.0.1:58000

    
Anoher example using IP Webcam application :  

    AUDIOFILE='http://192.168.40.10:8080/audio.wav'
    VIDEOFILE='http://192.168.40.10:8080/video'
    CALLSIGN=LamaBleu
    # audio is not included in this example.
    ffmpeg -r 3 -f mjpeg -flags2 +showall -i $VIDEOFILE \
    -f mpegts -b:v 1.1M -mpegts_service_id 1 -metadata service_provider=”$CALLSIGN” -metadata service_name=$CALLSIGN \
    -vf "drawtext=text=$CALLSIGN:x=30:y=70:fontsize=50:shadowx=2:shadowy=2:fontcolor=blue:shadowcolor=white, \
    drawtext=text='Mobile phone camera --> wifi --> ffmpeg --> GNUradio --> Pluto':y=h-line_h-100:x=w-mod(max(t-4.5\,0)*(w+tw)/8\,(w+tw)):fontcolor=orange:shadowcolor=black:fontsize=40:shadowx=2:shadowy=2" \
    -acodec mp2 -r 20 -muxrate 1.1M udp://127.0.0.1:58000  

So far the best result is obtained using IP Webcam.However you have to deal with resolution and fps.  
Try first at low res. I was able to get a decent reception at 1000kS and 1200kS on my sat-receiver, up to 800x600, with sound, but using low fps.  
Even if result is very good, please notice the latency is at least 5 seconds and will increase with time.  
Do not hesitate to submit better settings and correct my mistakes.  






