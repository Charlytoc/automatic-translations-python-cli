
import os
import shutil

def copy_mp4_to_uploadable():
    source_dir = 'output/'
    destination_dir = 'uploadable_videos/'
    
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.mp4'):
                shutil.copy(os.path.join(root, file), destination_dir)

copy_mp4_to_uploadable()
