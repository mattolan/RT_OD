#import from my python files
from SMS import Send_SMS
from MMS import Send_MMS
from Email import Send_Mail
from DropBox import UploadToDropBox
import ConfigValues

print("starting tests of required project modules for proper configuration and function")
print("")

print("")
print("SMS Test")
Send_SMS("Test SMS", ConfigValues.ReturnAlertPhoneDestination())
print("")



print("")
print("Email Test")
print("")

import cv2
image = cv2.imread("C:\Build3\RT_OD\img.jpg")
##cv2.waitKey(0) #if you uncomment this line a viewer will open showing the test image to email. You must exit the viewer with 'q' to continue
Image_Pth = "C:\Build3\RT_OD\img.jpg"
cv2.imwrite(Image_Pth, image)
Send_Mail(Image_Pth, "Test Email", "Label")

print("")
print("DropBox Test")
print("")

link = UploadToDropBox("img.jpg")
print ("File Uploaded, Viewing Link is: " + link)

print("")
print("MMS Test using the file uploaded in the dropbox test")
print("")
Send_MMS("Test MMS", ConfigValues.ReturnAlertPhoneDestination(), link)

print("")
print("Test Completed!")
