from tkinter import Tk
from time import strftime, localtime, strptime
from os import stat, makedirs, path
from typing import List, Dict, Tuple
from shutil import move
from helpers import *
from ErrorLogger import ErrorLogger
from PIL import Image
from sys import stdout

# SETUP

Tk = Tk()
Tk.withdraw()

# LOGIC

# TODO - cli

errorLogger: ErrorLogger = ErrorLogger(logErrors=True, resetFile=True)
errorLogger.startCapturing()

sourceFolderName: str = getFolderName("Select the source folder (The one containing unorganised photos)")
destinationFolderName: str = getFolderName("Select the destination folder (The one that will contain organised photos)")

print(sourceFolderName)

fullSourceDirectory: List[str] = getFullFolderContents(sourceFolderName)

total: int = len(fullSourceDirectory)

print(f"Found {total} files. Beginning cleanup process and outputting to:\n{destinationFolderName}")

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

        FileCreatedTime: Tuple = ()
        try:
            # 36867 is the index of the 'date taken' tag, which is more accurate but only exists on image files
            imageDateString: str = Image.open(currentFile)._getexif()[36867]
            if len(imageDateString) != 19:
                raise ValueError("Date string isn't in the format 'YYYY:MM:DD HH:MM:SS'")
            if imageDateString == '0000:00:00 00:00:00':
                raise ValueError("Date string is default values")
            FileCreatedTime = strptime(imageDateString, '%Y:%m:%d %H:%M:%S')
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            # for all files that fail to get the tag, just find the earliest known date for the file
            fileStats = stat(currentFile)
            fileCreatedFloat: float = min(fileStats.st_mtime, fileStats.st_atime, fileStats.st_ctime)
            FileCreatedTime: Tuple = localtime(fileCreatedFloat)

        fileTimeData: Dict[str, str] = {
            "second": strftime("%S", FileCreatedTime),
            "minute": strftime("%M", FileCreatedTime),
            "hour": strftime("%H", FileCreatedTime),
            "day": strftime("%d", FileCreatedTime),
            "monthNumber": strftime("%m", FileCreatedTime),
            "month": strftime("%m-%B", FileCreatedTime),
            "year": strftime("%Y", FileCreatedTime)
        }

        newFilePath: str = f"{destinationFolderName}/{fileGroup}/{fileTimeData['year']}/{fileTimeData['month']}/{fileTimeData['day']}"
        isFileAlreadyCopied: bool = path.exists(f"{newFilePath}/{fileName}")
        newFileName: str = rename(fileName, currentFile, fileTimeData, isFileAlreadyCopied)
        makedirs(newFilePath, exist_ok=True)
        move(currentFile, f"{newFilePath}/{newFileName}")

    except:
        errorLogger.log()

errorLogger.stopCapturing()