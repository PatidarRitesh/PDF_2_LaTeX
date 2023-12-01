import os
import tarfile 
import re
import subprocess
from tqdm import tqdm
import json
from tqdm import tqdm


def extract_tar_gz(year_directory,folder, year):
    input_directory = os.path.join(year_directory, "target_src")
    output_directory = os.path.join(year_directory, "final_extracted")
    temp_src_folder = os.path.join(year_directory, "temp_folder")
    # input_directory contain the subfolder. extract those subfolder in output_directory and name of extracted file should be subfolder name without .gz
    lst_not_extracted=[]
    count_target_src = 0
    count_extracted_src=0

    # folders=os.listdir(input_directory) 
    # for folder in folders: # folder contains the folder for 2301, 2302, 2303, 2304, 2305,...
    
    # create the absolute path of the folder,  eg /mnt/NFS/patidarritesh/PDF_2_TEX/2023/target_src/2301
    # and month_folder contains the list of all zip files in the folder- let say 2301
    month_folder=os.listdir(os.path.join(input_directory, folder))   
    count_target_src = len(month_folder)  
    
    for file in month_folder:  # for each zip file in the folder- let say 2301.00696.gz
        # get the absolute path of the zip file ; /mnt/NFS/patidarritesh/PDF_2_TEX/2023/target_src/2301/2301.00696.gz 
        file_path=os.path.join(input_directory,folder, file) 
        
        # destination path : "/mnt/NFS/patidarritesh/PDF_2_TEX/2023/final_extracted/2301/2301.00696"
        dest_dir=os.path.join(output_directory,folder, file[:-3])
        
        os.makedirs(dest_dir, exist_ok=True)
        print(f"Extracting {file} to {dest_dir}")
        
        try:
            subprocess.run(["tar", "-xzf", file_path, "-C", dest_dir], check=True)
            print(f"Successfully extracted {file} to {dest_dir}")
        
        except subprocess.CalledProcessError:
            print(f"Error extracting {file}")
            
            try:
                # delete the file created by tar command in dest_dir which ends with a dot 
                # eg. 2301.00696.   fyi: this folder is created by tar command when failed to extract the pdf file
                subprocess.run(["rm", "-r", dest_dir], check=True)
                # first copy the file to temp_src_folder
                # then extract the file using gunzip command in temp_src_folder and set the file type to .tex
                # then move the extracted file to output_directory
                os.makedirs(temp_src_folder, exist_ok=True)
                subprocess.run(["cp", file_path, temp_src_folder], check=True)
                print(f"Successfully copied {file} to {temp_src_folder}")
                
                subprocess.run(["gunzip", os.path.join(temp_src_folder, file)], check=True)
                print(f"Successfully extracted {file} to {temp_src_folder}")
                
                os.rename(os.path.join(temp_src_folder, file[:-3]), os.path.join(temp_src_folder, "main.tex"))
                print(f"Successfully renamed {file[:-3]} to {'main.tex'}")
                
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                
                subprocess.run(["mv", os.path.join(temp_src_folder, "main.tex"), dest_dir], check=True)
                print(f"Successfully moved {file[:-3]+'.tex'} to {dest_dir}")
                # delete all the files in temp_src_folder

            except subprocess.CalledProcessError:
                print(f"Error extracting {file}")
                lst_not_extracted.append(file_path)
            # finally:
            #     subprocess.run(["rm","-r", temp_src_folder], check=True)

    
    count_extracted_src = len(os.listdir(os.path.join(output_directory,folder)))
    # make a json for the below three print statements and save it in the output_directory


    # Define the data for the JSON object   
    data = {
        "month: yymm": folder, 
        "count_target_src " : count_target_src , 
        "Count_Final_extracted": count_extracted_src,
        "lst_not_extracted": lst_not_extracted
    }
    # Save the data as a JSON file
    # Create the directory if it doesn't exist
    output_filename = f"stats_{folder}.json"
    json_out = f"{year_directory}/json_files/"
    
    os.makedirs(json_out, exist_ok=True)
    
    with open(os.path.join(json_out, output_filename), "w") as json_file:
        json.dump(data, json_file, indent=4)

    
    print("count_target_src :  ", count_target_src ) 
    print("Count Final_extractes", count_extracted_src)
    print("count_extracted_src: ", count_target_src - len(lst_not_extracted))
    print("lst_not_extracted: ", lst_not_extracted)
    



