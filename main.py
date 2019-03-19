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

from constants import *
from settings import *
from json import dumps
from tkinter import Tk
from tkinter import filedialog
Tk = Tk()
Tk.withdraw()

SETTING_RENAME_VALUE = CONST_RENAME_LIST[SETTING_RENAME]

def getCommand(theInput):
    theInput = theInput.lower()
    addList = ["add", "plus", "+", "also"]
    deleteList = ["remove", "delete", "-", "not"]
    if theInput in addList:
        return CONST_ADD
    elif theInput in deleteList:
        return CONST_DELETE
    else:
        return CONST_NOT_KNOWN

def getFiletypePair(theInput):
    inputList = theInput.split(" ")
    if len(inputList) == 1:
        return {"fileExtension": None, "category": inputList[0]}
    return {"fileExtension": inputList[0], "category": inputList[-1]}

    
def getYesNo(prompt):
    while True:
        theInput = str(input(prompt)).lower()
        if len(theInput) == 0 or len(theInput) > 4:
            continue
        if theInput[0] == "y":
            return CONST_YES
        elif theInput[0] == "n":
            return CONST_NO
    

def saveSettings(destination, mapping, months, rename):
    try:
        saveString = CONST_SETTING_STRING_1 + dumps(mapping, indent=4, sort_keys=True, separators=(",", ": ")) + CONST_SETTING_STRING_2 + ("True" if months else "False") + CONST_SETTING_STRING_3 + str(rename)
        saveFile = open(destination, "w")
        saveFile.write(saveString)
        return True, "save succeeded with message: 'yay'"
    except Exception as e:
        return False, e

def getFolderName():
    inputName = ""
    while inputName == "":
        inputName = filedialog.askdirectory()
    print(inputName + " chosen.")
    return inputName

def operate(operation, fileType, mapping):
    extension = fileType["fileExtension"]
    category = fileType["category"]
    if operation == CONST_ADD:
        try:
            temp = set(mapping[category])
        except KeyError:
            temp = set()
        temp.add(extension)
        mapping[category] = list(temp)
        return mapping
    if operation == CONST_DELETE:
        if extension is None:
            try:
                del mapping[category]
            except KeyError:
                print("unable to delete " + category + ", it is not a category")
            return mapping
        try:
            temp = set(mapping[category])
        except KeyError:
            print("unable to delete from " + category + ", it is not a category")
            return mapping
        try:
            temp.remove(extension)
        except KeyError:
            print("unable to delete " + extension + ", it is not an extension")
            return mapping
        if len(temp) > 0:
            mapping[category] = list(temp)
        else:
            del mapping[category]
        return mapping



print("hey yo lets organise some dang files")

# print("Select the source folder (the one that contains all the files to be sorted)")
# sourceFolder = getFolderName()
#
# print("Select the destination folder (the one that will contain the sorted files)")
# destinationFolder = getFolderName()

print(dumps(SETTING_MAPPING, indent=4, sort_keys=True, separators=(",", ": ")))
print(CONST_CURRENT_MAPPING_OK)

loop = True if getYesNo("('yes'/'no') > ") == CONST_NO else False

while loop:
    print("Current Mapping:")
    print(dumps(SETTING_MAPPING, indent=4, sort_keys=True, separators=(",", ": ")))
    print("What change would you like to make? (write 'none' to continue)")
    print("[add/remove] [filetype] [to/from] [format]")
    print("eg: add png to photos")
    print("or")
    print("remove [format]")
    print("eg: remove photos")
    userInput = str(input("> ")).lower().split(" ", 1)
    if userInput[0] == "none":
        break
    if len(userInput) == 1:
        print(CONST_UNKNOWN_OPERATION)
        print(CONST_CURRENT_MAPPING_OK)
        continue
    command = getCommand(userInput[0])
    fileTypePair = getFiletypePair(userInput[1])
    if command == CONST_NOT_KNOWN:
        print(CONST_UNKNOWN_OPERATION)
        print(CONST_CURRENT_MAPPING_OK)
        continue
    SETTING_MAPPING = operate(command, fileTypePair, SETTING_MAPPING)

    

    
    
    
    

