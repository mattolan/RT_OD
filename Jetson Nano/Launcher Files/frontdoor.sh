#! /bin/sh
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
source `which virtualenvwrapper.sh`

workon py3cv4
cd Desktop/RT_OD

python RT_OD.py -v "rtsp://192.168.1.10:7447/5cc263bde4b0b09f7c6923cc_2" -n "Front Door" -rsy 2 -rsx 125 -rey 358 -rex 638 -u 1 -ac 5

deactivate
