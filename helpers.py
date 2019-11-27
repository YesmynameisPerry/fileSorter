from typing import Dict, List
from tkinter import filedialog
from os import walk
from settings import DOCUMENT_LOOKUP as DocumentTypes

__all__=["rename", "delay", "getFolderName", "getFullFolderContents", "getFileTypeGroup"]


usePauses: bool = False
useEnters: bool = False

def rename(fileName: str, fileNameData: Dict[str, str]) -> str:
    """
    Renames a file to whatever the user wants, depending on global variables
    """
    # TODO - provide different options for file renaming
    """
    don't change the filename (unless clash)
    append random string to end of filename (to avoid clash, or only do in event of clash)
    change file name to dd/mm/yyyy or something similar
    make filename equal full original path (replace '/' with '-' or similar)
    """
    return fileName

def delay(delay: int = 2) -> None:
    """
    Either sleeps for a default of 2 seconds, or waits for the use to press 'Enter', depending on global variables
    """
    if usePauses:
        sleep(delay)
    elif useEnters:
        input("Press 'Enter' to proceed")

def getFolderName(prompt: str) -> str:
    """
    Prompts the user to select a folder and doesn't let them progress until they do
    """
    print(prompt)
    delay()
    folderName: str = filedialog.askdirectory()

    while folderName == "":
        print()
        print("No folder chosen, please choose a folder.")
        delay()
        folderName: str = filedialog.askdirectory()
    
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

def getFileTypeGroup(fileExtension: str, default: str = "unknown") -> str:
    try:
        return DocumentTypes[fileExtension.lower()]
    except KeyError:
        return default