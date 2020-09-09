# -*- coding: utf-8 -*-
# The first step is always the same: import all necessary components:
import sys
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
from email import encoders 
from email.mime.image import MIMEImage
import os
import argparse
import ConfigValues

def Send_Mail(Image_Path, name, label):
    try:
        port = ConfigValues.ReturnSMTPPort() 
        smtp_server = ConfigValues.ReturnSMTPServer() 
        login = ConfigValues.ReturnSMTPLogin() 
        password = ConfigValues.ReturnSMTPPassword() 

        fromaddr = ConfigValues.ReturnSMTPLogin() 
        toaddr = ConfigValues.ReturnSMTPToAddress() 
        
        msg = MIMEMultipart() 
        msg['From'] = fromaddr
        msg['To'] = toaddr 
        msg['Subject'] = name + ": Alert -" + label
        body = "Detection Image Attached"
        
        msg.attach(MIMEText(body, 'plain')) 
        
        if Image_Path != "":
            image_filename = Image_Path #'C:\Build3\RT_OD\Alert_image.jpg'#'./img.jpg'
            image = MIMEImage(open(image_filename, 'rb').read(), name=os.path.basename(image_filename))
    
            msg.attach(image)
        
        s = smtplib.SMTP(smtp_server, port) 
        s.starttls() 
        s.login(fromaddr, password) 

        text = msg.as_string() 

        s.sendmail(fromaddr, toaddr, text) 
        s.quit() 

        print('Sent')
    except:
        print("Oops!, Send Email Error: ", sys.exc_info()[0], "occurred.")
        print("For GMAIL Authentication errors please ensure allow less secure apps is enabled https://myaccount.google.com/lesssecureapps?pli=1")


