from tkinter import Tk
from time import strftime, localtime
from os import stat, makedirs
from typing import List, Dict
from shutil import copy2, move
from helpers import *
from ErrorLogger import ErrorLogger

# SETUP

Tk = Tk()
Tk.withdraw()

# LOGIC

errorLogger: ErrorLogger = ErrorLogger(logErrors=True, resetFile=True)
errorLogger.startCapturing()

sourceFolderName: str = getFolderName("Select the source folder (The one containing unorganised photos)")
destinationFolderName: str = getFolderName("Select the destination folder (The one that will contain organised photos)")

fullSourceDirectory: List[str] = getFullFolderContents(sourceFolderName)

print(f"Found {len(fullSourceDirectory)} files. Beginning cleanup process and outputting to:\n{destinationFolderName}")

for currentFile in fullSourceDirectory:
    try:
        fileName: str = currentFile.split("/")[-1]
        fileExtension: str = fileName.split(".")[-1]
        fileGroup: str = getFileTypeGroup(fileExtension)
        fileCreatedFloat: float = stat(currentFile).st_mtime
        fileTimeData: Dict[str, str] = {
            "day": strftime("%d", localtime(fileCreatedFloat)),
            "month": strftime("%m-%B", localtime(fileCreatedFloat)),
            "year": strftime("%Y", localtime(fileCreatedFloat))
        }

        newFileName: str = rename(fileName, fileTimeData)
        newFilePath: str = f"{destinationFolderName}/{fileGroup}/{fileTimeData['year']}/{fileTimeData['month']}"

        makedirs(newFilePath, exist_ok=True)
        move(currentFile, f"{newFilePath}/{newFileName}")

    except:
        errorLogger.log()

errorLogger.stopCapturing()