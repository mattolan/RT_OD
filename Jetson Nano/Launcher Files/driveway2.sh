#! /bin/sh
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
source `which virtualenvwrapper.sh`

workon py3cv4
cd Desktop/RT_OD

python RT_OD.py -v "rtsp://192.168.1.10:7447/599e3600e4b06b8d1258c2ae_2" -n "Driveway2" -rsy 80 -rsx 2 -rey 358 -rex 638 -u 1 -ac 5 -asph 22 -aspm 00 -aeph 7 -aepm 00

deactivate
