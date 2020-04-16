from typing import Dict, List
from enum import Enum
__all__ = ["DOCUMENT_LOOKUP", "UNKNOWN_FOLDER_NAME", "RenameMethod", "DEFAULT_RENAME_METHOD"]

# File types (add new file extensions in lowercase here to map them to the correct folder)

UNKNOWN_FOLDER_NAME: str = "unknown"

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
        "odt",
        "txt",
        "rtf"
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
        "mkv",
        "mod"
    ],
    "audio": [
        "mp3",
        "wav",
        "ogg"
    ]
}

class RenameMethod(Enum):
    noModify: str = "no modify"
    tagDuplicate: str = "tag duplicate"
    date: str = "date"
    time: str = "time"
    dateTime: str = "date time"
    originalPath: str = "original path"


DEFAULT_RENAME_METHOD = RenameMethod.tagDuplicate

# This is the automatically generated reverse of the above, so the program can go DOCUMENT_LOOKUP["png"] and get "photos"

DOCUMENT_LOOKUP: Dict[str, str] = {}

for group in _SETTING_MAPPING:
    for fileExtension in _SETTING_MAPPING[group]:
        DOCUMENT_LOOKUP[fileExtension] = group