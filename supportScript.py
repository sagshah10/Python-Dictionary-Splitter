import os
import json
import shutil
# Learnt about shutil from: https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python


################################################################################################################
'''
This function checks whether JsonDictSplit, is being used for the first time or not,
and if first time, then it creates the necessary folders & setup files, then reqardless
of first time or not, it would return the path, and user defined maxDictLength before a split.
'''
################################################################################################################


def getPathAndMaxLength(maxSplitLength=50):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "Resources", "JSONData")

    if not os.path.isfile(os.path.join(path, "setup.json")):

        # print(path)
        os.makedirs(path, exist_ok=True)

        d = {"Available Count": [0], "path": path, "maxSplitLength": maxSplitLength}

        with open(os.path.join(path, "setup.json"), "w") as f:
            json.dump(d, f, indent=4)

    else:
        with open(os.path.join(path, "setup.json"), "r") as f:
            d = json.load(f)

        if d["maxSplitLength"] != maxSplitLength:
            pass

    toReturn = (d["path"], d["maxSplitLength"])

    return toReturn


################################################################################################################
'''
This function returns the exact working file or an error, after going through all
the user given keys and searching through all the mathcing split dictionary nests
to identify the working file of the last user given key.
'''
################################################################################################################


def findKeyLoc(*Keys, count=0, fName="main.json"):

    working_path = os.path.join(path, fName)

    if len(Keys) == 0:
        return fName

    d = readDictFile(working_path)

    found = False

    for k, v in d.items():

        if k in Keys:
            found = True

            if type(v) != str:
                if count + 1 == len(Keys):
                    return fName

                else:
                    Error = {"Error": "Key: {}, from given Keys: {}, does  not exist".format(Keys[count + 1], Keys)}
                    print(Error)
                    return Error

            if not isSplit(v):
                if count + 1 == len(Keys):
                    return fName

                else:
                    Error = {"Error": "Key: {}, from given Keys: {}, does  not exist".format(Keys[count + 1], Keys)}
                    print(Error)
                    return Error

            elif count + 1 == len(Keys):
                return fName

            else:
                return findKeyLoc(*Keys, count=count + 1, fName=v)
                # Learnt about passing *Keys as a parameter for the function call, from my stackoverflow question: https://stackoverflow.com/questions/48482244/calling-a-function-within-function-and-trying-to-change-args-paramater-within-t?noredirect=1#comment83957593_48482244
                # If just Keys was passed it would pass it as a value to include within a new tuple, or if Keys = Keys or *Keys=Keys was passed then it would return an error.

        elif "dictSplit" in d:
            return findKeyLoc(*Keys, count=count, fName=d["dictSplit"])

    if not found:
        Error = "Key: {}, from given Keys: {}, does  not exist".format(Keys[count], Keys)
        print(Error)
        return {"Error": Error}


################################################################################################################
'''
This function identifies and returns the next available count/ split number to be
used for spliting a nest from the given dictionary.
'''
################################################################################################################


def getAvailableCount():

    countD = readDictFile("setup.json")
    count = cleanUpAvailableCount(countD['Available Count'])

    returnCount = count[0]

    if len(count) == 1:
        ammendedCount = [count[0] + 1]

    else:
        ammendedCount = count[1:-1]

    countD['Available Count'] = ammendedCount

    writeDictFile(countD, "setup.json")
    return returnCount


################################################################################################################
'''
This function searches the availableCount array list to see if there is a sequence leading to the last
number stored on the list, and if so, it removes the sequence, whilst retaining only the number that
begins the sequence. This is created to remove unnecessary data being stored within this list.
'''
################################################################################################################


def cleanUpAvailableCount(availableCount):

    i = 0
    previous = availableCount[0]
    lastKnownSequence = availableCount[0]
    lastKnownSequencePosition = 0

    while i < len(availableCount):
        if (availableCount[i] - 1) != previous:
            lastKnownSequence = availableCount[i]
            lastKnownSequencePosition = i

        previous = availableCount[i]
        i += 1

    toReturn = sorted(list(set(availableCount[0:lastKnownSequencePosition + 1])))
    return toReturn



################################################################################################################
'''
This function reads and returns a dictionary file.
Made this function to help reduce repetition and LOC, whilst also to help make the code easier to read.
'''
################################################################################################################


def readDictFile(file):
    if isSplit(file):
        file = file.replace("**REF**", "")

    working_path = os.path.join(path, file)

    with open(working_path, "r") as f:
        d = json.load(f)

    return d


################################################################################################################
'''
This function writes a given dictionary to a given file name.
Made this function to help reduce repetition and LOC, whilst also to help make the code easier to read.
'''
################################################################################################################


def writeDictFile(d, file):
    if isSplit(file):
        file = file.replace("**REF**", "")

    working_path = os.path.join(path, file)

    with open(working_path, "w") as f:
        json.dump(d, f, indent=4)


################################################################################################################
'''
This function decompiles all the split out dictionary files and converts it back into a single whole,
dictionary.
'''
################################################################################################################


