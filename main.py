from tkinter import Tk
from os import makedirs, path
from shutil import move
from typing import Dict, Tuple, List
from helpers import *
from ErrorLogger import ErrorLogger
from sys import stdout

# SETUP

Tk = Tk()
Tk.withdraw()

# LOGIC

errorLogger: ErrorLogger = ErrorLogger(logErrors=True, resetFile=True)
errorLogger.startCapturing()

sourceFolderName: str = getFolderName("Select the source folder (The one containing unorganised files)")
destinationFolderName: str = getFolderName("Select the destination folder (The one that will contain organised files)")

print(f"\nMove all files from:\n{sourceFolderName}\nto:\n{destinationFolderName}")
if not yesNo():
    exit(0)

fullSourceDirectory: List[str] = getFullFolderContents(sourceFolderName)

total: int = len(fullSourceDirectory)

print(f"\nFound {total} files. Beginning sorting and moving to:\n{destinationFolderName}")

count: int = 0

for currentFile in fullSourceDirectory:
    try:
        count += 1
        if count % 100 == 0:
            print(f"{count} out of {total}")
            stdout.flush()
        fileName: str = currentFile.split("/")[-1]
        fileExtension: str = fileName.split(".")[-1]
        fileGroup: str = getFileTypeGroup(fileExtension)

        fileCreatedTime: Tuple = getFileCreatedTime(currentFile)
        fileTimeData: Dict[str, str] = getFileTimeData(fileCreatedTime)

        # To make it only break things up into months, just remove the `fileTimeData['day']` part.
        newFilePath: str = f"{destinationFolderName}/{fileGroup}/{fileTimeData['year']}/{fileTimeData['month']}/{fileTimeData['day']}"
        isFileAlreadyCopied: bool = path.exists(f"{newFilePath}/{fileName}")
        newFileName: str = rename(fileName, currentFile, fileTimeData, isFileAlreadyCopied)
        makedirs(newFilePath, exist_ok=True)
        move(currentFile, f"{newFilePath}/{newFileName}")

    except:
        errorLogger.log()

print(f"\nSuccessfully processed {total-errorLogger.getErrorCount()} files.")

errorLogger.stopCapturing()