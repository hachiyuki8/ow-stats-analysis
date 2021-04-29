import requests
import json
import time
import os

NAMES_PATH = os.getcwd() + "/names/" # path to the folder with text files storing usernames
OUTPUT_FILE = "battletags.txt" # file name to store all valid battletags
NAME_PROGRESS_FILE = "usednames.txt" # file name to store all usernames for which searching is done

PLAY_OW = "https://playoverwatch.com/en-us/search/account-by-name/" # url from which to get battletags
RATE_LIMIT = 0.33 # time paused after each query to playeroverwatch.com
INTERVAL = 25 # print the current scraping progress after every INTERVAL number of usernames

def getBattletagsFromName(username):
    """ Return a list of battletags with the given username.
        Only battletags that 1) are for PC users, 2) have a public profile, and 3) are at least
        level 25 are included.

    args:
        username: a string
    
    return:
        result: a list of battletags that satisfy the requirements above
    """

    url = PLAY_OW + username.lower()
    response = requests.get(url)
    result = []

    if response.status_code == 200:
        battletags = json.loads(response.text)
        for tag in battletags:
            if tag["platform"] == "pc" and tag["isPublic"] and tag["level"] >= 25:
                result.append(tag["urlName"])
    else: 
        print("[getBattletagsFromName] Error querying from playoverwatch.com\n")

    return result

def getTagsFromSet(names, output):
    """ For every given username, find all the associated battletags and write them to the given 
        output file. 
        To keep track of the progress, when all battletags of a username have been written, this 
        username is added to a file, defined by NAME_PROGRESS_FILE, which contains all usernames 
        for which the searching is done.
        To avoid getting banned from https://playoverwatch.com/, a rate limit defined by RATE_LIMIT
        is set for each query (per username).

    args:
        names: a set of (unique) strings
        output: an opened file to store the battletags
    
    return:
        result: a list of battletags for all the input usernames
    """

    result = []
    name_count = 0
    tag_count = 0
    with open(NAME_PROGRESS_FILE, "a+") as usedNames:
        for name in names:
            newTags = getBattletagsFromName(name)
            tag_count += len(newTags)
            # write battletags for the current username to the output file
            output.write("\n".join(newTags) + "\n")
            # add the current username to the file of used names
            usedNames.write(str(name) + "\n")
            name_count += 1

            if (name_count % INTERVAL == 0):
                print(f"...[getTagsFromSet] Current progress: {name_count}/{len(names)}")
                print(f"...[getTagsFromSet] Number of tags collected: {tag_count}")
            time.sleep(RATE_LIMIT) # rate limit per username 

    return result

# @INPUT:  [string] path of a folder
# @INPUT:  [file] output file object where battletags are written to
# @OUTPUT: [list of strings] battletags of all names in all text files in the folder
def checkAllFiles(folderPath, output):
    """ Check every text file in the given folder for usernames, and search for all valid
        battletags associated with these usernames.

    args:
        folderPath: a string containing the path of the folder containing username text files
        output: an opened file to be passed into getTagsFromSet

    return:
        result: a list of battletags for all usernames in the input files
    """

    namePool = set()
    for file in os.listdir(folderPath):
        if file.endswith(".txt"):
            filePath = folderPath + file
            with open(filePath, "r") as curFile:
                print(f"[checkAllFiles] Successfully opened {file}")
                names = curFile.readlines()
                names = [name.strip() for name in names]
                # Dedup usernames stored across different files
                namePool.update(names)
    
    print(f"[checkAllFiles] Total number of names: {len(namePool)}")
    result = getTagsFromSet(namePool, output)

    return result

if __name__ == "__main__":
    """ Write all valid battletags (PC, public, level >= 25) associated with usernames stored in 
        text files in NAMES_PATH to OUTPUT_FILE. NAME_PROGRESS_FILE will contain all usernames for
        which searching is done.

        To avoid scraping the same usernames across multiple runs, text files in NAMES_PATH should
        not contain any username in NAME_PROGRESS_FILE. 

        This program takes around 30 minutes to scrape 1000 usernames. If it is interrupted and
        user wants to continue scraping instead of starting over, user should manually remove all 
        usernames in NAME_PROGRESS_FILE from text files in NAMES_PATH before rerunning the program. 
        NAME_PROGRESS_FILE and OUTPUT_FILE can remain the same across multiple runs.
    """
    with open(OUTPUT_FILE, "a+") as output:
        checkAllFiles(NAMES_PATH, output)
            