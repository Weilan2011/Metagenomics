import os
import shutil

# Path where your files are currently stored
source_directory = '/home/weilan/Desktop/Raf_shotgun_desktop/Raf_dbCAN3_Substrate'

# Get all files in the directory
files = os.listdir(source_directory)

for file in files:
    # Extract the part of the filename after '_dbCAN_substrate_'
    parts = file.split('_dbCAN_substrate_')
    if len(parts) > 1:
        # The extension is what follows '_dbCAN_substrate_', taking everything up to the next dot or the end of the filename
        extension = parts[1].split('.')[0]
        # Define the folder name based on the extension
        extension_folder = extension
    else:
        continue  # If no '_dbCAN_substrate_' is found, skip the file

    # Create a new directory for this extension if it doesn't exist
    target_directory = os.path.join(source_directory, extension_folder)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Move the file to the new directory
    shutil.move(os.path.join(source_directory, file), target_directory)

print("Files have been organized.")
