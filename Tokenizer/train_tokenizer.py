import os
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders
from tqdm import tqdm

if not os.path.exists("tokenizers"):
    os.makedirs("tokenizers")

root_path = "/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/DATA_2/"

tex_lst = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".tex"):
            tex_lst.append(os.path.join(root, file))
print("Length of tex files",len(tex_lst))

bbl_lst = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".bib"):
            bbl_lst.append(os.path.join(root, file))
print("length of bbl files",len(bbl_lst))

import random
# two_percent_tex_files = random.sample(tex_lst, int(0.02*len(tex_lst)))
# two_percent_bbl_files = random.sample(bbl_lst, int(0.02*len(bbl_lst)))

# print("Length of 2% tex files",len(two_percent_tex_files))
# print("Length of 2% bbl files",len(two_percent_bbl_files))



def train_latex_bpe_tokenizer(directory_path, percent=0.02, vocab_size=10000, tokenizer_output_path="tokenizers"):
    # Initialize a new tokenizer
    directory_path = random.sample(directory_path, int(percent*len(directory_path)))    
    print("Length of directory path",len(directory_path))
    tokenizer = Tokenizer(models.BPE())

    # Customize pre-tokenization and decoding options if needed
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()
    tokenizer.decoder = decoders.ByteLevel()

    # Create a list to store LaTeX corpus
    latex_corpus = []

    # Read LaTeX files from the specified directory
    for file_path in tqdm(directory_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as latex_file:
                    latex_text = latex_file.read()
                    latex_corpus.append(latex_text)
            except UnicodeDecodeError:
                # Fallback to 'latin-1' encoding if UTF-8 is not supported
                with open(file_path, 'r', encoding='latin-1') as latex_file:
                    latex_text = latex_file.read()
                    latex_corpus.append(latex_text)

    if not latex_corpus:
        print("No LaTeX files found in the directory.")
        return

    # Train the tokenizer on the LaTeX corpus with the specified vocab_size
    trainer = trainers.BpeTrainer(special_tokens=["[PAD]", "[CLS]", "[SEP]", "[MASK]", "[UNK]"], vocab_size=vocab_size)
    tokenizer.train_from_iterator(latex_corpus, trainer=trainer)

    # Save the trained tokenizer to a file
    tokenizer.save(f'{tokenizer_output_path}_{percent}_{vocab_size}.json')
    print(f"Tokenizer trained and saved to {tokenizer_output_path}_{percent}_{vocab_size}.json")

    return tokenizer

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--root_path", type=str, default="/mnt/NFS/patidarritesh/SID_DATA_PROCESSED/DATA_2/")
parser.add_argument("--percent", type=float, default=0.02)
parser.add_argument("--vocab", type=int, default=10000)
parser.add_argument("--tokenizer_output_path", type=str, default="tokenizers")
args = parser.parse_args()


directory_path = tex_lst + bbl_lst
tokenizer = train_latex_bpe_tokenizer(directory_path=directory_path, percent=args.percent, vocab_size=args.vocab, tokenizer_output_path=args.tokenizer_output_path)