# read the files inside the files_to_upload folder and upload them on dropbox

import os
import dropbox
import datetime
import shutil
from subscriber_info import subscriber
from paths import folder_paths
from database_configuration_scripts.operations_on_database_methods import log_operations

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

log_operations(USER, text='Zipping images')

os.system("zip -r {0}/images_{1}_{2} {0}".format(folderToUploadPath, USER, TODAY))

try:
    log_operations(USER, text='uploading zip file to dropbox')
    print("uploading zip file to dropbox")
    file_from = folderToUploadPath+"/images_"+USER+'_'+TODAY+".zip"
    file_to = "/images_"+USER+"_"+TODAY
    transferData.upload_file(file_from, file_to)
except:
    print("error cannot upload the file")
    log_operations(USER, text="error in uploading the file, creating a local copy of the folder to temporary save the file")
    # save the zip file inside the backup folder
    shutil.copy(folderToUploadPath+"/images_"+USER+'_'+TODAY+".zip", folderBackup+"/images_"+USER+'_'+TODAY+".zip")

log_operations(USER, text='Upload completed, starting to remove images from tmp folder and to_upload folder')
# remove all the files in the to_upload folder and tmp folder
shutil.rmtree(folderToUploadPath)
shutil.rmtree(folderTmp)
# recreate the removed directories
os.makedirs(folderToUploadPath)
os.makedirs(folderTmp)
log_operations(USER, text='images removed, going to sleep :)')
