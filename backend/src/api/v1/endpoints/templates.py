"""
Endpoint for generating templates
"""

from typing import Optional
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from src.services.file_service import file_service
from src.services.image_service import image_service

router = APIRouter()
router.description = (
    "Template Generation API, "
    "providing functions for retrieving templates from path and generating template images"
)


@router.get("/psd-templates/")
async def get_psd_templates():
    """List available PSD templates."""
    try:
        templates = file_service.fetch_psd_templates()
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


from typing import List

@router.post("/generate-template/")
async def generate_template(
    base_images: List[UploadFile] = File(...),
    template_image: Optional[UploadFile] = File(None),
    template_name: Optional[str] = Form(None),
):
    """
    Generate a list of composited template images and return as base64 strings.
    Accepts multiple base images and either a template image upload or a template name (from fetch_psd_templates).
    """
    try:
        # Get template image path
        if template_image:
            template_path = (
                f"/tmp/{template_image.filename}"
                if os.name != "nt"
                else os.path.join(os.environ.get("TEMP", "."), template_image.filename)
            )
            with open(template_path, "wb") as f:
                f.write(await template_image.read())
        elif template_name:
            templates = file_service.fetch_psd_templates()
            match = next(
                (
                    t
                    for t in templates
                    if t["name"] == template_name
                    or os.path.splitext(t["name"])[0] == template_name
                ),
                None,
            )
            if not match:
                raise HTTPException(status_code=404, detail="Template not found")
            template_path = match["path"]
        else:
            raise HTTPException(
                status_code=400, detail="No template image or name provided"
            )
        # Process all base images
        result_images = []
        for base_image in base_images:
            base_path = (
                f"/tmp/{base_image.filename}"
                if os.name != "nt"
                else os.path.join(os.environ.get("TEMP", "."), base_image.filename)
            )
            with open(base_path, "wb") as f:
                f.write(await base_image.read())
            img_b64 = image_service.layer_template_over_base(base_path, template_path)
            result_images.append({
                "imageBase64": img_b64,
                "filename": base_image.filename
            })
        return JSONResponse({"images": result_images})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}"
        ) from e
