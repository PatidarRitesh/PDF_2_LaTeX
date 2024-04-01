# # using above tokenizer find the number of tokens in each directory containing latex files and save it in a csv file
# # Path: latex_token_count.py
# import time
# import os
# from tokenizers import Tokenizer
# from tqdm import tqdm
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# from tokenizers import Tokenizer
# import csv
# import logging
# import sys

# # multiprocessing using joblib
# from joblib import Parallel, delayed
# import multiprocessing
# from multiprocessing import Pool

# num_cores = multiprocessing.cpu_count()
# root_dir = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/DATA/"
# log_root_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/processed_data_level_2/"
# if not os.path.exists(log_root_path):
#     os.makedirs(log_root_path)


# logging.basicConfig(level=logging.INFO, filename=f"{log_root_path}tc.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.info(f"Number of cores: {num_cores}")


# def latex_token_count(directory_path, yr, month):
#     logging.basicConfig(level=logging.INFO, filename=f"{log_root_path}tc.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)

#     if not os.path.exists(f"{log_root_path}tc_{yr}.csv"):
#         with open(f"{log_root_path}tc_{yr}.csv", "a") as f:
#             writer = csv.writer(f)
#             writer.writerow(["Year", "file_name", "Token Count"])

#     # return [0] if directory is empty or not exist
#     if not os.path.exists(directory_path):
#         logger.error(f"Directory does not exist. {directory_path}")
#         return None

#     # Read LaTeX files from the specified directory
#     file_names = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(".tex")]
#     latex_corpus = []
#     tokenizer = Tokenizer.from_file("latex_bpe_tokenizer.json")
#     # ______________________________________________________________________________________________
#     # ########################### Read LaTeX files from the specified directory ####################
#     print("Reading LaTeX files from yymm",yr,month)
#     for file_path in file_names:
#         try:
#             with open(file_path, 'r', encoding='utf-8') as latex_file:
#                 latex_corpus.append(latex_file.read())
#         except UnicodeDecodeError:
#             with open(file_path, 'r', encoding='latin-1') as latex_file:
#                 latex_corpus.append(latex_file.read())

#     if not latex_corpus:
#         logger.error(f"No LaTeX files found in the directory. {directory_path}")
#         # print("No LaTeX files found in the directory.", directory_path)
#         return None

#     st = time.time()
#     logger.info(f"Encoding tokens for {directory_path} started.")
#     # ______________________________________________________________________________________________
#     # ########################## Tokenize the LaTeX corpus #########################################
#     latex_corpus_tokenized = tokenizer.encode_batch(latex_corpus)
#     del tokenizer
#     logger.info(f"FILE: {directory_path} TIME: {(time.time() - st)/60} minutes, PAPERS: {len(latex_corpus_tokenized)}, TOTAL TOKENS: {sum([len(x.tokens) for x in latex_corpus_tokenized])}")
#     logger.info(f"FILE: {directory_path}, Size of latex_corpus <untokenized> {sys.getsizeof(latex_corpus)}")
#     logger.info(f"FILE: {directory_path}, Size of latex_corpus <tokenized>   {sys.getsizeof(latex_corpus_tokenized)}")
#     del latex_corpus

    
#     # ______________________________________________________________________________________________
#     # ########################## Log the token size per paper to csv ###############################
#     print("Writing to csv file.", yr, month)
#     with open(f"{log_root_path}tc_{yr}.csv", "a") as f:
#         writer = csv.writer(f)
#         for file_path, latex_file in tqdm(zip(file_names, latex_corpus_tokenized)):
#             writer.writerow([f'{yr}{month}', file_path, len(latex_file.tokens)])

#     del latex_corpus_tokenized

