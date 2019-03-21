from settings import *
from helpers import *
from time import localtime, strftime
from shutil import move, copyfile
import os

saveLocation = "tempSave.py"

SETTING_RENAME_VALUE = CONST_RENAME_LIST[SETTING_RENAME]

print("hey yo lets organise some dang files")

print("do you want to use previously saved settings?")
if True if getYesNo() == CONST_YES else False:
    print("select the settings file:")
    settingsName = getFileName()
    # TODO - this
    eval("from " + settingsName[:-3] + " import *")

isOkToStart = False

while not isOkToStart:


    print("Select the source folder (the one that contains all the files to be sorted)")
    sourceFolder = getFolderName()

    print("Select the destination folder (the one that will contain the sorted files)")
    destinationFolder = getFolderName()

    print(formatMapping(SETTING_MAPPING))
    print(CONST_CURRENT_MAPPING_OK)

    loop = True if getYesNo() == CONST_NO else False

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
    SETTING_MONTHS = True if getYesNo() == CONST_YES else False

    print("This program will either move all the files (fast) or copy all the files (slow)")
    print("Do you want to move the files?")
    SETTING_COPY_OR_MOVE = CONST_MOVE if getYesNo() == CONST_YES else CONST_COPY

    # TODO - allow changing of file renaming setting

    print("Are the following settings ok?")
    print("Source: " + sourceFolder)
    print("Destination: " + destinationFolder)
    print("Will " + ("" if SETTING_MONTHS else "not ") + "divide years into months")
    print("Current filetype mapping:")
    print(formatMapping(SETTING_MAPPING))
    print("Will " + ("copy " if SETTING_COPY_OR_MOVE == CONST_COPY else "move ") + "files to the destination")
    isOkToStart = True if getYesNo() == CONST_YES else False


print("Save these settings?")
if True if getYesNo() == CONST_YES else False:
    saveLocation = input("Saved settings filename: ")
    saveLocation += ".py" if (len(saveLocation) < 4 or saveLocation[-3:] != ".py") else ""
    saved = saveSettings(saveLocation, SETTING_MAPPING, SETTING_MONTHS, SETTING_RENAME, SETTING_COPY_OR_MOVE)
    if saved[0]:
        print("settings saved to " + saveLocation)
    else:
        print("saving failed lol")
        print(saved[1])

# sourceFolder = "D:/Jason/Documents/pythonEVERYTHING/photoFinder/testSource"
# destinationFolder = "D:/Jason/Documents/pythonEVERYTHING/photoFinder/testDestination"

# this allows the program to find the folder for an extension nice and fast
reverseMapping = dict()

for key in SETTING_MAPPING:
    for extension in SETTING_MAPPING[key]:
        reverseMapping[extension] = key

# making the settings actually do a thing
moveOrCopy = move if SETTING_COPY_OR_MOVE == CONST_MOVE else copyfile
yearMonthFormat = "%y/%b" if SETTING_MONTHS else "%y"
rename = lambda name, createTime: name  # TODO - make functions that do the right thing here

errorLog = open("ERRORS.txt", "w")

for currentFile in getFolderContents(sourceFolder, True):
    try:
        fileName = currentFile.split("/")[-1]
        extension = fileName.split(".")[-1].lower()
        category = reverseMapping.get(extension, "default")
        fileCreateTime = getStatsFromFile(currentFile).st_mtime
        newFileName = rename(fileName, fileCreateTime)
        newPath = destinationFolder + "/" + category + "/" + strftime(yearMonthFormat, localtime(fileCreateTime)) + "/" + fileName
        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        print(currentFile)
        print(newPath)
        moveOrCopy(currentFile, newPath)
        print()
    except Exception as e:
        print("Problem encountered with file:")
        print(currentFile)
        print("Error encountered:")
        print(e)

        errorLog.write("Problem encountered with file:")
        errorLog.write(currentFile)
        errorLog.write("Error encountered:")
        errorLog.write(e)
        errorLog.write()

errorLog.close()

