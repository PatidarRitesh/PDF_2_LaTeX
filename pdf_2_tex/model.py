import logging
import math
import os
from typing import List, Optional, Union
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
import cv2
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import ImageOps
from timm.models.swin_transformer import SwinTransformer
from torchvision.transforms.functional import resize, rotate
from transformers import (
    PreTrainedTokenizerFast,
    StoppingCriteria,
    StoppingCriteriaList,
    
    MBartConfig,
    MBartForCausalLM,
)
from transformers.file_utils import ModelOutput
from transformers.modeling_utils import PretrainedConfig, PreTrainedModel
from nougat.postprocessing import postprocess
from nougat.transforms import train_transform, test_transform