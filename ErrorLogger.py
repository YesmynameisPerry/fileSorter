from traceback import format_exc
from datetime import datetime
from io import TextIOWrapper
from typing import Dict
from json import dumps

__all__ = ["ErrorLogger"]

class ErrorLogger:
    """
    Enables you to throw your errors into it and have them logged nicely to a lil file for you
    """
    def __init__(self, errorLogFileName: str = "errors.log", *, resetFile: bool = False, logErrors: bool = True):
        self.errorFileName: str = errorLogFileName
        self.errorFile: TextIOWrapper = open(errorLogFileName, "w" if resetFile else "a")
        self.ableToCaptureErrors: bool = False
        self.errorCount: int = 0
        self.logErrors = logErrors

    @staticmethod
    def _getCurrentFormattedTime() -> str:
        """
        Returns a string of the current date and time
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    
    def startCapturing(self) -> None:
        """
        Must be called before logging any errors
        """
        if not self.logErrors:
            return
        if self.ableToCaptureErrors:
            print("Error capturing is already enabled")
            return
        self.ableToCaptureErrors: bool = True
        self.errorFile.write(f"\n~~ ERROR CAPTURING BEGINNING AT {self._getCurrentFormattedTime()} ~~\n")
        self.errorFile.flush()

    def log(self, additionalContext: Dict[str, str] =None) -> None:
        """
        Logs the most recent error to the log file, requires startCapturing to have been called first
        """
        if not self.logErrors:
            return
        if not self.ableToCaptureErrors:
            raise RuntimeError("Error capturing is not enabled yet, run ErrorLogger.startCapturing() first.")
        self.errorCount += 1
        self.errorFile.write(f"\nError at {self._getCurrentFormattedTime()}: {format_exc()}")
        if additionalContext is None:
            self.errorFile.write(f"Additional context: {dumps(additionalContext, indent=2)}\n")
        self.errorFile.write("~~~~~~~~~~")
        self.errorFile.flush()

    def stopCapturing(self) -> None:
        """
        Safely closes the error log file, should be called before the program exits
        """
        if not self.logErrors:
            return
        if not self.ableToCaptureErrors:
            print("Error capturing is already disabled")
            return
        self.ableToCaptureErrors: bool = False
        self.errorFile.write(f"\n~~ ERROR CAPTURING ENDING AT {self._getCurrentFormattedTime()} ~~\n")
        self.errorFile.close()
        if self.errorCount > 0:
            print(f"{self.errorCount} error{('s' if self.errorCount > 1 else '')} encountered. They have been logged to {self.errorFileName}.")
        self.errorCount: int = 0

    def getErrorCount(self) -> int:
        return self.errorCount
