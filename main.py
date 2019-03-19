"""
~~ setup 

select 'read' folder using gui
select 'write' folder using gui

print and edit mappings

select file renaming settings

select auto or manual start

print settings and confirm, else restart

walk folder and print number of files

start (auto or manual based on setting above)

~~ end setup

~~ cleaning

live percent moved counter on screen

~~ end cleaning

done
"""


"""
ways to check if two strings are the same

they are equal coming in
they are equal when made the same case
if they are different lengths by one:
  remove one letter at a time from longer
they have two consecutive letters that are swapped


"""

from constants import *
from settings import *
from json import dumps
from tkinter import Tk, filedialog
Tk.withdraw()

SETTING_RENAME_VALUE = CONST_RENAME_LIST[SETTINGS_RENAME]

def getCommand(userInput):
    userInput = userInput.lower()
    addList = ["add", "plus", "+", "also"]
    deleteList = ["remove", "delete", "-", "not"]
    if userInput in addList:
        return CONST_ADD
    elif userInput in deleteList:
        return CONST_DELETE
    else:
        return CONST_NOT_KNOWN

def getFiletypePair(userInput):
    inputList = userInput.split(" ")
    if len(inputList) == 1:
        return CONST_NOT_KNOWN
    return {"fileExtension": inputList[0], "category": inputList[-1]}

    
def getYesNo(prompt):
    while True:
        userInput = str(input(prompt)).lower()
        if len(userInput) == 0 or len(userInput) > 4:
            continue
        if userInput[0] == "y":
            return CONST_YES
        elif userInput[0] == "n":
            return CONST_NO
    

def saveSettings(mapping, months, rename):
    saveString = CONST_SETTING_STRING_1 + dumps(SETTING_MAPPING, indent=2, sort_keys=True, separators=(",", ": ")) + CONST_SETTING_STRING_2 + ("True" if SETTING_MONTHS else "False") + CONST_SETTING_STRING_3 + str(SETTING_RENAME)
    return saveString

def getFolderName(prompt = "choose a file/folder", fileType = ""):
    inputName = ""
    while inputName == "":
        inputName = filedialog.askopenfilename(filetypes=[(prompt, fileType)])
    print(inputname + " chosen.")
    return inputName

print("hey yo lets organise some dang files")

print("Select the source folder (the one that contains all the files to be sorted)")
sourceFolder = getFolderName("Select the source folder")

print("Select the destination folder (the one that will contain the sorted files)")
destinationFolder = getFolderName("Select the destination folder")

print(CONST_CURRENT_MAPPING_OK)
print(dumps(SETTING_MAPPING, indent=2, sort_keys=True, separators=(",", ": ")))

while True if getYesNo("('yes'/'no') > ") == CONST_NO else False:
    print("Current Mapping:")
    print(dumps(SETTING_MAPPING, indent=2, sort_keys=True, separators=(",", ": ")))
    print("What change would you like to make?")
    print("[add/remove] [filetype] [to/from] [format]")
    print("eg: remove png from photos")
    userInput = str(input("> ")).split(" ", 1)
    if len(userInput) == 1:
        print(CONST_UNKNOWN_OPERATION)
        print(CONST_CURRENT_MAPPING_OK)
        continue
    command = getCommand(userInput[0])
    fileTypePair = getFiletypePair(userInput[1])
    if command == CONST_NOT_KNOWN or fileTypePair == CONST_NOT_KNOWN:
        print(CONST_UNKNOWN_OPERATION)
        print(CONST_CURRENT_MAPPING_OK)
        continue
    

    
    
    
    

