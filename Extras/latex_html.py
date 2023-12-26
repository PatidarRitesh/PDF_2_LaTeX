import os
import subprocess
import random
import shutil
from tqdm import tqdm
from joblib import Parallel, delayed

def parellel_process(latex_dir, filename):
    # print(os.path.basename(filename))
    filename = filename[:-4]
    command = ['latexmlc',f'--dest=html_files_2/{filename}.html', f'{latex_dir}/{filename}.tex']
    try:
        result = subprocess.run(command, check=True, text=True, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        print(f"Successfully completed:{filename}")
    except subprocess.CalledProcessError as e:
        # Handle errors, if any
        print(f"Errorin {filename}:")
    
def Tex2HTML():
    # latexmlc --dest=somewhere/mydoc.html mydoc
    latex_dir = '/home/patidarritesh/Nougat/nougat/test_path'
    # html_files = '/home/patidarritesh/Nougat/nougat/html_files'
    Parallel(n_jobs=16, verbose=2)(delayed(parellel_process)(latex_dir, filename) for filename in tqdm(os.listdir(latex_dir)))


# def split():
#     count = 0
#     lst_latex = []
#     for year in range(2000, 2024):
#         year = str(year)
#         year_dir = os.path.join("/mnt/NFS/patidarritesh/PDF_2_TEX", year, "preprocessing_1")
#         for month_dir in os.listdir(year_dir):
#             # print(month_dir)
#             # input()
#             for file in os.listdir(os.path.join(year_dir, month_dir)):
#                 lst_latex.append((os.path.join(year_dir, month_dir, file)))
#         # print(lst_latex)
#     train_ratio = 0.8
#     test_ratio = 0.2
#     val_ratio = 0

#     all_files = lst_latex
#     random.shuffle(all_files)

#     train_path = ''
#     test_path = '/mnt/NFS/patidarritesh/test_path'
#     val_path = ''

#     # Calculate the split indices
#     train_split = int(train_ratio * len(all_files))
#     test_split = int((train_ratio + test_ratio) * len(all_files))

#     # Split the files into train, test, and validation sets
#     train_files = all_files[:train_split]
#     test_files = all_files[train_split:test_split]
#     val_files = all_files[test_split:]

#     # Copy files to the respective folders
#     # for filename in train_files:
#     #     shutil.copy(filename, os.path.join(train_path, filename))
#     # print(test_files[0])
#     # input()
#     for filename in tqdm(test_files):
#         testname = filename.split('/')[-1]
#         # input()
#         try:     
#             shutil.copy(filename, os.path.join(test_path, testname))
#             print(f"File '{filename}' copied to ,", os.path.join(test_path, testname))
#             count+=1
#         except:
#             print(f"Error in File '{filename}' copied to ,", os.path.join(test_path, filename))
            
#     print(count)
    # for filename in val_files:
    #     shutil.copy(filename, os.path.join(val_path, filename))


# split()
# print("ALL split successful")

Tex2HTML()