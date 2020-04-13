from tkinter import Tk
from time import strftime, localtime
from os import stat, makedirs, path
from typing import List, Dict, Tuple
from shutil import move
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

total: int = len(fullSourceDirectory)

print(f"Found {total} files. Beginning cleanup process and outputting to:\n{destinationFolderName}")

count: int = 0

for currentFile in fullSourceDirectory:
    try:
        count += 1
        if count % 100 == 0:
            print(f"{count} out of {total}")
        fileName: str = currentFile.split("/")[-1]
        fileExtension: str = fileName.split(".")[-1]
        fileGroup: str = getFileTypeGroup(fileExtension)
        fileCreatedFloat: float = stat(currentFile).st_mtime
        localFileCreatedTime: Tuple = localtime(fileCreatedFloat)
        fileTimeData: Dict[str, str] = {
            "microsecond": strftime("%f", localFileCreatedTime),
            "second": strftime("%S", localFileCreatedTime),
            "minute": strftime("%M", localFileCreatedTime),
            "hour": strftime("%H", localFileCreatedTime),
            "day": strftime("%d", localFileCreatedTime),
            "monthNumber": strftime("%m", localFileCreatedTime),
            "month": strftime("%m-%B", localFileCreatedTime),
            "year": strftime("%Y", localFileCreatedTime)
        }

        newFilePath: str = f"{destinationFolderName}/{fileGroup}/{fileTimeData['year']}/{fileTimeData['month']}/{fileTimeData['day']}"
        isFileAlreadyCopied: bool = path.exists(f"{newFilePath}/{fileName}")
        newFileName: str = rename(fileName, currentFile, fileTimeData, isFileAlreadyCopied)
        makedirs(newFilePath, exist_ok=True)
        move(currentFile, f"{newFilePath}/{newFileName}")

    except:
        errorLogger.log()

errorLogger.stopCapturing()