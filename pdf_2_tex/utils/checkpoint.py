from typing import Optional
import requests
import os
import tqdm
import io
from pathlib import Path
import torch



MODEL_TAG = "0.0.1"
def torch_hub(model_tag: Optional[str] = MODEL_TAG) -> Path:
    old_path = Path(torch.hub.get_dir() + "/pdf_2_tex")
    if model_tag is None:
        model_tag = MODEL_TAG
    hub_path = old_path.with_name(f"pdf_2_tex-{model_tag}")
    if old_path.exists():
        # move to new format
        old_path.rename(old_path.with_name("pdf_2_tex-0.1.0"))
    return hub_path


def get_checkpoint(
    checkpoint_path: Optional[os.PathLike] = None,
    model_tag: str = MODEL_TAG,
    download: bool = True,
) -> Path:
    """
    Get the path to the Nougat model checkpoint.

    This function retrieves the path to the Nougat model checkpoint. If the checkpoint does not
    exist or is empty, it can optionally download the checkpoint.

    Args:
        checkpoint_path (Optional[os.PathLike]): The path to the checkpoint. If not provided,
            it will check the "NOUGAT_CHECKPOINT" environment variable or use the default location.
            Default is None.
        model_tag (str): The model tag to download. Default is "0.1.0-small".
        download (bool): Whether to download the checkpoint if it doesn't exist or is empty.
            Default is True.

    Returns:
        Path: The path to the Nougat model checkpoint.
    """
    checkpoint = Path(
        checkpoint_path or os.environ.get("pdf_2_tex_CHECKPOINT", torch_hub(model_tag))
    )
    if checkpoint.exists() and checkpoint.is_file():
        checkpoint = checkpoint.parent
    # if download and (not checkpoint.exists() or len(os.listdir(checkpoint)) < 5):
    #     checkpoint.mkdir(parents=True, exist_ok=True)
    #     download_checkpoint(checkpoint, model_tag=model_tag or MODEL_TAG)
    return checkpoint



if __name__ == "__main__":
    get_checkpoint()