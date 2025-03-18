import os
from PIL import Image

#Placeholder for now
def load_prompt_template(project_style: str):
    # Load a prompt template based on the project style
    template_path = os.path.join("resources", "prompts", project_style, "template.txt")
    with open(template_path, "r") as file:
        return file.read()

def save_image_locally(image: Image.Image):
    # Save the image locally and return the path
    image_path = os.path.join("output", "image.png")
    image.save(image_path)
    return image_path