# # Define a function to process a single month's data
# def process_month(year, month):
#     year_ = f"0{year}" if year < 10 else f"{year}"
#     i_ = f"0{month}" if month < 10 else f"{month}"
#     dir_path = root_dir + f"{year}/{year_}{i_}"
#     print(dir_path)
#     if os.path.exists(dir_path):
#         try:
#             latex_token_count(dir_path, yr = year_, month = i_)
#         except Exception as e:
#             # add error to log file with the directory path
#             logger.error(f"{dir_path} {e}")

# # #------------------------------------------------------------------------------------------------------------------

# # year = int(input("Enter year: "))
# # add process names
# # pool = Pool(processes=12)
# # results = pool.starmap(process_month, [(year, month) for month in range(1,13)])

# # use Parallel to run the process in parallel

# # [[process_month(yr, month) for month in range(1,13)] for yr in range(24)]
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(16, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(17, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(18, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(19, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(20, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(21, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(22, month) for month in range(1,13))
# results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(23, month) for month in range(1,13))




# # using above tokenizer find the number of tokens in each directory containing latex files and save it in a csv file
# # Path: latex_token_count.py
# import time
# import os
# from tokenizers import Tokenizer
# from tqdm import tqdm
# import pandas as pd
# from tokenizers import Tokenizer
# import csv
# import logging
# import sys
# from transformers import AutoTokenizer
# tokenizer_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/tokenizers/tokenizers/hf_tokenizer_1.0%_30000_new"
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})


# directory_path = "/mnt/NFS/patidarritesh/preprocess_2/latex_file_10_page"


# # Read LaTeX files from the specified directory
# file_names = []
# for filename in os.listdir(directory_path):
#     if filename.endswith(".tex"):
#         file_names.append(os.path.join(directory_path, filename))

# # sample of 3 file_names
# print("--------------------------")

# latex_corpus = []
# # ______________________________________________________________________________________________
# # ########################### Read LaTeX files from the specified directory ####################
# for file_path in file_names:
#     try:
#         with open(file_path, 'r', encoding='utf-8') as latex_file:
#             latex_corpus.append(latex_file.read())
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as latex_file:
#             latex_corpus.append(latex_file.read())

# if not latex_corpus:
#     print(f"No LaTeX files found in the directory. {directory_path}")
#     # print("No LaTeX files found in the directory.", directory_path)

# st = time.time()
# print(f"Encoding tokens for {directory_path} started.")
# # ______________________________________________________________________________________________
# # ########################## Tokenize the LaTeX corpus #########################################
# latex_corpus_tokenized = []
# for latex in tqdm(latex_corpus):
#     print(latex)
#     latex_corpus_tokenized.append(tokenizer.encode_plus(latex,truncation=False))

# print(f"FILE: {directory_path} TIME: {(time.time() - st)/60} minutes, PAPERS: {len(latex_corpus_tokenized)}, TOTAL TOKENS: {sum([len(x) for x in latex_corpus_tokenized])}")
# for file_name, tokens in tqdm(zip(file_names, latex_corpus_tokenized)):
#     print(f"{file_name}: {len(tokens)}")






# # # __________________________________________ Ritesh version 1 ______________________________________________________
# import time
# import os
# import pandas as pd
# from tqdm import tqdm
# from transformers import AutoTokenizer

# # Specify the path to the tokenizer
# # tokenizer_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/tokenizers/tokenizers/hf_tokenizer_1.0%_30000_new"
# # tokenizer_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/tokenizers/tokenizers/hf_tokenizer_4.0%_50000_new"
# # tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer"
# tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer_30k"

# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer.add_special_tokens({'unk_token': '[UNK]'})

# # Specify the directory containing LaTeX files
# directory_path = "/mnt/NFS/patidarritesh/preprocess_2/latex_file_10_page"

# # Read LaTeX files from the specified directory
# file_names = [filename for filename in os.listdir(directory_path) if filename.endswith(".tex")]

# # Initialize lists to store results
# file_names_list = []
# num_tokens_list = []

# # Tokenize the LaTeX content and count tokens for each file
# for file_name in tqdm(file_names):
#     file_path = os.path.join(directory_path, file_name)

#     try:
#         with open(file_path, 'r', encoding='utf-8') as latex_file:
#             latex_content = latex_file.read()
#             tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#             num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor

#             # Append results to lists
#             file_names_list.append(file_name)
#             num_tokens_list.append(num_tokens)

#     except UnicodeDecodeError:
#         print(f"UnicodeDecodeError: Skipping file {file_name}")

# # Create a DataFrame from the lists
# result_df = pd.DataFrame({'File Name': file_names_list, 'Num Tokens': num_tokens_list})

# # Save the results to a CSV file
# csv_output_path = "/mnt/NFS/patidarritesh/preprocess_2/token_counts.csv"
# result_df.to_csv(csv_output_path, index=False)

# print(f"Token counts saved to {csv_output_path}")


### __________________________________________ Ritesh version 2 ______________________________________________________

# import os
# import json
# import shutil
# import pandas as pd
# from tqdm import tqdm
# from transformers import AutoTokenizer

# json_file_path = "/mnt/NFS/patidarritesh/preprocess_2/pdf_files.json"
# latex_root_file = "/mnt/NFS/patidarritesh/preprocess_2"

# # Read the JSON file
# with open(json_file_path, "r") as json_file:
#     data = json.load(json_file)

# # Get the list of PDF files from the JSON data
# pdf_files = sorted(data.get("pdf_files", []))

# # Specify the path to the tokenizer
# tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer_30k"
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer.add_special_tokens({'unk_token': '[UNK]'})

# # Initialize lists to store results
# file_names_list = []
# num_tokens_list = []

# # Tokenize the LaTeX content and count tokens for each file
# for pdf_file in tqdm(pdf_files):
#     # Assuming the LaTeX file has the same base name but with a ".tex" extension
#     latex_file_name = os.path.splitext(pdf_file)[0] + ".tex"
#     folders = latex_file_name[:2]

#     folder_path = os.path.join(latex_root_file, folders)

#     for folder in os.listdir(folder_path):
#         month = latex_file_name[:4]
#         if folder == month:
#             latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#             try:
#                 with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                     latex_content = latex_file.read()
#                     tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                     num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor

#                     # Append results to lists
#                     file_names_list.append(latex_file_path)
#                     num_tokens_list.append(num_tokens)

#             except UnicodeDecodeError:
#                 print(f"UnicodeDecodeError: Skipping file {latex_file_path}")

# # Create a DataFrame from the lists
# result_df = pd.DataFrame({'File Name': file_names_list, 'Num Tokens': num_tokens_list})

# # Save the results to a CSV file
# csv_output_path = "/mnt/NFS/patidarritesh/preprocess_2/token_counts_demo.csv"
# result_df.to_csv(csv_output_path, index=False)

# print(f"Token counts saved to {csv_output_path}")







# # __________________________________________ Ritesh version 3 ______________________________________________________

# import os
# import json
# import pandas as pd
# from tqdm import tqdm
# from transformers import AutoTokenizer

# json_file_path = "/mnt/NFS/patidarritesh/preprocess_2/pdf_files.json"
# latex_root_file = "/mnt/NFS/patidarritesh/preprocess_2"
# output_json_error_path = "/mnt/NFS/patidarritesh/preprocess_2/missing_latex_files.json"

# # Read the JSON file
# with open(json_file_path, "r") as json_file:
#     data = json.load(json_file)

# # Get the list of PDF files from the JSON data
# pdf_files = sorted(data.get("pdf_files", []))

# # Specify the path to the tokenizer
# tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer_30k"
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer.add_special_tokens({'unk_token': '[UNK]'})

# # Initialize lists to store results
# file_names_list = []
# num_tokens_list = []
# missing_latex_files = []

# # Tokenize the LaTeX content and count tokens for each file
# for pdf_file in tqdm(pdf_files):
#     # Assuming the LaTeX file has the same base name but with a ".tex" extension
#     latex_file_name = os.path.splitext(pdf_file)[0] + ".tex"
#     folders = latex_file_name[:2]

#     folder_path = os.path.join(latex_root_file, folders)

#     for folder in os.listdir(folder_path):
#         month = latex_file_name[:4]
#         if folder == month:
#             latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#             try:
#                 with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                     latex_content = latex_file.read()
#                     tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                     num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor

#                     # Append results to lists
#                     file_names_list.append(os.path.basename(latex_file_path))  # Get only the file name
#                     num_tokens_list.append(num_tokens)

#             except FileNotFoundError:
#                 print(f"FileNotFoundError: Skipping file {latex_file_path}")
#                 missing_latex_files.append(pdf_file)

# # Create a DataFrame from the lists
# result_df = pd.DataFrame({'File Name': file_names_list, 'Num Tokens': num_tokens_list})

# # Save the results to a CSV file
# csv_output_path = "/mnt/NFS/patidarritesh/preprocess_2/token_counts_demo2.csv"
# result_df.to_csv(csv_output_path, index=False)

# # Save the list of PDF files with missing LaTeX files to a JSON file
# with open(output_json_error_path, 'w') as json_error_file:
#     json.dump({"missing_latex_files": missing_latex_files}, json_error_file, indent=2)

# print(f"Token counts saved to {csv_output_path}")
# print(f"List of PDF files with missing LaTeX files saved to {output_json_error_path}")



# # __________________________________________ Ritesh version 4 Parallel ______________________________________________________



# import os
# os.environ["TOKENIZERS_PARALLELISM"] = "true"
# import json
# import re
# import pandas as pd
# from tqdm import tqdm
# from transformers import AutoTokenizer
# from joblib import Parallel, delayed

# def process_latex_file(pdf_file, latex_root_file, tokenizer):
#     latex_file_name = os.path.splitext(pdf_file)[0] + ".tex"
#     pattern = r"\d{4}\.\d{5}"

#     if re.search(pattern, latex_file_name):
#         folders = latex_file_name[:2]
#         folder_path = os.path.join(latex_root_file, folders)

#         for folder in os.listdir(folder_path):
#             month = latex_file_name[:4]
#             if folder == month:
#                 latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#                 try:
#                     with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                         latex_content = latex_file.read()
#                         tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                         num_tokens = tokens['input_ids'].shape[1]

#                         return {'File Name': os.path.basename(latex_file_path), 'Num Tokens': num_tokens}

#                 except FileNotFoundError:
#                     return {'File Name': os.path.basename(pdf_file), 'Num Tokens': 0}  # Return file name if not found

#     else:
#         folders = latex_file_name[-10:-9]
#         folder_path = os.path.join(latex_root_file, folders)

#         for folder in os.listdir(folder_path):
#             month = latex_file_name[-11:-7]
#             if folder == month:
#                 latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#                 try:
#                     with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                         latex_content = latex_file.read()
#                         tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                         num_tokens = tokens['input_ids'].shape[1]

#                         return {'File Name': os.path.basename(latex_file_path), 'Num Tokens': num_tokens}

#                 except FileNotFoundError:
#                     return {'File Name': os.path.basename(pdf_file), 'Num Tokens': 0}  # Return file name if not found

#     return None

# def process_pdf_files(pdf_files, latex_root_file, tokenizer):
#     results = Parallel(n_jobs=8, verbose=2)(
#         delayed(process_latex_file)(pdf_file, latex_root_file, tokenizer) for pdf_file in tqdm(pdf_files)
#     )

#     # Create a DataFrame from the results
#     result_df = pd.DataFrame(results)

#     return result_df

# if __name__ == "__main__":
#     json_file_path = "/mnt/NFS/patidarritesh/preprocess_2/pdf_names.json"
#     latex_root_file = "/mnt/NFS/patidarritesh/preprocess_2"
#     output_json_error_path = "/mnt/NFS/patidarritesh/preprocess_2/missing_latex_files.json"
#     tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer_30k"

#     # Read the JSON file
#     with open(json_file_path, "r") as json_file:
#         data = json.load(json_file)

#     # Get the list of PDF files from the JSON data
#     pdf_files = sorted(data.get("pdf_files", []))

#     # Specify the path to the tokenizer
#     tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
#     tokenizer.add_special_tokens({'pad_token': '[PAD]'})
#     tokenizer.add_special_tokens({'unk_token': '[UNK]'})

#     # Process PDF files using parallel processing
#     result_df = process_pdf_files(pdf_files, latex_root_file, tokenizer)

#     # Save the results to a CSV file
#     csv_output_path = "/mnt/NFS/patidarritesh/preprocess_2/token_counts.csv"
#     result_df.to_csv(csv_output_path, index=False)

#     # Identify missing LaTeX files
#     # missing_latex_files = result_df[result_df['Num Tokens'] == 0]['File Name'].tolist()

#     # # Save the list of PDF files with missing LaTeX files to a JSON file
#     # with open(output_json_error_path, 'w') as json_error_file:
#     #     json.dump({"missing_latex_files": missing_latex_files}, json_error_file, indent=2)

#     print(f"Token counts saved to {csv_output_path}")
#     # print(f"List of PDF files with missing LaTeX files saved to {output_json_error_path}")



# # __________________________________________ Ritesh version 5 ______________________________________________________

# import os
# import json
# import re
# import pandas as pd
# from tqdm import tqdm
# from transformers import AutoTokenizer

# json_file_path = "/mnt/NFS/patidarritesh/preprocess_2/pdf_name_5_page.json"
# latex_root_file = "/mnt/NFS/patidarritesh/preprocess_2"
# output_json_error_path = "/mnt/NFS/patidarritesh/preprocess_2/missing_latex_files_5_page.json"
# pattern = r"\d{4}\.\d{5}"
# pattern2 = r"\d{4}\.\d{4}"
# # Read the JSON file
# with open(json_file_path, "r") as json_file:
#     data = json.load(json_file)

# # Get the list of PDF files from the JSON data
# pdf_files = sorted(data.get("pdf_files", []))

# # Specify the path to the tokenizer
# tokenizer_path = "/mnt/NFS/patidarritesh/preprocess_2/tokenizer_30k"
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer.add_special_tokens({'unk_token': '[UNK]'})

# # Initialize lists to store results
# file_names_list = []
# num_tokens_list = []
# missing_latex_files = []

# # Tokenize the LaTeX content and count tokens for each file
# for pdf_file in tqdm(pdf_files):
#     # Assuming the LaTeX file has the same base name but with a ".tex" extension
#     latex_file_name = os.path.splitext(pdf_file)[0] + ".tex"
#     if re.search(pattern, latex_file_name): 
        
#         folders = latex_file_name[:2]

#         folder_path = os.path.join(latex_root_file, folders)

#         for folder in os.listdir(folder_path):
#             month = latex_file_name[:4]
#             if folder == month:
#                 latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#                 try:
#                     with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                         latex_content = latex_file.read()
#                         tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                         num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor

#                         # Append results to lists
#                         file_names_list.append(os.path.basename(latex_file_path))  # Get only the file name
#                         num_tokens_list.append(num_tokens)

#                 except FileNotFoundError:
#                     print(f"FileNotFoundError: Skipping file {latex_file_path}")
#                     missing_latex_files.append(pdf_file)

#     else:
    
#         folders = latex_file_name[-10:-9]
        

#         folder_path = os.path.join(latex_root_file, folders)

#         for folder in os.listdir(folder_path):
#             month = latex_file_name[-11:-7]
#             if folder == month:
#                 latex_file_path = os.path.join(folder_path, folder, latex_file_name)

#                 try:
#                     with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
#                         latex_content = latex_file.read()
#                         tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
#                         num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor

#                         # Append results to lists
#                         file_names_list.append(os.path.basename(latex_file_path))  # Get only the file name
#                         num_tokens_list.append(num_tokens)

#                 except FileNotFoundError:
#                     print(f"FileNotFoundError: Skipping file {latex_file_path}")
#                     missing_latex_files.append(pdf_file)

# # Create a DataFrame from the lists
# result_df = pd.DataFrame({'File Name': file_names_list, 'Num Tokens': num_tokens_list})

# # Save the results to a CSV file
# csv_output_path = "/mnt/NFS/patidarritesh/preprocess_2/token_counts_5_page.csv"
# result_df.to_csv(csv_output_path, index=False)

# # Save the list of PDF files with missing LaTeX files to a JSON file
# with open(output_json_error_path, 'w') as json_error_file:
#     json.dump({"missing_latex_files": missing_latex_files}, json_error_file, indent=2)

# print(f"Token counts saved to {csv_output_path}")
# print(f"List of PDF files with missing LaTeX files saved to {output_json_error_path}")


# # __________________________________________ Ritesh version 6 ______________________________________________________

import os
import json
from tqdm import tqdm
import pandas as pd
from transformers import AutoTokenizer
import re

def process_latex_file(latex_file_path, tokenizer):
    try:
        with open(latex_file_path, 'r', encoding='utf-8') as latex_file:
            latex_content = latex_file.read()
            tokens = tokenizer.encode_plus(latex_content, truncation=False, return_tensors='pt')
            num_tokens = tokens['input_ids'].shape[1]  # Get the number of tokens from the tensor
            return os.path.basename(latex_file_path), num_tokens
    except FileNotFoundError:
        print(f"FileNotFoundError: Skipping file {latex_file_path}")
        return None

def main():
    json_file_path = "/mnt/HDFS/patidarritesh/preprocess_2/pdf_name_4_page.json"
    latex_root_file = "/mnt/HDFS/patidarritesh/preprocess_2"
    output_json_error_path = "/mnt/HDFS/patidarritesh/preprocess_2/missing_latex_files_4_page.json"
    pattern = r"\d{4}\.\d{5}"
    pattern2 = r"\d{4}\.\d{4}"

    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    pdf_files = sorted(data.get("pdf_files", []))

    tokenizer_path = "/mnt/HDFS/patidarritesh/preprocess_2/tokenizer_30k"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenizer.add_special_tokens({'unk_token': '[UNK]'})

    file_names_list = []
    num_tokens_list = []
    missing_latex_files = []

    for pdf_file in tqdm(pdf_files):
        latex_file_name = os.path.splitext(pdf_file)[0] + ".tex"

        if re.search(pattern, latex_file_name):
            folders = latex_file_name[:2]
        elif re.search(pattern2, latex_file_name):
            folders = str(int(latex_file_name[:2]))
        else:
            folders = latex_file_name[-10:-9]

        folder_path = os.path.join(latex_root_file, folders)

        for folder in os.listdir(folder_path):
            month = latex_file_name[:4] if re.search(pattern, latex_file_name) or re.search(pattern2,latex_file_name) else latex_file_name[-11:-7]
            if folder == month:
                latex_file_path = os.path.join(folder_path, folder, latex_file_name)
                result = process_latex_file(latex_file_path, tokenizer)
                if result:
                    file_names_list.append(result[0])
                    num_tokens_list.append(result[1])

    result_df = pd.DataFrame({'File Name': file_names_list, 'Num Tokens': num_tokens_list})
    csv_output_path = "/mnt/HDFS/patidarritesh/preprocess_2/token_counts_4_page.csv"
    result_df.to_csv(csv_output_path, index=False)

    with open(output_json_error_path, 'w') as json_error_file:
        json.dump({"missing_latex_files": missing_latex_files}, json_error_file, indent=2)

    print(f"Token counts saved to {csv_output_path}")
    print(f"List of PDF files with missing LaTeX files saved to {output_json_error_path}")

if __name__ == "__main__":
    main()
