#Must be installed before running this script for the first time
	#pip install setuptools
	#pip install imutils
	#pip install numpy
	#pip install opencv-contrib-python
	#pip install twilio
	#pip install dropbox

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time as t
import cv2
from datetime import datetime, time
import datetime

#import from my python files
from SMS import Send_SMS
from MMS import Send_MMS
from Email import Send_Mail
from DropBox import UploadToDropBox
from AlertTime import is_time_between
import ConfigValues

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default="rtsp://192.168.1.10:7447/5cc263bde4b0b09f7c6923cc_2", help="path to video file or url to RTSP")
ap.add_argument("-n", "--name", default="Front Door", help="camera Name")
ap.add_argument("-rsy", "--ROISY", type=int, default=0, help="ROI Start Y")
ap.add_argument("-rsx", "--ROISX", type=int, default=2, help="ROI Start X")
ap.add_argument("-rey", "--ROIEY", type=int, default=358, help="ROI End Y")
ap.add_argument("-rex", "--ROIEX", type=int, default=638, help="ROI End X")
ap.add_argument("-u", "--use-gpu", type=bool, default=False,help="boolean indicating if CUDA GPU should be used")
ap.add_argument("-ac", "--Alert", type=int, default=5,help="Alert Cool Down Period in minutes")
ap.add_argument("-asph", "--AlertStartPeriodHour", type=int, default=0,help="Alerting Period Start Hour")
ap.add_argument("-aspm", "--AlertStartPeriodMin", type=int, default='00',help="Alerting Period Start Min")
ap.add_argument("-aeph", "--AlertEndPeriodHour", type=int, default=23,help="Alerting Period End Hour")
ap.add_argument("-aepm", "--AlertEndPeriodMin", type=int, default=59,help="Alerting Period End Min")
args = vars(ap.parse_args())

