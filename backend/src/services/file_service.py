"""Module for file operations"""

import os
from typing import List, Dict
import pandas as pd


class FileService:
    def __init__(self):
        # Find the project root (the folder containing 'backend')
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        self.psd_templates_dir = os.path.join(
            project_root, "backend", "src", "templates"
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


file_service = FileService()
