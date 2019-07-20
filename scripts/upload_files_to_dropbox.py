# read the files inside the files_to_upload folder and upload them on dropbox

import os
import dropbox
import datetime
import shutil
from subscriber_info import subscriber
from paths import folder_paths

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)


# read the files from the folder
folderToUploadPath = folder_paths['files_to_upload_path']
# in this folder i will save the files that for any reason could t be transfered in the dropbox folder
folderBackup = folder_paths['files_to_reupload_path']
#tmp folder
folderTmp = folder_paths['tmp_img_folder_path']
# access token to dropbox
DB_ACCESS_TOKEN = 'ro0Z_2nW1rAAAAAAAAAACZV3mhao6zTK4-1I9ksskp_PhQ6YS7WV_J8MSk386u5a' # need to see how to make this secret in some way also with the database connection info
USER = subscriber['name']
TODAY = str(datetime.datetime.now().date())

dbx = dropbox.Dropbox(DB_ACCESS_TOKEN)
image_name_list = os.listdir(folderToUploadPath)

print(image_name_list)

# check if possible to upload all the folder and rename it as such:
# subscriber_currentDate

transferData = TransferData(DB_ACCESS_TOKEN)

for image in image_name_list:
    try:
        file_from = folderToUploadPath+'/'+image
        file_to = '/images_'+USER+'_'+TODAY+'/'+image  # The full path to upload the file to, including the file name
        transferData.upload_file(file_from, file_to)
    except:
        print("error in uploading the files, creating a local copy of the folder with the issue")
        # save the files that could t be transferd to dropbox to a backup folder
        # create the folder specific to the current day and save inside the files
        if not os.path.exists(folderBackup+'/'+TODAY):
            print("folder doesn`t exists, creating a new one")
            os.makedirs(folderBackup+'/'+TODAY)
        # save images inside the folder
        shutil.copy(folderToUploadPath+'/'+image, folderBackup+'/'+TODAY+'/'+image)

# remove all the files in the to_upload folder and tmp folder
# for image in image_name_list:
#     os.remove(folderToUploadPath+"/"+image)
#     os.remove(folderTmp+"/"+image)