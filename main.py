from tkinter import Tk
from tkinter import filedialog
from time import sleep, strftime, localtime
from os import walk, listdir, stat, makedirs
from typing import List, Dict
from shutil import copy2, move
from io import TextIOWrapper
from datetime import datetime
from settings import DOCUMENT_LOOKUP as DocumentTypes
from traceback import format_exc

# SETUP

usePauses: bool = False
useEnters: bool = True
logErrors: bool = False

Tk = Tk()
Tk.withdraw()

# HELPERS

def rename(fileName: str, fileNameData: Dict[str, str]) -> str:
    """
    Renames a file to whatever the user wants, depending on global variables
    """
    # TODO - provide different options for file renaming
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
    delay(2)
    folderName: str = filedialog.askdirectory()

    while folderName == "":
        print()
        print("No folder chosen, please choose a folder.")
        delay(2)
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

def getCurrentFormattedTime() -> str:
    """
    Returns a string of the current date and time
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

def getFileTypeGroup(fileExtension: str, default: str = "unknown") -> str:
    try:
        return DocumentTypes[fileExtension.lower()]
    except KeyError:
        return default

class ErrorLogger:
    """
    Enables you to throw your errors into it and have them logged nicely to a lil file for you
    """
    def __init__(self, errorLogFileName: str = "errorLog.txt", resetFile=False):
        self.errorFileName: str = errorLogFileName
        self.errorFile: TextIOWrapper = open(errorLogFileName, "w" if resetFile else "a")
        self.ableToCaptureErrors: bool = False
        self.errorCount: int = 0
    
    def startCapturing(self) -> None:
        """
        Must be called before logging any errors
        """
        if not logErrors:
            return
        if self.ableToCaptureErrors:
            print("Error capturing is already enabled")
            return
        self.ableToCaptureErrors: bool = True
        self.errorFile.write(f"\n~~ ERROR CAPTURING BEGINNING AT {getCurrentFormattedTime()} ~~\n")

    def log(self, additionalContext=None) -> None:
        """
        Logs the most recent error to the log file, requires startCapturing to have been called first
        """
        if not logErrors:
            return
        if not self.ableToCaptureErrors:
            raise RuntimeError("Error capturing is not enabled yet, run ErrorLogger.startCapturing() first.")
        self.errorCount += 1
        self.errorFile.write(f"\nError at {getCurrentFormattedTime()}: {format_exc()}")
        if additionalContext != None:
            self.errorFile.write(f"Additional context: {additionalContext}\n")
        self.errorFile.write("~~~~~~~~~~")

    def stopCapturing(self) -> None:
        """
        Safely closes the error log file, must be called before the program exits
        """
        if not logErrors:
            return
        if not self.ableToCaptureErrors:
            print("Error capturing is already disabled")
            return
        self.ableToCaptureErrors: bool = False
        self.errorFile.write(f"\n~~ ERROR CAPTURING ENDING AT {getCurrentFormattedTime()} ~~\n")
        self.errorFile.close()
        if self.errorCount > 0:
            print(f"{self.errorCount} error{('s' if self.errorCount > 1 else '')} encountered. They have been logged to {self.errorFileName}.")
        self.errorCount: int = 0

# LOGIC

errorLogger: ErrorLogger = ErrorLogger()
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
            "month": strftime("%B", localtime(fileCreatedFloat)),
            "year": strftime("%Y", localtime(fileCreatedFloat))
        }

        newFileName: str = rename(fileName, fileTimeData)
        newFilePath: str = f"{destinationFolderName}/{fileGroup}/{fileTimeData['year']}/{fileTimeData['month']}"

        makedirs(newFilePath, exist_ok=True)
        copy2(currentFile, f"{newFilePath}/{newFileName}")

    except Exception as e:
        errorLogger.log()

errorLogger.stopCapturing()