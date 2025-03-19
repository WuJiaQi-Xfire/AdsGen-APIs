import os
from PIL import Image

#Placeholder for now
def load_prompts(prompt_file):
    with open(prompt_file, "r") as file:
        return file.read()

def save_image_locally(image: Image.Image):
    # Save the image locally and return the path
    image_path = os.path.join("output", "image.png")
    image.save(image_path)
    return image_path