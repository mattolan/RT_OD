@Echo Off

cd\RT_OD
call activate opencv-env
python RT_OD.py -v "rtsp://192.168.1.10:7447/53a8d8b423a1a64a2d6359a7_2" -n "Driveway1"  -rsy 80 -rsx 2 -rey 358 -rex 638 -ac 5 -asph 22 -aspm 00 -aeph 7 -aepm 00

pause
q
#Driveway 1  	rtsp://192.168.1.10:7447/53a8d8b423a1a64a2d6359a7_2
