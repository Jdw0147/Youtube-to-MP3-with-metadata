import re

def safe_filename(name):
    # Remove invalid filename characters for Windows
    return re.sub(r'[\\/*?:"<>|]', "", name).strip() or "untitled"