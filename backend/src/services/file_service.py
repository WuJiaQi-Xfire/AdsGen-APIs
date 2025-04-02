"""Module for file operations"""

import os
import base64
import pandas as pd
from PIL import Image


def load_prompt_from_file(file_path: str) -> str:
    """Function to load prompt files"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError as e:
        raise Exception(f"The file at {file_path} was not found.") from e
    except Exception as e:
        raise Exception(
            f"Unable to load the file at {file_path} due to : {str(e)}"
        ) from e


def read_art_file():
    """Function to read Art styles"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "styles", "game_art_styles.csv")
    df = pd.read_csv(template_path, header=None)
    styles = [
        {"id": row[0], "name": row[0], "styleType": "art"}
        for index, row in df.iterrows()
    ]
    return styles


def sanitize_filename(filename: str) -> str:
    """Replace invalid characters in filenames"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename.strip()


def file_name(prompt_name, style_name, seed):
    """Save the image locally and return the path"""
    prompt_name = sanitize_filename(prompt_name)
    style_name = sanitize_filename(style_name)
    output_folder = f"{prompt_name}_output"
    os.makedirs(output_folder, exist_ok=True)
    style_folder = os.path.join(output_folder, style_name)
    os.makedirs(style_folder, exist_ok=True)
    image_path = os.path.join(style_folder, f"{seed}.png")
    return image_path
