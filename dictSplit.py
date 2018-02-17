from supportScript import *
import json
import os

#####################################################################################################################
########################################### CREATE Part of CRUD #####################################################
# Takes a full dictionary and appropriately splits it. This function would be used by a user only the first time, to
# create the splits, after they must use update, or else, reuse of this would create a new split dictionary. It is
# later reused by the Update function to appropriately create new splits.
#####################################################################################################################


def Create(d={}, count=None):

    if count == None:
        print("Processing given dictionary...")
        emptyOrResetDict()
        count = "main"

    i = 0
    split = 0
    fName = "{}.**REF**json".format(count)  # THE "**REF**" is used to differentiate, a split file from a general string containing the word "json" in it. (REF = Reference)
    ammendedDict = {}

    for k, v in d.items():

        if i % maxSplitLength == 0:

            if split > 0:
                spltFName = "{}Split{}.**REF**json".format(count, split)
            else:
                spltFName = fName

            if not i + 1 == len(d):
                ammendedDict["dictSplit"] = spltFName

            writeDictFile(ammendedDict, fName)

            fName = spltFName
            ammendedDict.clear()  # Learnt from https://www.tutorialspoint.com/python/dictionary_clear.htm
            split += 1

        if type(v) == dict:
            newCount = getAvailableCount()
            ammendedDict[k] = "{}.**REF**json".format(newCount)
            Create(v, newCount)

        else:
            ammendedDict[k] = v
        i += 1

    writeDictFile(ammendedDict, fName)


#####################################################################################################################
########################################### RETRIEVE Part of CRUD #####################################################
## Retrieves either the whole dictionary or segments of the dictionary depending on what keys and whether if keys are parsed ##
#####################################################################################################################


def Retrieve(*keys):
    d = readDictFile("main.json")

    for key in keys:
        if key in d:
            print(key)
            v = d[key]

            if isSplit(v):
                d = readDictFile(d[key])
                # with open("Resources/JSONData/" + d[key], "r") as f:
                #     d = json.loads(f.read())
            else:
                return v

        elif "dictSplit" in d:
            run = True
            checkRestDicts = d  # As the overall large dictionary has been split, this will be used to check through the other split parts of the dictionary

            while run:
                checkRestDicts = readDictFile(checkRestDicts['dictSplit'])

                if key in checkRestDicts:
                    run = False
                    v = checkRestDicts[key]

                    if isSplit(v):
                        d = readDictFile(v)
                    else:
                        return v

                elif not "dictSplit" in checkRestDicts:
                    run = False
                    print("KEY ERROR: Key '{}' from {} does not exist".format(key, str(keys)))
                    return

        else:
            print("KEY ERROR: Key '{}' from {} does not exist".format(key, str(keys)))
            return

    else:
        return decompileDict(d)


#####################################################################################################################
########################################### UPDATE Part of CRUD #####################################################
        ## Updates any given type of value to the split dictionary appropriately    ##
#####################################################################################################################


def Update(value, *keys, replace=False):
    keysLength = len(keys)
    if keys:
        lastKey = keys[-1]
        # pri0nt("lastKey = ", lastKey)

    # print("keys Length = ", keysLength)
    # First need to find exact file which needs to be updated
    if keysLength == 0 and type(value) != dict:
        Error = "Value Error!!.. Unable to update dictionary!!!.. provided value for the first parameter must be a dictionary (when no keys are passed to this function), inorder to update the existing dictinary"
        # Error checking to see if the user has provided a dictionary for value, when the keys parameter is empty, because it means that the user wants to add a new key and value item to the the existing main dictionary.
        print(Error)
        return Error

    elif keysLength == 0 and type(value) == dict:
        workingFile = "main.json"
        # This means that the user want to add a new dictionary key(s) and their values(s) within the main dictionary. (Main dictionary means the primary dictionary which is the parent to all other nests)

    else:
        workingFile = findKeyLoc(*keys)

        if "Error" in workingFile:
            print(workingFile["Error"])
            return

    # print("keys =", keys)
    print("workingFile = ", workingFile)

    d = readDictFile(workingFile)
    # with open(path + workingFile, "r") as f:
    #     d = json.loads(f.read())

    # Replace, removes all the nested dictionary's

    if replace:

        if keysLength > 0:
            print("d[lastKey] = " + d[lastKey])

            File2StrtDel(d[lastKey])

            if type(value) == dict:

                newCount = getAvailableCount()
                ammendedFName = "{}.json".format(newCount)
                d[lastKey] = ammendedFName

                writeDictFile(d, workingFile)
                # with open(path + workingFile, "w") as f:
                #     json.dump(d, f)

                # print("NewCOunt = ", newCount)
                Create(value, newCount)

            else:
                d[lastKey] = value
                writeDictFile(d, workingFile)

        else:
            File2StrtDel(workingFile)
            Create(value)

    #   if keysLength == 0:
    #       #I.e. wants to replace the entire dictionary, with a new dictionary.
    #       File2StrtDel(workingFile)

    #   else:
    #       File2StrtDel(d[keys[-1]])

    elif type(value) == dict:
        if keysLength > 0:
            update_existing_keys(value, d[lastKey])

        else:
            update_existing_keys(value, workingFile)

    else:
        if isSplit(d[lastKey]):
            File2StrtDel(d[lastKey])

        d[lastKey] = value

        writeDictFile(d, workingFile)

        # print(d)


#####################################################################################################################
########################################### Delete Part of CRUD #####################################################
## Deletes either the whole dictionary if no keys are given, or only segments of the dictionary related to the Key ##
#####################################################################################################################


def Delete(*keys):

    if len(keys) == 0:
        File2StrtDel("main.json")
        return

    lastKey = keys[-1]

    if lastKey.strip() == "":
        Error = "ERROR!!.. Last given key, from given Keys: {}, is detected as empty, Please check if the contents passed for the last given parameter is not empty"
        print(Error)
        return Error

    workingFile = findKeyLoc(*keys)

    # print("WrokingFile = ", workingFile)

    if "Error" in workingFile:
        print(workingFile["Error"])
        return workingFile["Error"]

    d = readDictFile(workingFile)
    # with open(path + workingFile, "r") as f:
    #     d = json.load(f)

    file = d[lastKey]

    # print("Key = {}".format(lastKey))
    # print("file = ", file)

    if isSplit(file):
        File2StrtDel(file)

    d.pop(lastKey, None)

    writeDictFile(d, workingFile)
    # with open(path + workingFile, "w") as f:
    # json.dump(d, f, indent=4)
