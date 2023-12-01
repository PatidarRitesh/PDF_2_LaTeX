import os
import tarfile 
import re
import subprocess
from tqdm import tqdm
import json


for year in range(2000, 2024):
    year = str(year)
    year_directory = f"/mnt/HDFS/patidarritesh/pdf_extr/{year}"

    tot_json = f"Tot_JSON_{year}.json"
    tot_json_file_path = os.path.join(year_directory,"json_files", tot_json)
    json_subdirectory = os.path.join(year_directory, "json_files")

    # Check if the directory exists; if not, create it
    if not os.path.exists(json_subdirectory):
        os.makedirs(json_subdirectory)

    # Create a new empty JSON file
    with open(tot_json_file_path, 'w') as file:
        json.dump({'count_pdf': '0'},file)
    # print(year)
    for i in tqdm(range(1,13)):
        folder = year[-2:]+str(i).zfill(2)

        path_month = os.path.join(year_directory, folder)
        if not os.path.exists(path_month):
            os.makedirs(path_month)

        lst_pdf_name = sorted(os.listdir(path_month))
        data = {
            'count_pdf' : len(lst_pdf_name),
            'lst_pdf_name' : lst_pdf_name
        }
        
        filename = f"Stats_{folder}.json"
        json_file_path = os.path.join(year_directory,"json_files", filename)
        json_subdirectory = os.path.join(year_directory, "json_files")

        if not os.path.exists(json_subdirectory):
            os.makedirs(json_subdirectory)
        
        # Create a new empty JSON file
        with open(json_file_path, 'w') as file:
            json.dump(data, file)

        with open(tot_json_file_path, "r") as json_file:
                maindata = json.load(json_file)
        maindata['count_pdf'] = str(int(maindata['count_pdf']) + int(data['count_pdf']))
            
        with open(tot_json_file_path, "w") as json_file:
            json.dump(maindata, json_file, indent=4)


        