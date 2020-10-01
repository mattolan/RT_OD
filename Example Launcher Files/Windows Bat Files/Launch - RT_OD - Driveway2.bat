@Echo Off

cd\RT_OD
call activate opencv-env
python RT_OD.py -v "rtsp://192.168.1.10:7447/599e3600e4b06b8d1258c2ae_2" -n "Driveway2" -rsy 80 -rsx 2 -rey 358 -rex 638 -ac 5 -asph 20 -aspm 30 -aeph 7 -aepm 00

pause

#Driveway 2  	rtsp://192.168.1.10:7447/599e3600e4b06b8d1258c2ae_2
#Damaged 	rtsp://192.168.1.10:7447/5c074196e4b0b09f7c1639e6_2

#python RT_OD.py -v "rtsp://192.168.1.10:7447/599e3600e4b06b8d1258c2ae_2" -n "Driveway2" -rsy 80 -rsx 2 -rey 358 -rex 638 -u 1 -ac 5 -asph 22 -aspm 00 -aeph 7 -aepm 00
#python RT_OD.py -v "rtsp://192.168.1.10:7447/599e3600e4b06b8d1258c2ae_2" -n "Driveway2" -rsy 0 -rsx 2 -rey 358 -rex 638 -u 1 -ac 5 -asph 22 -aspm 00 -aeph 7 -aepm 00
#python RT_OD.py -v "rtsp://192.168.1.10:7447/5cc263bde4b0b09f7c6923cc_2" -n "Front Door" -rsy 2 -rsx 125 -rey 358 -rex 638 -u 1 -ac 5