#import from my python files
from SMS import Send_SMS
from MMS import Send_MMS
from Email import Send_Mail
from DropBox import UploadToDropBox
import ConfigValues
import FaceDetection
import argparse
import cv2

link = ""

print("starting tests of required project modules for proper configuration and function")
print("")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--facedetection")
ap.add_argument("-d", "--dropbox")
ap.add_argument("-s", "--sms")
ap.add_argument("-m", "--mms")
ap.add_argument("-e", "--email")
args = vars(ap.parse_args())


if(args["sms"]):
    print("")
    print("SMS Test")
    Send_SMS("Test SMS", ConfigValues.ReturnAlertPhoneDestination())
    print("")


if(args["email"]):
    print("")
    print("Email Test")
    print("")

    image = cv2.imread("C:\RT_OD\img.jpg")
    ##cv2.waitKey(0) #if you uncomment this line a viewer will open showing the test image to email. You must exit the viewer with 'q' to continue
    Image_Pth = "C:\RT_OD\img.jpg"
    cv2.imwrite(Image_Pth, image)
    Send_Mail(Image_Pth, "Test Email", "Label")

if(args["dropbox"]):
    print("")
    print("DropBox Test")
    print("")

    link = UploadToDropBox("img.jpg")
    print ("File Uploaded, Viewing Link is: " + link)

if(args["mms"]):
    print("")
    print("This test requires the dropbox test is also run using -d")
    print("MMS Test using the file uploaded in the dropbox test")
    print("")
    Send_MMS("Test MMS", ConfigValues.ReturnAlertPhoneDestination(), link)

if(args["facedetection"]):
    print("")
    print("FaceDetection Test")
    print("")
    image = cv2.imread("C:\RT_OD\Couple.jpg")
    #next two lines are only needed to view the test image to validate that it loaded correctly from disk
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    FaceDetection.FaceDetection(image)

print("")
print("Test Completed!")
