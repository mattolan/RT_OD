@Echo Off

cd\RT_OD
call activate opencv-env
python RT_OD.py -v "rtsp://192.168.1.10:7447/5cc263bde4b0b09f7c6923cc_2" -n "Front Door"  -rsy 2 -rsx 125 -rey 358 -rex 638 -ac 5

pause

