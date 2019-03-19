"""
~~ setup 

select 'read' folder using gui
select 'write' folder using gui

print and edit mappings

select putting photos into month folders

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
from helpers import *
from json import dumps

SETTING_RENAME_VALUE = CONST_RENAME_LIST[SETTING_RENAME]

print("hey yo lets organise some dang files")

IsOkToStart = False
enteredLoop = False

while not IsOkToStart:
    enteredLoop = True
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

    print("Do you want 'year' folders to be divided into 'month' folders?")
    SETTING_MONTHS = True if getYesNo("('yes'/'no') > ") == CONST_YES else False

    print("This program will scan the source folder and find all the files, displaying a total count.")
    print("Do you want to automatically start sorting once this is done?")
    SETTING_AUTOSTART = True if getYesNo("('yes'/'no') > ") == CONST_YES else False

    print("Are the following settings ok?")
    print("Source: " + sourceFolder)
    print("Destination: " + destinationFolder)
    print("Will " + ("" if SETTING_MONTHS else "not ") + "divide years into months")
    print("Current filetype mapping:")
    print(dumps(SETTING_MAPPING, indent=4, sort_keys=True, separators=(",", ": ")))
    print("Will " + ("" if SETTING_AUTOSTART else "not ") + "automatically start once scanning is complete")
    IsOkToStart = True if getYesNo("('yes'/'no') > ") == CONST_YES else False

if enteredLoop:
    saveSettings("settings.py", SETTING_MAPPING, SETTING_MONTHS, SETTING_RENAME, SETTING_AUTOSTART)
    print("settings saved to settings.py")

