from traceback import format_exc
from datetime import datetime

class ErrorLogger:
    """
    Enables you to throw your errors into it and have them logged nicely to a lil file for you
    """
    def __init__(self, errorLogFileName: str = "errorLog.txt", resetFile: bool = False, logErrors: bool = True):
        self.errorFileName: str = errorLogFileName
        self.errorFile: TextIOWrapper = open(errorLogFileName, "w" if resetFile else "a")
        self.ableToCaptureErrors: bool = False
        self.errorCount: int = 0
        self.logErrors = logErrors


    def _getCurrentFormattedTime(self) -> str:
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

    def log(self, additionalContext=None) -> None:
        """
        Logs the most recent error to the log file, requires startCapturing to have been called first
        """
        if not self.logErrors:
            return
        if not self.ableToCaptureErrors:
            raise RuntimeError("Error capturing is not enabled yet, run ErrorLogger.startCapturing() first.")
        self.errorCount += 1
        self.errorFile.write(f"\nError at {self._getCurrentFormattedTime()}: {format_exc()}")
        if additionalContext != None:
            self.errorFile.write(f"Additional context: {additionalContext}\n")
        self.errorFile.write("~~~~~~~~~~")

    def stopCapturing(self) -> None:
        """
        Safely closes the error log file, must be called before the program exits
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