## Merging multiple .tex files into one .tex file


# Pattern1: """\input""" and/or """\include""" commands with optional whitespace and an optional group name enclosed in curly braces.
pattern  = r'(\\input\s*{?([A-Za-z0-9_-]+))|(\\include\s*{?([A-Za-z0-9_-]+))'

# Pattern2: """\begin""" commands, optional whitespace, strings "{document}", "{Document}", or "{DOCUMENT}"
pattern2 = r"(\\begin\s*{?document)|(\\begin\s*{?Document)|(\\begin\s*{?DOCUMENT)"

# pattern3: Extension of pattern1 to and 2
pattern3 = r'(%+\s*\\input\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)|(%+\s*\\include\s*{?([A-Za-z0-9\/_-]+)(\.tex)*}?)|(\\input\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)|(\\include\s*{?([A-Za-z0-9\/_-]+)(\.tex)*}?)'

# pattern4: To match bibliography commands
pattern4 = r'/(\\bibliographystyle\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)|(%+\s*\\bibliographystyle\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)|(\\bibliography\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)|(%+\s*\\bibliography\s*{?([A-Za-z0-9_\/-]+)(\.tex)*}?)'

#----------------------------------------------------------------------------------------------
def check_bbl_exists(directory):

    # walk through the directory and check if there is a .bbl file
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.bbl'):
                return os.path.splitext(file)[0]
    return None
    # Returns name of bbl file if exists, NONE otherwise

#----------------------------------------------------------------------------------------------
def get_root_files(directory):
    lst_no_root = []  # Initialize an empty list to store files with no root file

    root_files = []  # Initialize an empty list to store root files

    name_bbl = check_bbl_exists(directory)  # Check if a .bbl file exists in the directory

    if name_bbl:
        # If a .bbl file exists, check if a .tex file with the same name is present
        if name_bbl + '.tex' in os.listdir(directory):
            root_files.append(name_bbl + '.tex')  # Add the .tex file to the root_files list
            return root_files  # Return the list of root files
    
    # Loop through the files in the directory to identify potential root files
    for file in os.listdir(directory):
        if file.endswith('.tex'):
            with open(os.path.join(directory, file), 'rb') as f:
                try:
                    data = f.read()
                    try:
                        data = data.decode("utf-8")  # Ignore non-UTF-8 characters
                    except:
                        data = data.decode("latin-1", errors="ignore")
                    
                    # Search for patterns in the file content
                    res = re.findall(pattern2, data)  

                    # Add the file to the root_files list if a pattern is found
                    if len(res) and (res[0] != "" or res[1] != "" or res[2] != ""):
                        root_files.append(file)  
                except Exception as e:
                    print("%" * 50, "\nError in file:", file, ":", directory, e)
                    lst_no_root.append(file)
                    # # Copy the file directory to a new folder named NO_ROOT
                    # subprocess.run(["cp", "-r", file, os.path.join(directory,"NO_Root")])  

    return root_files  # Return the list of potential root files

#----------------------------------------------------------------------------------------------
def get_include_file_name_from_root_file(root_file):
    with open(root_file, 'rb') as f:
        try:
            str=f.read()
            try:
                str = str.decode("utf-8")  # Ignore non-UTF-8 characters
            except:
                str = str.decode("latin-1", errors="ignore")
            
            # res=re.findall(pattern3,str)
            include_files = re.findall(pattern3, str)
            file_names_to_be_included = []
            for include_file in include_files:
                if include_file[5] != "":
                    file_names_to_be_included.append(include_file[5])
                if include_file[7] != "":
                    file_names_to_be_included.append(include_file[7])
        except Exception as e:
            print(f'Errr in {root_file}: {e}')
            
    return list(set(file_names_to_be_included))
