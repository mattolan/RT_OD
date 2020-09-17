![Delivery](https://github.com/mattolan/RT_OD/blob/master/Documentation/Images-GitHub/Delivery.jpg?raw=true)
![Nigth](https://github.com/mattolan/RT_OD/blob/master/Documentation/Images-GitHub/Night%202.jpg?raw=true)
![Night2](https://github.com/mattolan/RT_OD/blob/master/Documentation/Images-GitHub/Night.jpg?raw=true)

This project is an object detection and alerting program.

It accepts an RTSP feed from a security camera and enhances the camera feed by detection people inside the feed. If a person is detected the application can send a text message to a defined phone number with the detection image attached.  For example if you are monitoring the RTSP feed of a camera by a an entrance door you can get an alert sent to a cell phone (or multiple cell phones) when a person walks up to the door.

The program supports defining a detection box over the RTSP feed so that only people with the defined area trigger a detection. For example if the camera covers the street and a box is defined over the front door step it will only alert once a person is on the front door step.

It also supports setting a time period where alerts can be send. For example at night only.

This program will run on Windows, Linux, Nvidia Jetson Nano or Raspberry Pi 4. 

Alerting depends on having the following 3rd party accounts connected via API Keys
- Twilio (Pay as you go Account)
- DropBox (Free account or Paid)
- Email

Installation

This document will walk you through setting up this project and configuring the components required
The core operations of this program "Object Recognition" is derived from following the Blog Lessons of Adrian Rosebrock.  

Adrian, his blog, Lessons and related information can be located at https://www.pyimagesearch.com/ Adrian's site is a wealth of information and educational
materials for anyone interested in learning more about Machine learning based Object Recognition.

This Object detection software requires an RTSP camera feed in order to function. Low quality camera feeds work best as they require the lease amount of CPU time

Components and Requirements

1. Real Time Object Detection - Core Module RT_OD.py
	This is the core of this program where all the magic happens
2. Email Messaging
	This module handles the sending of email alerts if configured
	An Email account is required that supports basic authentication. basic authentication isn't great and is being phased out by many providers
	you milage may vary with this feature.  for example with gmail https://ugtechmag.com/enable-basic-authentication-gmail-account/ even once enabled 
	I find gmail resets this value to off stopping the use of email from this application after a few days. I prefer MMS messaging personally
3. SMS Messaging
	This module handles the sending of SMS (Text Messages) messages via Twilio if configure. 
	This function reaquires a Paid messaging subscription from Twilio https://www.twilio.com/messaging
	You must generate an API key https://www.twilio.com/docs/iam/keys/api-key-resource and https://www.twilio.com/console/project/api-keys
	You must also register a phone number with Twilio to be used to send messages from
4. MMS Messaging
	This module handles the sending of MMS (Text Messages with attached images) messages via Twilio if configure. 
	This function requires a Paid messaging subscription from Twilio https://www.twilio.com/messaging
	This function also requires a DropBox account in order to upload, store and provide a publicly accessible URL for Twilio to grab the images from
	You must generate an API key https://www.twilio.com/docs/iam/keys/api-key-resource and https://www.twilio.com/console/project/api-keys
	You must also register a phone number with Twilio to be used to send messages from
	SMS and MMS use the same Twilio account and information. Registering once will allow both modules to function
	$20 of credit loaded onto Twilio covers my MMS notifications for approx 6-8 weeks. Approx 600 MMS Messages. However this will depend on how many notifications your
	system generates
5. DropBox
	This module is used to upload and store detection event images. It is also used to provide publicly accessible URL's for use with Twilio for sending MMS messages
	A Free DropBox account is sufficient https://www.dropbox.com/
	You must generate a dropbox API key for use with this app http://99rabbits.com/get-dropbox-access-token/

Windows Setup
	1. Download and install Anaconda
		Download Link https://www.anaconda.com/products/individual#windows
		Installation Instructions https://docs.anaconda.com/anaconda/install/windows/ Pretty much leave default and just hit next, next, finish
		Anaconda is a data science tool kit that will allow us to create a virtual envronment on windows machines to run python and linux packages. 
		It is free for personal home use

		Restart Your computer before proceeding to step 2.  

	2. Create a virtual environment in anaconda from the windows command prompt
		open the command prompt
		issue the following command - "conda create --name opencv-env python=3.7" to create a virtual python environment named opencv-env
		Confirm the prompt asking to install required compnonents for running python in the virtual envrionment
	3. Activate the environment from the command prompt with the command "activate opencv-env"
		Note all work needs to be done in the "opencv-env" virtual envronment.  Everytime you want to run or work on the project you must load this envronment
		or your project will not funtion due to missing dependencies
	4. continue and run the linux setup steps from within this virtual environment

Configuration File 
	1. Rename the file "ConfigValuesTemplay.py" to "ConfigValues.py"
	2. Open the file in your prefered editor. If you don't have an editor Notepad, Nano, or Vi will work
	3. Complete the configuration file with information from your own accounts for the following services
		DropBox
		Email 
		Twilio
		Destination Phone Number\s for alerting

Linux Setup
	1. If you are continuing from the windows install steps jump to step 2. If this is a linux install open a new terminal window
	2. Run the following list of commands one at a time to install the required components
	   OpenCV supports offloading of video processing to GPU
	   If you plan to use Nvidia GPU (Cuda) Skip installing the openCV-contrib-python this module is precompiled for CPU support
	   for Nvidia Cuda GPU support you will have to manually compile OpenCV with the correct GPU features enabled
		
		pip install setuptools
		pip install imutils
		pip install numpy
		pip install twilio
		pip install dropbox
		pip install opencv-contrib-python

	3. Download the Github repository https://github.com/mattolan/RT_OD as a ZIP file
	4. Extract the contents of the Zip file to a directory of your choosing.
	6. You are now ready to launch the software.

Launching the Object Detection Software
	1. Launch a terminal windows 
	2. If running on windows activate the virtual environment with the following command
		activate opencv-env
	3. launch the software with the following example command
		
		python RT_OD.py -v "rtsp://192.168.1.1:7447/5cc263923cc_2" -n "Front Door Camera"  -rsy 2 -rsx 125 -rey 358 -rex 638 -ac 5 -asph 22 -aspm 00 -aeph 7 -aepm 00

		The command command can be modified to suit your needs.
		You can execute the command multiple times to stream multiple RTSP feeds from different cameras

		Parameters
		-v		This is the RTSP feed from the camera to be monitored. You must aquire this from your camera or NVR system. It will be 
				Unique for each camera you wish to monitor
		-n		This is a name of your choosing that describes the camera
				
				All values starting with -r are used to define the "Region of Interest" This is the area of a video feed that you wish to monitor for people
				all four values are required and are used to draw a box across the RTSP stream representing the area being monitored
		-rsy	ROI Start Y axis pixel location
		-rsx	ROI Start X axis pixel location
		-rey	ROI End Y axis pixel location
		-rex	ROI End X axis pixel location

		-ac		This is the cool down period in minutes to wait between sending alerts. 
				For example if you set this to 5 you will only recieve an alert for a person in the camera feed every 5 minutes 
				(assuming of course that there is a person in the feed)

				All as and ae values are optional Set these values if you wish to only recieve alerts during a specified time frame. 
				This command assumes a 24 hour clock
				For example if you only want alerts from 10pm until 7am (the example command provided)
				If you want alerts all the time you can delete these parameters from the command
		-asph	Alert Start Period Hour
		-aspm	Alert Start Period Minute
		-aeph	Alert End Period Hour
		-aepm	Alert End Period Minue


Optional Linux GPU Setup (Nvidia Cuda) (Nvidia Jetson Nano Setup)
Continued in documentation text file contained in project
