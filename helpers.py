from constants import *

# returns either CONST_ADD, CONST_DELETE or CONST_NOT_KNOWN based on an input
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

# returns an object with a file extension and a category, or a None and a category
def getFiletypePair(theInput):
    inputList = theInput.split(" ")
    if len(inputList) == 1:
        return {"fileExtension": None, "category": inputList[0]}
    return {"fileExtension": inputList[0], "category": inputList[-1]}

# prompts the user until a valid reason to return CONST_YES or CONST_NO is given
def getYesNo(prompt):
    while True:
        theInput = str(input(prompt)).lower()
        if len(theInput) == 0 or len(theInput) > 4:
            continue
        if theInput[0] == "y":
            return CONST_YES
        elif theInput[0] == "n":
            return CONST_NO
    
# saves the given settings in the destination
def saveSettings(destination, mapping, months, rename, autoStart):
    try:
        saveString = CONST_SETTING_STRING_1 + formatMapping(mapping) + CONST_SETTING_STRING_2 + ("True" if months else "False") + CONST_SETTING_STRING_3 + str(rename) + CONST_SETTING_STRING_4 + ("True" if autoStart else "False")
        saveFile = open(destination, "w")
        saveFile.write(saveString)
        saveFile.close()
        return True, "save succeeded with message: 'yay'"
    except Exception as e:
        return False, e

# uses tkinter to bring up a folder selection window
def getFolderName():
    from tkinter import Tk
    from tkinter import filedialog
    Tk = Tk()
    Tk.withdraw()
    inputName = ""
    while inputName == "":
        inputName = filedialog.askdirectory()
    print(inputName + " chosen.")
    return inputName

# adds or removes a filetype or category from the mapping dictionary
def operate(operation, fileType, mapping):
    extension = fileType["fileExtension"]
    category = fileType["category"]
    if operation == CONST_ADD:
        addedExtensions = [extension for listOfExtensions in [mapping[key] for key in mapping.keys()] for extension in listOfExtensions]
        if extension in addedExtensions:
            knownCategory = "WHAT NO"
            for key in mapping:
                if extension in mapping[key]:
                    knownCategory = key
            print(extension + " is already added to " + knownCategory)
            return mapping
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

# returns a neat string that looks nice
def formatMapping(mapping):
    from json import dumps
    return dumps(mapping, indent=4, sort_keys=True, separators=(",", ": "))

# returns all the files in a folder
def getFolderContents(currentDirectory, includeSubdirectories=False):
    from os import walk, listdir
    output = []
    if includeSubdirectories:
        for fileTuple in walk(currentDirectory):
            for file in fileTuple[2]:
                output += [(fileTuple[0].replace("\\", "/")+"/"+file)]
    else:
        files = listdir(currentDirectory)
        for item in files:
            if "." in item:
                output += [currentDirectory.replace("\\", "/") + "/" + item]
    return output

# getStats on a file
def getStatsFromFile(file):
    from os import stat
    return stat(file)