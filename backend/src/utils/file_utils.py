"""File utlity functions"""


def sanitize_filename(filename: str) -> str:
    """Replace invalid characters in filenames"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename.strip()
