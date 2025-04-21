"""Module for file operations"""

import base64
import os
from typing import List, Dict
import pandas as pd


class FileService:
    def __init__(self):
        self.file_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\base_image"
        self.preview_path = (
            r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\resized_image"
        )
        self.psd_templates_dir = (
            r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\backend\src\templates"
        )

    def fetch_psd_templates(self):
        """List all PSD files in the templates directory."""
        psd_files = []
        for fname in os.listdir(self.psd_templates_dir):
            if fname.lower().endswith(".png"):
                psd_files.append(
                    {"name": fname, "path": os.path.join(self.psd_templates_dir, fname)}
                )
        return psd_files

    def load_prompt_from_file(self, file_path: str) -> str:
        """Load prompt from file"""
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

    def read_art_file(self) -> List[Dict[str, str]]:
        """Read art styles from CSV"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        template_path = os.path.join(base_dir, "styles", "game_art_styles.csv")
        df = pd.read_csv(template_path, header=None)
        return [
            {"id": row[0], "name": row[0], "styleType": "art"}
            for index, row in df.iterrows()
        ]

    def get_generated_images(self) -> List[Dict[str, str]]:
        """Get generated images as base64 strings"""
        images = []
        try:
            image_files = [
                f for f in os.listdir(self.file_path) if f.lower().endswith((".png"))
            ]
            for image_file in image_files:
                new_path = os.path.join(self.file_path, image_file)
                with open(new_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode("utf-8")
                    images.append(
                        {
                            "filename": image_file,
                            "data": f"data:image/png;base64,{img_data}",
                        }
                    )
            return images
        except Exception as e:
            print(f"Error loading generated images: {str(e)}")
            return []

    def clear_image_folders(self):
        """Clear all images from output folders"""
        os.makedirs(self.file_path, exist_ok=True)
        os.makedirs(self.preview_path, exist_ok=True)

        try:
            for folder in [self.file_path, self.preview_path]:
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            print("Successfully cleared image folders")
        except Exception as e:
            print(f"Error clearing image folders: {str(e)}")


file_service = FileService()
