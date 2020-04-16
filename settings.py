from typing import Dict, List
from enum import Enum
from json import load

__all__ = ["DOCUMENT_LOOKUP", "UNKNOWN_FOLDER_NAME", "RenameMethod", "DEFAULT_RENAME_METHOD"]

UNKNOWN_FOLDER_NAME: str = "unknown"

class RenameMethod(Enum):
    noModify: str = "no modify"
    tagDuplicate: str = "tag duplicate"
    date: str = "date"
    originalFullPath: str = "original full path"


DEFAULT_RENAME_METHOD = RenameMethod.tagDuplicate

# This is the automatically generated reverse of fileTypeMapping.json, so the program can go DOCUMENT_LOOKUP["png"] and get "pictures"
_SETTING_MAPPING: Dict[str, List[str]] = load(open("fileTypeMapping.json"))
DOCUMENT_LOOKUP: Dict[str, str] = {}
for group in _SETTING_MAPPING:
    for fileExtension in _SETTING_MAPPING[group]:
        DOCUMENT_LOOKUP[fileExtension] = group