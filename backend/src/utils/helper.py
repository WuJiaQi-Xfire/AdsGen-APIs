import re

def sanitize_filename(filename: str) -> str:
    sanitized_name = re.sub(r'[<>:"/\\|?*]', "_", filename)
    return sanitized_name[:255]  # Truncate to 255 characters

def validate_image_format(format: str) -> bool:
    allowed_formats = {"PNG", "JPEG", "WEBP", "GIF"}
    return format.upper() in allowed_formats