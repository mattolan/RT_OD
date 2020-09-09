#https://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script
#must install dropbox modules
#pip install dropbox
import sys
import pathlib
import dropbox
import re
import datetime
from Email import Send_Mail
import ConfigValues

def UploadToDropBox(filename):
    try:
        #the source file
        folder = pathlib.Path(".")    # located in this folder
        #filename = "img.jpg"         # file name
        filepath = folder / filename  # path object, defining the file

        #target location in Dropbox
        #target = "/Detection/"              # the target folder
        #targetfile = target + filename #datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')  # the target path and file name
        
        newfilename = "/Detection/"  + str(datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')) + filename
        targetfile = newfilename

        print("Begin uploading " + targetfile + " to DropBox")
        
        #Create a dropbox object using an API v2 key
        d = dropbox.Dropbox(ConfigValues.ReturnDropBoxAPIKey())

        # open the file and upload it
        with filepath.open("rb") as f:
           # upload gives you metadata about the file
           # we want to overwite any previous version of the file
           meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))

        # create a shared link
        link = d.sharing_create_shared_link(targetfile)

        # url which can be shared
        url = link.url

        # link which directly downloads by replacing ?dl=0 with ?dl=1
        dl_url = re.sub(r"\?dl\=0", "?raw=1", url)
        #print (dl_url)
    
        #Check for error
        if dl_url[0:5] != "https":
            print("Error")
            Send_Mail(filename, "RT_OD - DropBox Error:", "")

        return dl_url
    except:
       print("Oops!, DropBox Error: ", sys.exc_info()[0], "occurred.")
       Send_Mail(filename, "RT_OD - DropBox Error:", "")

