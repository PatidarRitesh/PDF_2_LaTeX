# imports 
import os
import re
import csv
import sys
from time import time
import logging
import subprocess
from tqdm import tqdm
# multiprocessing using joblib
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Pool
num_cores = multiprocessing.cpu_count()

#-------------- Initializing logger ---------------------
root_log_dir = '/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/extract_meta_data_img_bib/'
logging.basicConfig(level=logging.INFO, filename=f"{root_log_dir}tc_extracted.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info(f"Number of cores: {num_cores}")


# -------------- Initializing useful data structures --------------
output_root_dir = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED"
input_root_dir = "/mnt/NFS/patidarritesh/PDF_2_TEX"

pattern_image1 = [r'\\begin{figure}', r'\\end{figure}']
pattern_image2 = [r'\\begin{figure*}', r'\\end{figure*}']
pattern_image3 = [r'\\begin{teaserfigure}', r'\\end{teaserfigure}']
pattern_image4 = [r'\\begin{teaserfigure*}', r'\\end{teaserfigure*}']
pattern_image5 = [r'\\begin{wrapfigure}', r'\\end{wrapfigure}']
pattern_image6 = [r'\\begin{wrapfigure*}', r'\\end{wrapfigure*}']

dummy_image = '''\n\\begin{figure}[h]\n\\includegraphics[]{image_name}\n\\label{fig:label}\n\\end{figure}\n\n'''
# pattern_image7 = r'\\includegraphics' \n
'''
\\begin{figure*}
\\end{figure*}

\\begin{figure}
\\end{figure}

\\begin{teaserfigure}
\\end{teaserfigure}

\\includegraphics
'''
pattern_bib = [r"\\begin{thebibliography}",r"\\end{thebibliography}"]
pattern_meta_data = [r"\\begin{document}",r"\\end{document}" ]

bib_dict = dict()

#_________________________________________________________________________________
# for bibliography and all figures
def remove_content_in_between(data, pattern):
    start_pattern, end_pattern = pattern
    bib_data = ""
    if start_pattern == r"\\begin{thebibliography}":
        # with open("temp.text", "w") as f:
        #     f.write(data)
        matches = re.finditer(start_pattern, data)
        if matches:
            new_data = ""
            prev_end = 0
            for match in matches:
                start = match.start()
                end_match = re.search(end_pattern, data[start:])
                if end_match is None:
                    # logger.error(f"end_pattern: {end_pattern}, not found")
                    return None, ""
                end = end_match.end()
                new_data += data[prev_end:start]
                prev_end = start + end
                bib_data += data[start : start + end] + "\n"
            bib_data = re.sub('\n+','\n',bib_data)
            new_data = new_data + data[prev_end:]
            data = new_data
        
    else:
        matches = re.finditer(start_pattern, data)
        if matches:
            new_data = ""
            prev_end = 0
            for match in matches:
                start = match.start()
                end_match = re.search(end_pattern, data[start:])
                if end_match is None:
                    # logger.error(f"end_pattern: {end_pattern}, not found")
                    return None, ""
                end = end_match.end()
                new_data += data[prev_end:start] + dummy_image
                prev_end = start + end 
            new_data = new_data + data[prev_end:]
            data = new_data
    return data, bib_data

#_________________________________________________________________________________
# for begin{document} and end{document}
def remove_content_outside(data, pattern):
    start_pattern, end_pattern = pattern
    matches = re.finditer(start_pattern, data)
    if matches:
        # if len(list(matches)) > 1:
        #     logger.error(f"More than one begin_document found")
        #     return -1
        for match in matches:
            start,end_beign = match.start(), match.end()
            end_match = re.search(end_pattern, data[start:])
            if end_match is None:
                logger.error(f"end_document not found")
                return -2
            start_end, end = end_match.start(), end_match.end()
            return (data[end_beign: start+start_end])
            # return data[start:end]
    return data
    

#_________________________________________________________________________________
def process_data(input_dir, output_dir):
    logging.basicConfig(level=logging.INFO, filename=f"{root_log_dir}tc_extracted.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    err_count = 0
    files = os.listdir(input_dir)
    for file in tqdm(files):
        # file = "2301.00009.tex"
        # file = '/mnt/NFS/patidarritesh/PDF_2_TEX/2000/preprocessing_1/0001/cs0001013.tex'
        try:
            data = ""
            bib_data = ""
            # print(input_dir + "/" + file)
            # exit()
            with open(input_dir + "/" + file, "rb") as f:
                data = f.read()
                try:
                    data = data.decode("utf-8")  # Ignore non-UTF-8 characters
                except:
                    data = data.decode("latin-1", errors="ignore")
                
                #__________________________________________________________________________________
                # In[2]: remove all the text between \begin{thebibliography} and \end{thebibliography}
                data,bib_data = remove_content_in_between(data, pattern_bib)
                if data is None:
                    # logger.error(f"Error in file {input_dir + '/' + file}: end_pattern: {pattern_bib[1]}, not found")
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image1)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image1[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image2)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image2[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image3)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image3[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image4)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image4[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image5)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image5[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")
                data,_ = remove_content_in_between(data, pattern_image6)
                if data is None:
                    raise Exception(f"Pattern Not Found: end_pattern: {pattern_image6[1]}, not found")
                    print(f"Pattern Not Found: end_pattern: {pattern_bib[1]}, not found")

                data = remove_content_outside(data, pattern_meta_data)
                # print(data)
                if data == -1:
                    raise Exception(f"More than one begin_document found")
                    print(f"More than one begin_document found")
                elif data == -2:
                    raise Exception(f"end_document not found")
                    print(f"end_document not found")

                #__________________________________________________________________________________
                # In[3]: remove all the multiple new line character
                data = re.sub('\t+','',data)
                data = re.sub('\n+','\n',data)

                #__________________________________________________________________________________
                # In[]: write back the data
                file_path = output_dir + "/" + file
                
                bib_file_path = output_dir + "/" + os.path.splitext(file)[0] + ".bib"
                # Use 'w' mode to create a new file (or overwrite an existing one)
                with open(bib_file_path, "wb") as f:
                    try:
                        data1 = bib_data.encode("utf-8")  # Ignore non-UTF-8 characters
                    except:
                        data1 = bib_data.encode("latin-1", errors="ignore")
                    f.write(data1)

                # with open(file_path, "w") as f:
                #     pass  # Using 'pass' to indicate that we're not writing any content to the file
                # # with open(output_folder_path2 + "/" + file, "wb") as f:

                # add  '\importpackages{}' in begining
                data = '\\importpackages{}\n\graphicspath{ {./images/} }\n\n' + data
                with open(output_dir + "/" + file, "wb") as f:
                    logger.info(f"Created a new file: {file_path}")
                    try:
                        data1 = data.encode("utf-8")  # Ignore non-UTF-8 characters
                    except:
                        data1 = data.encode("latin-1", errors="ignore")
                    f.write(data1)
        except Exception as e:
            logger.error(f"Error in file {input_dir + '/' + file} : {e}")
            err_count += 1
        
        
        
    
    logger.info(f"--"*50)
    logger.info(f"Input dir: {input_dir}")
    logger.info(f"Total files: {len(files)}")
    logger.info(f"Error count: {err_count}")
    logger.info(f"__"*50)

def parallel_process(year, month):
    year_ = f'{year}' if year > 9 else f'0{year}'
    month_ = f'{year_}{month}' if month > 9 else f'{year_}0{month}'
    final_path = os.path.join(input_root_dir,f"20{year_}","preprocessing_1",month_)
    if os.path.exists(final_path):
        output_path = os.path.join(output_root_dir, str(year), month_)
        os.makedirs(output_path, exist_ok=True)
        process_data(final_path, output_path)

year = None
month = None
for year in reversed(range(24)):
    st_time = time()
    results = Parallel(n_jobs=8, verbose=2)(delayed(parallel_process)(year, month) for month in range(1,13))
    # print(results)
    logger.info(f"Time taken for year {year}: {time() - st_time}")
    logger.info(f"__"*50)
# parallel_process(0,1)


# results = Parallel(n_jobs=2, verbose=4)(delayed(process_data)(20, month) for month in range(1,13))
# print(results)
# results = Parallel(n_jobs=2, verbose=4)(delayed(process_data)(21, month) for month in range(1,13))
# print(results)
