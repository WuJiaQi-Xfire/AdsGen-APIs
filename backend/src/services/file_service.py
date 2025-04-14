"""Module for file operations"""

import os
import base64
import pandas as pd

file_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\base_image"
preview_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\resized_image"


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


def get_generated_images():
    """Load all images from the base_image folder and convert them to base64 strings."""
    images = []
    try:
        image_files = [f for f in os.listdir(file_path) if f.lower().endswith((".png"))]
        for image_file in image_files:
            new_path = os.path.join(file_path, image_file)
            with open(new_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode("utf-8")
                image_obj = {
                    "filename": image_file,
                    "data": f"data:image/png;base64,{img_data}",
                }
                images.append(image_obj)

        return images
    except Exception as e:
        print(f"Error loading generated images: {str(e)}")
        return []


def clear_image_folders():
    """Clear all images from the base_image and resized_image folders."""
    os.makedirs(file_path, exist_ok=True)
    os.makedirs(preview_path, exist_ok=True)

    try:
        for file in os.listdir(file_path):
            file_path_to_remove = os.path.join(file_path, file)
            if os.path.isfile(file_path_to_remove):
                os.remove(file_path_to_remove)

        for file in os.listdir(preview_path):
            file_path_to_remove = os.path.join(preview_path, file)
            if os.path.isfile(file_path_to_remove):
                os.remove(file_path_to_remove)

        print("Successfully cleared image folders")
    except Exception as e:
        print(f"Error clearing image folders: {str(e)}")
