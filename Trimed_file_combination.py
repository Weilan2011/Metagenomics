# combine the contents of sub-folders into one main folder (Weilan)
import os
import shutil

# Specify the main folder and the destination folder
main_folder = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_shotgun_Prokka'
destination_folder = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_dbCAN3'

# List all sub-folders in the main folder
sub_folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

# Iterate through each sub-folder and move its contents to the destination folder
for sub_folder in sub_folders:
    sub_folder_path = os.path.join(main_folder, sub_folder)
    for item in os.listdir(sub_folder_path):
        item_path = os.path.join(sub_folder_path, item)
        destination_path = os.path.join(destination_folder, item)
        if os.path.isdir(item_path):
            shutil.copytree(item_path, destination_path)
        else:
            shutil.copy2(item_path, destination_path)

print("Contents of sub-folders have been combined into the destination folder.")