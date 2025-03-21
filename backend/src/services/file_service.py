import os
from PIL import Image


def load_prompt_from_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError:
        raise Exception(f"The file at {file_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")


# Placeholder for now, TODO auto save with session_ID/image seed -> naming convention tbc
def save_image_locally(image: Image.Image):
    # Save the image locally and return the path
    image_path = os.path.join("output", "image.png")
    image.save(image_path)
    return image_path
