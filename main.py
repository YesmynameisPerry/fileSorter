from settings import *
from helpers import *
from time import localtime, strftime
from shutil import move, copyfile
import os

saveLocation = "tempSave.py"

SETTING_RENAME_VALUE = CONST_RENAME_LIST[SETTING_RENAME]

print("hey yo lets organise some dang files")

IsOkToStart = False

while not IsOkToStart:

    print("Select the source folder (the one that contains all the files to be sorted)")
    sourceFolder = getFolderName()

    print("Select the destination folder (the one that will contain the sorted files)")
    destinationFolder = getFolderName()

    print(formatMapping(SETTING_MAPPING))
    print(CONST_CURRENT_MAPPING_OK)

    loop = True if getYesNo("('yes'/'no') > ") == CONST_NO else False

    while loop:
        print("Current Mapping:")
        print(formatMapping(SETTING_MAPPING))
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
    print(formatMapping(SETTING_MAPPING))
    print("Will " + ("" if SETTING_AUTOSTART else "not ") + "automatically start once scanning is complete")
    IsOkToStart = True if getYesNo("('yes'/'no') > ") == CONST_YES else False


# print("Save these settings?")
# if True if getYesNo("('yes'/'no') > ") == CONST_YES else False:
#     saved = saveSettings(saveLocation, SETTING_MAPPING, SETTING_MONTHS, SETTING_RENAME, SETTING_AUTOSTART)
#     if saved[0]:
#         print("settings saved to " + saveLocation)
#     else:
#         print("saving failed lol")
#         print(saved[1])

# auto start might disappear if it turns out to take too long or be too hard

#
# sourceFolder = "D:/Jason/Documents/pythonEVERYTHING/photoFinder/testSource"
# destinationFolder = "D:/Jason/Documents/pythonEVERYTHING/photoFinder/testDestination"

# this allows the program to find the folder for an extension nice and fast
reverseMapping = dict()

for key in SETTING_MAPPING:
    for extension in SETTING_MAPPING[key]:
        reverseMapping[extension] = key

for file in getFolderContents(sourceFolder, True):
    fileName = file.split("/")[-1]
    extension = fileName.split(".")[-1].lower()
    category = reverseMapping.get(extension, "default")
    statsObj = getStatsFromFile(file)
    newPath = destinationFolder + "/" + category + "/" + strftime('%Y/%b', localtime(statsObj.st_mtime)) + "/" + fileName
    os.makedirs(os.path.dirname(newPath), exist_ok=True)
    print(file)
    print(newPath)
    move(file, newPath)
    print()

"""
get file list
for each file:
    try:
        destination = mapping.get(fileExtension, extrasFolder)
        year, month = tostring(fileMetadataDate)
        move file (filepath, destination/year/month)
        continue
    except:
        print(error o no)
        log error to file
"""