def decompileDict(d):

    if "dictSplit" in d:
        run = True
        checkRestDicts = d  # As the overall large dictionary has been split, this will be used to check through the other split parts of the dictionary

        while run:
            checkRestDicts = readDictFile(checkRestDicts['dictSplit'])
            # with open("Resources/JSONData/{}".format(checkRestDicts['dictSplit']), "r") as f:
            #     checkRestDicts = json.loads(f.read())

            for k, v in checkRestDicts.items():
                # print(k)
                if k == "dictSplit" or k == "AvailableCountNumbers":
                    continue

                else:
                    d[k] = v

            if not "dictSplit" in checkRestDicts:
                run = False

        d.pop("dictSplit", None)

    for k, v in d.items():

        if isSplit(v):

            nestedDict = readDictFile(v)

            # with open("Resources/JSONData/" + v, "r") as f:
            #     nestedDict = json.loads(f.read())

            d[k] = decompileDict(nestedDict)

    if "AvailableCountNumbrs" in d:
        d.pop("AvailableCountNumbers", None)

    return d


################################################################################################################
'''
This function erases the entire stored split dictionary, is to be used to recreate a new split dictionary.
'''
################################################################################################################


def emptyOrResetDict():

    if os.path.exists(path):
        shutil.rmtree(path)

    getPathAndMaxLength()


################################################################################################################
'''
This function deletes all files (i.e. all relating split dictionaries) within and linked to a given fileName.
'''
################################################################################################################


def File2StrtDel(fileName):

    fileName = fileName.replace(".**REF**json", ".json")
    filesToDel = []
    checkFiles = [fileName]

    while len(checkFiles) > 0:

        newCheckFiles = []

        for item in checkFiles:

            d = readDictFile(item)
            # with open(path + item, "r") as f:
            #     d = json.loads(f.read())

            filesToDel.append(item)

            for k, v in d.items():
                # print("{} = {}".format(k,v))
                if isSplit(v):
                    # found = True
                    newCheckFiles.append(v)

        checkFiles = newCheckFiles

        # print("FROM FILE: {} - DETECTED FILES TO DELETE ARE: {} \n\n".format(item, checkFiles))

    appendCount = []
    resetCount = False

    for item in filesToDel:

        item = item.replace(".**REF**json", ".json")
        check = item.split(".json")[0]

        if check.isdigit():
            appendCount.append(int(check))

        if item == "main.json":
            d = {}

            writeDictFile(d, "main.json")
            # with open(path + "main.json", "w") as f:
            #     json.dump(d, f)

            appendCount.append(0)
            resetCount = True  # This means all contents of the dict are deleted.

        else:
            os.remove(os.path.join(path, item))

    # print("appendCount = ", appendCount)
    # The code below, is to allow me to re-use the numbers which are deleted when new updates are made to the dict

    if len(appendCount) > 0:

        countD = readDictFile("setup.json")

        if resetCount:
            countD["Available Count"] = [0]

        else:
            # with open(path + "availableCount.json", "r") as f:
            #     countD = json.load(f)

            currentlyAvailableCount = countD['Available Count']

            for count in appendCount:
                if not count in currentlyAvailableCount:
                    currentlyAvailableCount.append(count)

            mergedCount = sorted(list(set(currentlyAvailableCount)))  # Using list(set(x)) to obtain a list with no duplicate values. Learnt from: https://stackoverflow.com/questions/6764909/python-how-to-remove-all-duplicate-items-from-a-list

            countD['Available Count'] = mergedCount

            # print("Dict Available Count No = {}".format(d['Available Count']))

        # print("countD = ", countD)
        writeDictFile(countD, "setup.json")
        # with open(path + "availableCount.json", "w") as f:
        #     json.dump(countD, f)

    return filesToDel


################################################################################################################
'''
This function is used to appropriately add new keys to an existing dictionary,
'''
################################################################################################################


