import re

# Remove invalid filename characters for Windows
def safe_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip()