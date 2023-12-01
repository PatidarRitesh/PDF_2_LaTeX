import os
import tarfile 
import re
import subprocess

def extract_tar_files(src_folder, dest_folder):

    # Ensure the destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # List all files in the source folder
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)

        # Check if the file is a .tar.gz file
        if filename.endswith('.tar.gz'):
            print(f"Extracting {filename} to {dest_folder}...")
            
            # Open and extract the .tar.gz file
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(dest_folder)
            
            print(f"{filename} extracted successfully.")





# year wise  first level extraction
year='/mnt/NFS/patidarritesh/PDF_2_TEX/2023/src'
target="/mnt/NFS/patidarritesh/PDF_2_TEX/2023/target_src"
extract_tar_files(year, target)