#----------------------------------------------------------------------------------------------
# Function to recursively merge input files
def merge_input(file_name1, file_name2, root_file_path):
    input_folder, root_file_name = os.path.dirname(root_file_path), os.path.basename(root_file_path)
    file_name = file_name1 if file_name1 != "" else file_name2
    if file_name == None or file_name == "":
        return ""
    print(f"Processing {file_name}")
    print(f'input_folder = {input_folder} file_name = {file_name} root_file_name = {root_file_name}')
    file_path = os.path.join(input_folder, file_name)
    # print(f"{file_name} == {root_file_name} or {file_name+'.bbl'} == {root_file_name}")
    try:
        if file_name == root_file_name or file_name+'.tex' == root_file_name:
            print("importing bibliography..................")
            tex_content = ""
            with open(file_path+".bbl", "rb") as tex_file:
                tex_content = tex_file.read()
        else:
            with open(file_path+".tex", "rb") as tex_file:
                tex_content = tex_file.read()
        try:
            tex_content = tex_content.decode("utf-8")
        except:
            tex_content = tex_content.decode("latin-1", errors="ignore")
        return tex_content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""  # Return an empty string if the file is missing
    except Exception as e:
        print(f"Error in {file_path}: {e}")
        return ""
#----------------------------------------------------------------------------------------------
def merge_bibliography(file_name, root_file_path):
    if file_name  ==  "":
        return ""
    print(f"Processing {file_name}")
    # get the content from the .bbl file the same folder by walking through the directory
    input_folder, root_file_name = os.path.dirname(root_file_path), os.path.basename(root_file_path)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.bbl'):
                with open(os.path.join(root,file), 'rb') as f:
                    try:
                        str=f.read()
                        try:
                            str = str.decode("utf-8")  # Ignore non-UTF-8 characters
                        except:
                            str = str.decode("latin-1", errors="ignore")
                        return str
                    except Exception as e:
                        print(f'Errr in {root_file_path}: {e}')
    print(f"File not found: {file_name}")
    return ""  # Return an empty string if the file is missing
#----------------------------------------------------------------------------------------------
def replace_import_with_file_data(root_file, output_folder_path):
    with open(os.path.join(root_file), 'rb') as f:
        # try:
            str=f.read()
            str = str.decode("utf-8", errors="ignore")  # Ignore non-UTF-8 characters
            # merged_content = re.sub(pattern3, lambda match: merge_input(match.group(6), match.group(8), os.path.dirname(root_file)), str)
            # merge the tex file with input or include command
            merged_content = re.sub(pattern3, lambda match: merge_input(match.group(8), match.group(11), root_file), str)
            # merge the bbl file with bibliography command
            merged_content = re.sub(pattern4, lambda match: merge_bibliography(match.group(7), root_file), merged_content)

            # Write the merged content to the output folder with subfolder name
            output_filename = f"{os.path.basename(os.path.dirname(root_file))}.tex"
            print(f"Writing {output_filename}")
            print(f"Writing {output_folder_path}")
            output_path = os.path.join(output_folder_path, output_filename)
            with open(output_path, "w", encoding="utf-8") as output_tex:
                output_tex.write(merged_content)

        # except Exception as e:
        #     print(f'Errr in {root_file}: {e}')            
#----------------------------------------------------------------------------------------------

# 
# we will have one folder final_extracted 
# which contains month wise folders
# create final_merged folder with same subfolders as final_extracted
# create a folder final_merged

