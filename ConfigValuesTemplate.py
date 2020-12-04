#Drop Box Config
DropBoxAPIKey = "" #only required if using MMS

#Email Config
SMTPPort = 587
SMTPServer = ""
SMTPLogin = "" # paste your login 
SMTPPassword = "" # paste your password 
SMTPToAddress = ""
MailEnabled = 'false' #If set to false the other email config values can be left blank

#Twilio MMS & SMS Config
TwilioSID = ''
TwilioAuthToken = ''
TwilioSourcePhone = '+' + ''
TwilioSMSEnabled = 'false' #setting to false will still allow SMS to be uses as a failback to MMS
TwilioMMSEnabled = 'false' #if SMS and MMS are set to false the other email config values can be left blanks

#RT_OD Real Time Object Detection Config

#Detection Models
RTODPrototxt = "MobileNetSSD_deploy.prototxt.txt" #path to Caffe 'deploy' prototxt file
RTODModel = "MobileNetSSD_deploy.caffemodel" #path to Caffe pre-trained model
RTODSystemConfidence = 0.2 #minimum probability to filter weak detections

#Time to Sleep between frames - Limites CPU Time Usage by artifically lowering the frame rate
RTODFrameSleep = 0.25
#Detection Percentage - used to filter out eronious false detections that occur the closer to 100% of the detection area the more probable a
#detection is a false alert. 
DectectionPercentage = 60
#Alert On What Object Type
#Options Are
    #["background", "aeroplane", "bicycle", "bird", "boat",	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	#"dog", "horse", "motorbike", "person", "pottedplant", "sheep",	"sofa", "train", "tvmonitor"]
AlertObjectType = ["person", "car"]

#Enable Face Detection
FaceDetectionEnabled = 'true'

#Destination number for MMS & SMS notifications
AlertPhoneDestination = ['+' + '1234567890', '+' + '1234567890'] #list , seperated add phone numbers are desired

#Definitions to return the desired config values from above
def ReturnDropBoxAPIKey():
    return DropBoxAPIKey

def ReturnSMTPPort():
    return SMTPPort

def ReturnSMTPServer():
    return SMTPServer 

def ReturnSMTPLogin():
    return SMTPLogin

def ReturnMailEnabled():
    return MailEnabled

def ReturnSMTPToAddress():
    return SMTPToAddress

def ReturnSMTPToAddress():
    return SMTPToAddress

def ReturnTwilioSID():
    return TwilioSID

def ReturnTwilioAuthToken():
    return TwilioAuthToken

def ReturnTwilioSourcePhone():
    return TwilioSourcePhone

def ReturnTwilioSMSEnabled():
    return TwilioSMSEnabled

def ReturnTwilioMMSEnabled():
    return TwilioMMSEnabled

def ReturnRDODProtoTXT():
    return RTODPrototxt

def ReturnRTODModel():
    return RTODModel

def ReturnRTODSystemConfidence():
    return RTODSystemConfidence

def ReturnRTODFrameSleep():
    return RTODFrameSleep

def ReturnAlertPhoneDestination():
    return AlertPhoneDestination

def ReturnDectectionPercentage():
    return DectectionPercentage

def ReturnAlertObjectType():
    return AlertObjectType

def ReturnFaceDetectionEnabled():
    return FaceDetectionEnabled

def ReturnAlertPhoneDestination2():
    return AlertPhoneDestination2