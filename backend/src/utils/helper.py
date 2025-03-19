import re

def sanitize_filename(filename: str) -> str:
    sanitized_name = re.sub(r'[<>:"/\\|?*]', "_", filename)
    return sanitized_name[:255]  # Truncate to 255 characters
