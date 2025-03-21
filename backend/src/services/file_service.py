"""Module for file operations"""

import os
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


def read_lora_file():
    """Function to read Lora styles"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "styles", "loras_list.csv")
    df = pd.read_csv(template_path, header=None)
    styles = [{"id": row[0], "name": row[1]} for index, row in df.iterrows()]
    return styles


def read_art_file():
    """Function to read Art styles"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "styles", "game_art_styles.csv")
    df = pd.read_csv(template_path, header=None)
    styles = [{"id": row[0], "name": row[0]} for index, row in df.iterrows()]
    return styles


# Placeholder for now, TODO auto save with session_ID/image seed -> naming convention tbc
def save_image_locally(image: Image.Image):
    """Save the image locally and return the path"""
    image_path = os.path.join("output", "image.png")
    image.save(image_path)
    return image_path


def resize_and_save_image(image, save_path, width):
    """Function to save and display image thumbnail"""
    ratio = width / float(image.width)
    height = int(image.height * ratio)
    img = image.resize((width, height), Image.LANCZOS)
    img.save(save_path, format="PNG")
    return img
