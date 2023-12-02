# using above tokenizer find the number of tokens in each directory containing latex files and save it in a csv file
# Path: latex_token_count.py
import time
import os
from tokenizers import Tokenizer
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tokenizers import Tokenizer
import csv
import logging
import sys

# multiprocessing using joblib
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Pool

num_cores = multiprocessing.cpu_count()
root_dir = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/DATA/"
log_root_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/processed_data_level_2/"
if not os.path.exists(log_root_path):
    os.makedirs(log_root_path)


logging.basicConfig(level=logging.INFO, filename=f"{log_root_path}tc.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info(f"Number of cores: {num_cores}")


def latex_token_count(directory_path, yr, month):
    logging.basicConfig(level=logging.INFO, filename=f"{log_root_path}tc.log", filemode="a+", format="%(asctime)-15s %(name)-10s %(levelname)-8s %(message)s") 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if not os.path.exists(f"{log_root_path}tc_{yr}.csv"):
        with open(f"{log_root_path}tc_{yr}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(["Year", "file_name", "Token Count"])

    # return [0] if directory is empty or not exist
    if not os.path.exists(directory_path):
        logger.error(f"Directory does not exist. {directory_path}")
        return None

    # Read LaTeX files from the specified directory
    file_names = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(".tex")]
    latex_corpus = []
    tokenizer = Tokenizer.from_file("latex_bpe_tokenizer.json")
    # ______________________________________________________________________________________________
    # ########################### Read LaTeX files from the specified directory ####################
    print("Reading LaTeX files from yymm",yr,month)
    for file_path in file_names:
        try:
            with open(file_path, 'r', encoding='utf-8') as latex_file:
                latex_corpus.append(latex_file.read())
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as latex_file:
                latex_corpus.append(latex_file.read())

    if not latex_corpus:
        logger.error(f"No LaTeX files found in the directory. {directory_path}")
        # print("No LaTeX files found in the directory.", directory_path)
        return None

    st = time.time()
    logger.info(f"Encoding tokens for {directory_path} started.")
    # ______________________________________________________________________________________________
    # ########################## Tokenize the LaTeX corpus #########################################
    latex_corpus_tokenized = tokenizer.encode_batch(latex_corpus)
    del tokenizer
    logger.info(f"FILE: {directory_path} TIME: {(time.time() - st)/60} minutes, PAPERS: {len(latex_corpus_tokenized)}, TOTAL TOKENS: {sum([len(x.tokens) for x in latex_corpus_tokenized])}")
    logger.info(f"FILE: {directory_path}, Size of latex_corpus <untokenized> {sys.getsizeof(latex_corpus)}")
    logger.info(f"FILE: {directory_path}, Size of latex_corpus <tokenized>   {sys.getsizeof(latex_corpus_tokenized)}")
    del latex_corpus

    
    # ______________________________________________________________________________________________
    # ########################## Log the token size per paper to csv ###############################
    print("Writing to csv file.", yr, month)
    with open(f"{log_root_path}tc_{yr}.csv", "a") as f:
        writer = csv.writer(f)
        for file_path, latex_file in tqdm(zip(file_names, latex_corpus_tokenized)):
            writer.writerow([f'{yr}{month}', file_path, len(latex_file.tokens)])

    del latex_corpus_tokenized

# Define a function to process a single month's data
def process_month(year, month):
    year_ = f"0{year}" if year < 10 else f"{year}"
    i_ = f"0{month}" if month < 10 else f"{month}"
    dir_path = root_dir + f"{year}/{year_}{i_}"
    print(dir_path)
    if os.path.exists(dir_path):
        try:
            latex_token_count(dir_path, yr = year_, month = i_)
        except Exception as e:
            # add error to log file with the directory path
            logger.error(f"{dir_path} {e}")

# #------------------------------------------------------------------------------------------------------------------

# year = int(input("Enter year: "))
# add process names
# pool = Pool(processes=12)
# results = pool.starmap(process_month, [(year, month) for month in range(1,13)])

# use Parallel to run the process in parallel

# [[process_month(yr, month) for month in range(1,13)] for yr in range(24)]
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(16, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(17, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(18, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(19, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(20, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(21, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(22, month) for month in range(1,13))
results = Parallel(n_jobs=8, verbose=4)(delayed(process_month)(23, month) for month in range(1,13))