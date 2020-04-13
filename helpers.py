from typing import Dict, List
from tkinter import filedialog
from os import walk
from settings import *
from random import choice
from string import ascii_lowercase

__all__ = ["rename", "getFolderName", "getFullFolderContents", "getFileTypeGroup"]

def rename(fileName: str, fullFilePath: str,fileTimeData: Dict[str, str], exists: bool, method: RenameMethod = DEFAULT_RENAME_METHOD) -> str:
    """
    Renames a file to whatever the user wants, depending on global variables
    """
    if method not in RenameMethod:
        raise ValueError(f"Given rename method {method} is not a valid member of the class RenameMethod")

    if method == RenameMethod.noModify:
        return fileName

    fileNameParts: List[str] = fileName.split(".")
    originalName: str = ".".join(fileNameParts[:-1])
    fileType: str = "." + fileNameParts[-1]

    if method == RenameMethod.tagDuplicate:
        randomString: str = ''.join(choice(ascii_lowercase) for _ in range(5))
        return f"{originalName}-DUPLICATE-{randomString}{fileType}" if exists else fileName

    if method == RenameMethod.date:
        return f"{fileTimeData['year']}-{fileTimeData['monthNumber']}-{fileTimeData['day']}_{fileName}"

    if method == RenameMethod.time:
        return f"{fileTimeData['hour']}-{fileTimeData['minute']}-{fileTimeData['second']}_{fileName}"

    if method == RenameMethod.dateTime:
        return f"{fileTimeData['year']}-{fileTimeData['monthNumber']}-{fileTimeData['day']}_{fileTimeData['hour']}-{fileTimeData['minute']}-{fileTimeData['second']}_{fileName}"

    if method == RenameMethod.originalPath:
        return fullFilePath.replace("/", ".")

    raise NotImplementedError(f"Given rename method {method} has no implementation")


def getFolderName(prompt: str) -> str:
    """
    Prompts the user to select a folder and doesn't let them progress until they do
    """
    print(prompt)
    folderName: str = filedialog.askdirectory(title=prompt)

    while folderName == "":
        print()
        print("No folder chosen, please choose a folder.")
        folderName: str = filedialog.askdirectory(title=prompt)
    
    return folderName

def getFullFolderContents(directoryPath: str) -> List[str]:
    """
    Walks the given directory and returns a list of all files in the directory and all subdirectories
    """
    output: List[str] = []
    for fileTuple in walk(directoryPath):
        for fileName in fileTuple[2]:
            output += [(fileTuple[0].replace("\\", "/")+"/"+fileName)]
    return output

def getFileTypeGroup(fileExtension: str, default: str = UNKNOWN_FOLDER_NAME) -> str:
    try:
        return DOCUMENT_LOOKUP[fileExtension.lower()]
    except KeyError:
        return default