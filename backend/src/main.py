"""
Abby's main
"""

import sys
from pathlib import Path

# add project root directory to Python import path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import (
    prompts,
    styles,
    generation,
    image_generation,
    templates,
)
from src.services.file_service import file_service

app = FastAPI()

# Configure CORS to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://10.10.205.180:8080",
        "http://2.0.1.1:8080/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompts.router, prefix="/api/prompts", tags=["Prompts"])
app.include_router(generation.router, prefix="/api/generate", tags=["Generation"])
app.include_router(templates.router, prefix="/api", tags=["Templates"])

# Comment this out if no comfyui running
app.include_router(styles.router, prefix="/api/styles", tags=["Styles"])
app.include_router(image_generation.router, prefix="/api", tags=["Image Generation"])


# Clear image folders on startup
@app.on_event("startup")
def startup_event():
    print("Clearing image folders on startup...")
    file_service.clear_image_folders()