def update_existing_keys(d, fName):

    fName = fName.replace(".**REF**json", ".json")
    mainFileCount = fName.split(".json")[0]

    if "Split" in fName:
        mainFileCount = mainFileCount.split("Split")[0]

    # mainFileCount above, is used to obtain the files actual number in order to easily reference and create the next split file, should all existing files for this dictionary have reached the maximum set dictionary length.

    checkExistingKeys = getDetailedKeys(fName)
    availableSpace = checkExistingKeys["availableSpace"]
    nextSplit = checkExistingKeys["nextSplit"]
    checkExistingKeys.pop("nextSplit", None)

    # print("availableSpace = ", availableSpace)

    for k, v in d.items():

        found = False
        existingKeyFile = None

        for detKey, detValue in checkExistingKeys["Keys"].items():

            if k in detValue:
                found = True
                existingKeyFile = detKey
                break

        if found:
            # This means a key with the same name already exists

            existingDKey = readDictFile(existingKeyFile)
            # with open(path + existingKeyFile, "r") as f:
            #     existingDKey = json.load(f)

            # print(existingDKey[k])

            if type(existingDKey[k]) == str:
                if isSplit(existingDKey[k]):
                    File2StrtDel(existingDKey[k])

            if type(v) == dict:
                newCount = getAvailableCount()
                newFileNm = "{}.**REF**json".format(newCount)
                Create(v, newCount)

                existingDKey[k] = newFileNm

            else:
                existingDKey[k] = v

            writeDictFile(existingDKey, existingKeyFile)
            # with open(path + existingKeyFile, "w") as file:
            #     json.dump(existingDKey, file)

        else:

            if not availableSpace:

                nxtFN = "{}Split{}.**REF**json".format(mainFileCount, nextSplit)  # nxtFN = Next File Name

                if nextSplit - 1 == 0:
                    prFN = "{}.**REF**json".format(mainFileCount)  # prFN = Previous File Name

                else:
                    prFN = "{}Split{}.**REF**json".format(mainFileCount, nextSplit - 1)

                availableSpace = [[nxtFN, DictLengthB4Split]]
                checkExistingKeys["Keys"]["nxtFN"] = [k]

                writeDictFile({}, nxtFN)
                pFUpdate = readDictFile(prFN)  # pFUpd = Previous File Update...
                # This opens the previous split file, to insert the key "dictSplit" and give it a reference to the new file created via nxtFN

                pFUpdate["dictSplit"] = nxtFN
                writeDictFile(pFUpdate, prFN)
                # This inserts a key reference to the new file on the previous split file

                # print("nextSplitB4Update =", nextSplit)
                nextSplit += 1
                # print("nextSplitAfterUpdate =", nextSplit)

            fileWithSpace4NewKey = availableSpace[0][0]
            dicWithSpc = readDictFile(fileWithSpace4NewKey)

            if type(v) == dict:
                newCount = getAvailableCount()
                newFileNm = "{}.**REF**json".format(newCount)

                # Need to save key with new file name where dict is saved.

                dicWithSpc[k] = newFileNm

                writeDictFile(dicWithSpc, fileWithSpace4NewKey)

                Create(v, newCount)

            else:
                dicWithSpc[k] = v

                if "dictSplit" in dicWithSpc:

                    temp = dicWithSpc["dictSplit"]
                    del dicWithSpc["dictSplit"]  # Doing this to keep the key dictSplit as the last element of the individual split dictionary section###
                    dicWithSpc["dictSplit"] = temp

                writeDictFile(dicWithSpc, fileWithSpace4NewKey)

            availableSpace[0][1] -= 1

            if availableSpace[0][1] == 0:
                del availableSpace[0]


################################################################################################################
'''
This is an internal function used to help get a detailed set of information, to allow the update_existing_keys
function to easily search through split files for matching keys, without having to constantly open those split
files, and to identify how much space a particular file has, before it meets the max length requirement, for
inserting new data into.
'''
################################################################################################################


def getDetailedKeys(file):
    # This function obtains all the keys for a dictionary
    file = file.replace(".**REF**json", ".json")
    if "Split" in file:
        file = file.split("Split")[0] + ".json"

    availableSpace = []
    run = True
    splitCount = 0
    newFile = None
    detailedKey = {"Keys": {}}

    while run:

        d = readDictFile(file)
        # with open(path + file, "r") as f:
        #     d = json.loads(f.read())

        if not "dictSplit" in d:
            run = False
        else:
            newFile = d["dictSplit"]

        d.pop("dictSplit", None)

        checkSpace = maxSplitLength - len(d)
        # print("SplitCount: {} - Space = {}".format(splitCount, checkSpace))
        if checkSpace > 0:
            spaceToAppend = [file, checkSpace]
            availableSpace.append(spaceToAppend)

        tempKeys = []

        for k, v in d.items():
            tempKeys.append(k)

        # toAppend = [file, tempKeys]
        detailedKey["Keys"][file] = tempKeys

        if newFile:
            file = newFile

        splitCount += 1

    detailedKey["nextSplit"] = splitCount
    detailedKey["availableSpace"] = availableSpace

    return detailedKey

################################################################################################################
'''
This function returns all the keys found from a user given keys location.
'''
################################################################################################################
def getKeys(*Keys):

    working_file = findKeyLoc(*Keys)

    if "Error" in working_file:
        return working_file["Error"]
    d = readDictFile(working_file)

    if len(Keys) > 0:
        lastKey = Keys[-1]
        if isSplit(d[lastKey]):
            working_file = d[lastKey]
        else:
            Error = "Key: {}, from given Keys: {}, is not a dictionary and therefore does not contain any keys".format(lastKey, list(Keys))
            print(Error)
            return(Error)

    obtainedKeys = []
    run = True

    while run:
        d = readDictFile(working_file)

        if "dictSplit" in d:
            working_file = d["dictSplit"]
        else:
            run = False

        d.pop("dictSplit", None)

        for k, v in d.items():
            obtainedKeys.append(k)

    return sorted(obtainedKeys)


################################################################################################################
'''
This function is used to reduce repetition, and to make it easier to identify whether if the give value is a
reference to a split file or not.
'''
################################################################################################################


def isSplit(value):
    if "**REF**json" in str(value):
        return True

    else:
        return False


path, maxSplitLength = getPathAndMaxLength()
