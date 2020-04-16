from typing import Dict, List, Tuple
from tkinter import filedialog
from os import walk, stat
from settings import *
from random import choice
from string import ascii_lowercase
try:
    from PIL import Image
except ImportError:
    print("PIL not found. EXIF data will not be used for image dates.\n")
    Image = None
from time import localtime, strptime, strftime
from sys import stdout

__all__ = ["rename", "getFolderName", "getFullFolderContents", "getFileTypeGroup", "getFileCreatedTime", "getFileTimeData"]

def rename(fileName: str, fullFilePath: str, fileTimeData: Dict[str, str], exists: bool, method: RenameMethod = DEFAULT_RENAME_METHOD) -> str:
    """
    Renames a file based on the chosen method
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

    if method == RenameMethod.originalFullPath:
        return fullFilePath.replace("/", ".")

    raise NotImplementedError(f"Given rename method {method} has no implementation")


def getFolderName(prompt: str) -> str:
    """
    Prompts the user to select a folder, exit the program if not
    """
    print(prompt)
    stdout.flush()
    folderName: str = filedialog.askdirectory(title=prompt)
    if folderName == "":
        print("No folder selected, exiting")
        exit(1)
    
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
    """
    Returns the type of file based on fileTypeMapping.json
    """
    try:
        return DOCUMENT_LOOKUP[fileExtension.lower()]
    except KeyError:
        return default

def getFileCreatedTime(filePath: str) -> Tuple:
    """
    Returns the best guess at the file's creation time, based on the metadata
    """
    try:
        # 36867 is the magical index of the 'date taken' exif tag, which is probably more accurate but only exists on image files
        imageDateString: str = Image.open(filePath)._getexif()[36867]
        if len(imageDateString) != 19:
            raise ValueError("Date string isn't in the format 'YYYY:MM:DD HH:MM:SS'")
        if imageDateString == '0000:00:00 00:00:00':
            raise ValueError("Date string is default values")
        return strptime(imageDateString, '%Y:%m:%d %H:%M:%S')
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        # for all files that fail to get the tag, just find the earliest known date for the file
        fileStats = stat(filePath)
        fileCreatedFloat: float = min(fileStats.st_mtime, fileStats.st_atime, fileStats.st_ctime)
        return localtime(fileCreatedFloat)

def getFileTimeData(fileTime) -> Dict[str, str]:
    """
    Returns a dict of dates to allow the final file path to be built
    """
    return {
        "day": strftime("%d", fileTime),
        "month": strftime("%m-%B", fileTime),
        "year": strftime("%Y", fileTime)
    }