def merge_final(year_directory, folder):
    count_final_merged = 0
    if not os.path.exists(os.path.join(year_directory, 'final_merged')):
        os.mkdir(os.path.join(year_directory, 'final_merged'))

    # create month wise folders in final_merged
    
    # for folder in os.listdir(os.path.join(year_directory, 'final_extracted')):
    if not os.path.exists(os.path.join(year_directory, 'final_merged', folder)):
        os.mkdir(os.path.join(year_directory, 'final_merged', folder))

    # Each month folder will have a list of directories in it which are the extracted zip of each paper
    # for folder in os.listdir(os.path.join(year_directory, 'final_extracted')):
    for paper_folder in os.listdir(os.path.join(year_directory, 'final_extracted', folder)):
        # process the paper folder and write the merged file in the respective month folder
        # parent_dir = "/mnt/NFS/patidarritesh/PDF_2_TEX/2023/Test/2302.00217"
        parent_dir = os.path.join(year_directory, 'final_extracted', folder, paper_folder)
        output_folder_path = os.path.join(year_directory, 'final_merged', folder)
        # print(f"All the files in the directory: {os.listdir(parent_dir)}")
        count_tex = 0
        count_bbl = 0
        bbl_file = ''

        for root, dir, files in os.walk(parent_dir):
            for file in files:
                if file.endswith('.tex') or file.endswith('.TEX'):
                    count_tex+=1
                if file.endswith('.bbl') or file.endswith('.BBL'):
                    count_bbl+=1
                    bbl_file = file

        # print(count_tex, count_bbl)
        # print(paper_folder)
        if(count_tex>1):
            try:
                root_file = get_root_files(parent_dir)
                print(f'Paper {paper_folder} Root file: {root_file}')
                replace_import_with_file_data(os.path.join(parent_dir, root_file[0]), output_folder_path)
                count_final_merged+=1
            except:
                print(f'Error in {parent_dir}')
        elif(count_tex == 1):
            for root, dir, files in os.walk(parent_dir):
                for file in files:
                    try:
                        if file.endswith('.tex') or file.endswith('.TEX'):
                            if count_bbl == 0:
                                # find the path of tex file
                                # copy the tex file to the output folder renaming as the paper folder name
                                os.rename(os.path.join(parent_dir, file), os.path.join(parent_dir, paper_folder+'.tex'))
                                print(f"Successfully renamed {file} to {paper_folder+'.tex'}")

                                file_path = os.path.join(parent_dir, paper_folder+'.tex')

                                subprocess.run(["cp", file_path, output_folder_path], check=True)
                                print(f"Successfully copied {file} to {output_folder_path}")
                                count_final_merged+=1
                            else:
                                replace_import_with_file_data(os.path.join(parent_dir, file), output_folder_path)
                                count_final_merged+=1
                            break
                    except:
                        print(f'error in {parent_dir}')
                        # lst.append()
    print("Count Merged = ",count_final_merged)
#----------------------------------------------------------------------------------------------
     # Specify the path to the JSON file
    filename = f"stats_{folder}.json"
    json_directory = os.path.join(year_directory,"json_files")
    json_file_path = os.path.join(year_directory,"json_files", filename)

    # Check if the JSON file exists
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)
    if not os.path.isfile(json_file_path):
        print(f"JSON file '{filename}' does not exist. Creating a new one.")
        
        # Create a new empty JSON file

        with open(json_file_path, 'w') as file:
            json.dump({}, file)

    # Load the JSON data from the file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Perform your edits on the data (for example, add a new key-value pair)
    data["count_final_merged"] = count_final_merged

    # Save the modified data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        

import os
import tarfile
import subprocess

def stats(year_directory, folder,year):
    src = os.path.join(year_directory, 'final_extracted')
    count1 = 0
    count0 = 0
    count2 = 0
    counttot = 0
    countntextr = 0
    countntdir = 0
    print(len(os.listdir(src)))
    # for folder in os.listdir(src):
    # List all items in the directory
    items = os.listdir(os.path.join(src,folder))
    # print(items)
    lst0 = []
    lst1 = []
    lst2 = []
    lst_ntextr = []
    lst_ntdir = []
    lst_main_tex = []
    lst_no_main=[]
    
    # Iterate through the items in the directory
    for item in items:
        item_path = os.path.join(src,folder, item)

        # Check if the item is a file with a .gz extension
        # if os.path.isfile(item_path) and (item.endswith('.gz') or item.endswith('.pdf')):
        #     # Delete the .gz file
        #     os.remove(item_path)
        #     print(f"Deleted file: {item}")

        if(os.path.isdir(item_path)):
            if(len(os.listdir(item_path)) == 0):
                lst_ntextr.append(item_path)
            
            else:
                count = 0
                flag=False
                for sub in os.listdir(item_path):
                    if(os.path.basename(sub).lower() == "main.tex"):
                        lst_main_tex.append((item_path))
                        flag=True
                    
                    if sub.endswith('.tex') or sub.endswith('.TEX') :
                        count+=1
            
                if(count == 0):
                    lst0.append(item_path)
                    # os.rmdir(item_path)
                if(count == 1):
                    lst1.append(item_path)
                if count>1:
                    lst2.append(item_path)
                    if flag==False:
                        lst_no_main.append(item_path)
        elif(not(item_path.endswith('.gz'))):
            lst_ntdir.append(item_path)
    countntextr = countntextr+len(lst_ntextr)
    count1 = count1+len(lst1)
    count0 = count0+len(lst0)
    count2 =  count2+len(lst2)
    countntdir = countntdir + len(lst_ntdir)
    counttot = counttot+len(lst0)+len(lst1)+len(lst2)+len(lst_ntextr) + len(lst_ntdir)
    tot = len(lst0)+len(lst1)+len(lst2)+len(lst_ntextr)+len(lst_ntdir)
    print("------------------------------------------------------------")
    print("Month_name: ",folder)
    print()
    print("File : ", os.path.basename(folder))
    print()
    print("0 .tex file: ", len(lst0))
    print("1 .tex file: ", len(lst1))
    print(">1 .tex file: ",len(lst2))
    print("Failed extraction: ", len(lst_ntextr))
    print("Not a directory: ", len(lst_ntdir))
    print("------------------------------------------------------------")
    count_final_merged_papers = len(os.listdir(os.path.join(year_directory, 'final_merged', folder)))
    data = {

        "0_texfile":str(len(lst0)),
        "1_texfile":str(len(lst1)),
        ">1_texfile":str(len(lst2)),
        "Failed_extraction":str(len(lst_ntextr)),
        "Not_directory" :str(len(lst_ntdir)),
        "Main_TEX": str(len(lst_main_tex)),
        "no_main": str(len(lst_no_main)),

        "list_of_main":  lst_main_tex,
        "list_of_no_main": lst_no_main,
        "Failed_extraction": lst_ntextr
        }
