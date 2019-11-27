from typing import Dict, List
__all__ = ["DOCUMENT_LOOKUP"]

# File types (add new file extensions in lowercase here to map them to the correct folder)

_SETTING_MAPPING: Dict[str, List[str]] = {
    "documents": [
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "pdf",
        "csv",
        "odt"
    ],
    "photos": [
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "gif"
    ],
    "videos": [
        "mov",
        "mp4",
        "m4a",
        "flv",
        "avi",
        "wmv",
        "mkv"
    ]
}

# This is the reverse of the above, so the program can go DOCUMENT_LOOKUP["png"] and get "photos"

DOCUMENT_LOOKUP: Dict[str, str] = {}

for group in _SETTING_MAPPING:
    for fileExtension in _SETTING_MAPPING[group]:
        DOCUMENT_LOOKUP[fileExtension] = group