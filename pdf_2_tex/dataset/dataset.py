import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from functools import partial
import random
from typing import Dict, Tuple, Callable
from PIL import Image, UnidentifiedImageError
from typing import List, Optional
import pypdf
import orjson
import jsonlines     
import fitz  # PyMuPDF
from transformers.modeling_utils import PreTrainedModel

class pdf_2_tex_Dataset(Dataset):

    def __init__(self, 
                 dataset_path, 
                 pdf_2_tex_model: PreTrainedModel,
                 max_length: int,
                 split: str = "train",

 ):
        super().__init__()
        self.pdf_2_tex_model = pdf_2_tex_model
        self.max_length = max_length
        self.dataset_path = dataset_path
        self.split = split
        self.pdf_path = []
        self.latex_path = []    
        split_path = Path(dataset_path).parent / f"{split}.jsonl"
        with jsonlines.open(split_path) as reader:
            for line_number, line in enumerate(reader, start=1):
                self.pdf_path.append(line['pdf'])
                self.latex_path.append(line['latex'])
        self.dataset_length = line_number

    def __len__(self):
        return self.dataset_length

    def __getitem__(self, idx):

        pdf_path = self.pdf_path[idx]
        latex_path = self.latex_path[idx]

        input_tensor = self.pdf_2_tex_model.encoder.prepare_input(pdf_path, random_padding=True)

        with open(latex_path, "rb") as f:
            gnd_truth_data = f.read()
            try:
                gnd_truth_data = gnd_truth_data.decode("utf-8")  # Try decoding with UTF-8
            except:
                gnd_truth_data = gnd_truth_data.decode("latin-1", errors="ignore")  # Fallback to Latin-1, ignore errors

        
        tokenizer_out = self.pdf_2_tex_model.decoder.tokenizer(
            gnd_truth_data,
            max_length=self.max_length,
            padding="max_length",
            return_token_type_ids=False,
            truncation=True,
            return_tensors="pt",
        )
        input_ids = tokenizer_out["input_ids"].squeeze(0)
        attention_mask = tokenizer_out["attention_mask"].squeeze(0)
        """      
        # randomly perturb ground truth tokens
        if self.split == "train" and self.perturb:
            # check if we perturb tokens
            unpadded_length = attention_mask.sum()
            while random.random() < 0.1:
                try:
                    pos = random.randint(1, unpadded_length - 2)
                    token = random.randint(
                        23, len(self.pdf_2_tex_model.decoder.tokenizer) - 1
                    )
                    input_ids[pos] = token
                except ValueError:
                    break"""
        return input_tensor, input_ids, attention_mask