#----------------------------------------------------------------------------------------------
    # Specify the path to the JSON file
    filename = f"stats_{folder}.json"
    json_file_path = os.path.join(year_directory,"json_files", filename)

    # Check if the JSON file exists
    if not os.path.isfile(json_file_path):
        print(f"JSON file '{filename}' does not exist. Creating a new one.")
        
        # Create a new empty JSON file
        with open(json_file_path, 'w') as file:
            json.dump({}, file)
        return

    # Load the JSON data from the file
    with open(json_file_path, "r") as json_file:
        maindata = json.load(json_file)

    maindata.update(data)

    # Save the modified data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(maindata, json_file, indent=4)







year = '2023'
year_directory = f"/mnt/NFS/patidarritesh/PDF_2_TEX/{year}"


tot_json = f"Tot_JSON_{year}.json"
tot_json_file_path = os.path.join(year_directory,"json_files", tot_json)
json_subdirectory = os.path.join(year_directory, "json_files")

# Check if the directory exists; if not, create it
if not os.path.exists(json_subdirectory):
    os.makedirs(json_subdirectory)

if not os.path.isfile(tot_json_file_path):
        # Create a new empty JSON file
        with open(tot_json_file_path, 'w') as file:
            json.dump(
                {'count_final_merged': '0',
                'count_target_src': '0'},
                         file)


for i in tqdm(range(1,13)):
    folder = year[-2:]+str(i).zfill(2)
    try:
        
        extract_tar_gz(year_directory, folder, year)
        merge_final(year_directory, folder)
        stats(year_directory, folder,year)

        path_target_src = os.path.join(year_directory, 'target_src', folder)
        path_final_merged = os.path.join(year_directory, 'final_merged', folder)

        target_src = sorted(os.listdir(path_target_src))
        final_merged = sorted(os.listdir(path_final_merged))

        print(target_src[0], target_src[-1], len(target_src))

        data = {
            'count_final_merged': str(len(final_merged)),
            'count_target_src': str(len(target_src)),
            'last_paper': str(target_src[-1])
        }
        # Specify the path to the JSON file
        filename = f"count_target_src_{folder}.json"
        json_file_path = os.path.join(year_directory,"json_files", filename)

        # Check if the JSON file exists
        if not os.path.isfile(json_file_path):
            # Create a new empty JSON file
            with open(json_file_path, 'w') as file:
                json.dump({}, file)

        # Load the JSON data from the file
        with open(json_file_path, "r") as json_file:
            maindata = json.load(json_file)

        maindata.update(data)

        # Save the modified data back to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(maindata, json_file, indent=4)

        with open(tot_json_file_path, "r") as json_file:
            maindata = json.load(json_file)
        maindata['count_final_merged'] = str(int(maindata['count_final_merged']) + len(final_merged))
        maindata['count_target_src'] = str(int(maindata['count_target_src']) + len(target_src))
        # subprocess.run(["rm","-r", f'/mnt/NFS/patidarritesh/PDF_2_TEX/2023/final_extracted/{folder}'], check=True)
        with open(tot_json_file_path, "w") as json_file:
            json.dump(maindata, json_file, indent=4)

    except Exception as e:
        print(f'{e} Error in {folder}')
