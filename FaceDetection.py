# import the necessary packages
import numpy as np
import argparse
import cv2
import ConfigValues
import DropBox
import MMS
import datetime
import time as t

def FaceDetection(image):
	try:
		FaceFound = 'false'
		#Detection Models
		Prototxt = "ModelFaceRec.prototxt.txt"#ConfigValues.ReturnRDODProtoTXT()
		Model = "ModelFaceRec.caffemodel"#ConfigValues.ReturnRTODModel()
		SystemConfidence = ConfigValues.ReturnRTODSystemConfidence()

		net = cv2.dnn.readNetFromCaffe(Prototxt, Model)
		# load the input image and construct an input blob for the image
		# by resizing to a fixed 300x300 pixels and then normalizing it
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))
		# pass the blob through the network and obtain the detections and
		# predictions
		print("[INFO] computing object detections...")
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		DetectedFaces = []
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]
			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > SystemConfidence:
				# compute the (x, y)-coordinates of the bounding box for the
				# object
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
 
				#Grab ROI
				#[startY:endY, startX:endX]
				roi = image[startY:endY, startX:endX]
				DetectedFaces.append(roi)	

		for df in DetectedFaces:
			FaceFound = 'true'
			#upload to DropBox
			#Path to Temp Save Alert Images 
			Image_Path = "FaceDetection.jpeg"  
			#Save Image to Disk
			cv2.imwrite(Image_Path, df)
			URL = DropBox.UploadToDropBox(Image_Path)
			print("DropBox Image Public Share URL: " + str(URL))

			#Send MMS
			if(ConfigValues.ReturnTwilioMMSEnabled() == 'true'):
				PhoneDestination = ConfigValues.ReturnAlertPhoneDestination()
				for PD in PhoneDestination:
					MMS.Send_MMS("FaceDetection " + str(datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')) , PD, URL) 
				print("MMS Alerts Sent")
		
		return FaceFound
	except:
		print("Oops!, Face Detection Error: ", sys.exc_info()[0], "occurred.")
	
		
		# show the output image
	#cv2.imshow("Output", image)
	#cv2.waitKey(0)
	