#Path to Temp Save Alert Images 
Image_Path = ".\Alert_" + args["name"] + ".jpeg"  #Use this line on Windows OS
#Image_Path = "Alert_" + args["name"] + ".jpeg"  #Use this line on Linux OS
Image_Name = "Alert_" + args["name"] + ".jpeg"
#Alert Times - Only alert between these times
StartAlerts = time(args["AlertStartPeriodHour"],args["AlertStartPeriodMin"])
EndAlerts = time(args["AlertEndPeriodHour"],args["AlertEndPeriodMin"])
#Detection Models
Prototxt = ConfigValues.ReturnRDODProtoTXT()
Model = ConfigValues.ReturnRTODModel()
SystemConfidence = ConfigValues.ReturnRTODSystemConfidence()
#ROI - Area of the image to monitor for object detections. Pixel Co-ordinates
ROIStartY = args["ROISY"] #80 when the trailer isn't home
ROIStartX = args["ROISX"]
ROIEndY = args["ROIEY"]
ROIEndX = args["ROIEX"]
#Time to Sleep between frames - Limites CPU Time Usage by artifically lowering the frame rate
FrameSleep = ConfigValues.ReturnRTODFrameSleep()
AlertSleepPeriod = args["Alert"] #minutes to sleep after sending an alert to prevent alert flooding

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
#only display this list of classes on images
ClassesToDisplay =["bicycle", "car", "cat",	"dog", "motorbike", "person", "pottedplant", "boat"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(Prototxt, Model)

# check if we are going to use GPU
if args["use_gpu"]:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream..." + args["name"])
#vs = VideoStream(src=0).start()
StreamLoaded = "False"
while StreamLoaded == "False":
	try:
		RTSP_URL=args["video"]
		vs = VideoStream(RTSP_URL).start()
		t.sleep(2.0)
		fps = FPS().start()
	
		#Set Date to prevent SMS Flood
		#import datetime
		SMSAlertDelay = datetime.datetime.now()

		# loop over the frames from the video stream
		print("[INFO] video stream loaded")
		print("[INFO] starting object detection processing")
		while True:
			t.sleep(FrameSleep)
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 800 pixels
			frame = vs.read()
			#frame = imutils.resize(frame, width=800) #defines the size of the picture

			#Grab ROI
			#[startY:endY, startX:endX]
			roi = frame[ROIStartY:ROIEndY, ROIStartX:ROIEndX]
			#frame = roi

			# grab the frame dimensions and convert it to a blob
			(h, w) = roi.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(roi, (300, 300)),
				0.007843, (300, 300), 127.5)
			# pass the blob through the network and obtain the detections and
			# predictions
			net.setInput(blob)
			detections = net.forward()

			# loop over the detections
			for i in np.arange(0, detections.shape[2]):
				# extract the confidence (i.e., probability) associated with
				# the prediction
				confidence = detections[0, 0, i, 2]
				# filter out weak detections by ensuring the `confidence` is
				# greater than the minimum confidence
				if confidence > SystemConfidence:
					# extract the index of the class label from the
					# `detections`, then compute the (x, y)-coordinates of
					# the bounding box for the object
					idx = int(detections[0, 0, i, 1])
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
				
					# draw the prediction on the frame
					label = "{}: {:.2f}%".format(CLASSES[idx],
						confidence * 100)
				
					#Only draw the detection clases I am interested in
					for o in ClassesToDisplay:
						if o in label:
							#print(label)
							cv2.rectangle(frame, (startX + ROIStartX, startY + ROIStartY), (endX  + ROIStartX, endY  + ROIStartY),
								COLORS[idx], 2)
							y = startY + ROIStartY - 15 if startY + ROIStartY - 15 > 15 else startY + ROIStartY + 15
							cv2.putText(frame, label, (startX + ROIStartX, y),
								cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
			
					#Draw a box around the area being monitor for Objects
					color = (255, 0, 0) # Blue color in BGR 
					start_point = (ROIStartX, ROIStartY)
					end_point = (ROIEndX, ROIEndY)
					thickness = 2
					frame = cv2.rectangle(frame, start_point, end_point, color, thickness)	
					y = ROIStartY - 15 if ROIStartY - 15 > 15 else ROIStartY + 15
					cv2.putText(frame, "Detection Zone", (ROIStartX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

					#alert for person detection
					#print(label)
					if("person" in label and SMSAlertDelay < datetime.datetime.now() and is_time_between(StartAlerts, EndAlerts)):
						print(label + " @ " + str(datetime.datetime.now()))

						#Test for False Alarm by checking X Lenght of the detection area against the detection
						print("")
						print("Check for False Detection")
						DetectionAreaXLength = args["ROIEX"] - args["ROISX"]
						print(DetectionAreaXLength)
						DetectionEventXLength = endX - startX
						print(DetectionEventXLength)
						DectectionPercentage = DetectionEventXLength/DetectionAreaXLength*100
						print(DectectionPercentage)
						print("End Check")
						print("")
						#End Test
				
						if(DectectionPercentage < ConfigValues.ReturnDectectionPercentage()): #The closer to 100% the detection is the more likely it's a false alert. 
							#Save Image to Disk
							cv2.imwrite(Image_Path, frame)
							#Send SMS
							if(ConfigValues.ReturnTwilioSMSEnabled() == 'true'):
								PhoneDestination = ConfigValues.ReturnAlertPhoneDestination()
								for PD in PhoneDestination:
									Send_SMS(label + " at: " + args["name"], PD)
							print("SMS Alerts Sent")
							#Send MMS
							#Upload image to dropbox and generate a public sharing URL
							URL = UploadToDropBox(Image_Name)
							print("Image Uploaded to Dropbox")
							print(URL)
							if(ConfigValues.ReturnTwilioMMSEnabled() == 'true'):
								PhoneDestination = ConfigValues.ReturnAlertPhoneDestination()
								for PD in PhoneDestination:
									Send_MMS(label + " at: " + args["name"], PD, URL) 
							print("MMS Alerts Sent")
							#Email image of the detection
							if(ConfigValues.ReturnMailEnabled() == 'true'):
								Send_Mail(Image_Path, args["name"], label)
							#Set Alert Delay Period before a new alert can be sent
							SMSAlertDelay = datetime.datetime.now() + datetime.timedelta(minutes=AlertSleepPeriod)
							print("Alerts Sleeping " + str(AlertSleepPeriod) + " minutes")
						else:
							print("")
							print("False Detection Occured Detection Percentage: " + str(DectectionPercentage))
							print("")
					else:
						if("person" in label):
							#if camera is in cool down period after a detection and the person remains in frame extend the cool down to prevent further alarms
							SMSAlertDelay = SMSAlertDelay + datetime.timedelta(seconds=0.5)
							print("Person still in frame, Extending Cool Down")

			# show the output frame
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
			# update the FPS counter
			fps.update()
	
		#stop the timer and display FPS information
		fps.stop()
		print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

		#Set StreamLoaded to True after to allow the loop to exit. Loop is only to allow the stream to be restarted if it errors
		print("Video Stream & Detection Stopped")
		StreamLoaded = "True"

	except:
		print("")
		print("Oops!, RTSP Stream Error ", sys.exc_info()[0])
		print ("Attempting to re-aquire Stream")
		print("")
		#stop the timer and display FPS information
		fps.stop()
		print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
print(args["name"] + " has exited. This window is safe to close" )

#ObjectDetection()