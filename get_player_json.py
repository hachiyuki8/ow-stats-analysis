import requests
import json
import time
import os
from get_battletags import OUTPUT_FILE

OVRSTAT = "https://ovrstat.com/stats/pc/" # API from which to get player stats
PLAYER_JSON = "player_json.txt" # file name to store JSON objects for all players
BATTLETAG_PROGRESS = "usedbattletags.txt" # file name to store all battletags that have been added
BATTLETAGS = OUTPUT_FILE # file containing all battletags scraped in get-battletags.py

RATE_LIMIT = 0.33 # time paused after each query to ovrstat.com
INTERVAL = 25 # print the current scraping progress after every INTERVAL number of battletags
ERROR_MSG = {-999: "Player not found", -2: "Private profile", -1: "No competitive ratings"}
# only search for battletags within index range [START, END) in BATTLETAGS
START = 0
END = 10000

def getPlayerFromTag(battletag):
    """ Return a json object containing player stats for the given battletag.
        
    args:
        battletag: a string of a valid battletag (username-id)
    
    return:
        status: -999 if player not found, -2 if private profile, -1 if no ratings, 0 otherwise
        ratings: a JSON object containing skill ratings (ELO) information
        compStats: a JSON object containing player statistics in competitive game mode
    """

    url = OVRSTAT + battletag
    response = requests.get(url)

    if response.status_code == 200:
        playerJSON = response.json()
        # skip players with private profile or no ratings
        if playerJSON["private"]:
            return -2, None, None
        elif not playerJSON["ratings"]:
            return -1, None, None
        
        ratings = playerJSON["ratings"]
        compStats = playerJSON["competitiveStats"]["careerStats"]
    else:
        return -999, None, None

    return 0, ratings, compStats

def checkAllTags(battletags, output):
    """ Fetch the JSON objects for every valid battletag in battletags and write them to the given
        output file.
        To keep track of the progress, after a battletag has been checked, it is added to a file
        defined by BATTLETAGS_PROGRESS.
        To avoid getting banned from https://ovrstat.com/, a rate limit defined by RATE_LIMIT is
        set for each query (per battletag).

        args:
            battletags: a list of battletags
            output: an opened file to store the JSON objects for all battletags

        return:
            battletag_count: total number of battletags for which player stats are collected
    """

    battletag_count = 0
    error_count = 0
    with open(BATTLETAG_PROGRESS, "a+") as usedBattletags:
        for battletag in battletags:
            status, ratings, compStats = getPlayerFromTag(battletag)
            if status < 0:
                msg = ERROR_MSG[status]
                print(f"[checkAllTags] Error querying {battletag} from ovrstat.com: {msg}")
                error_count += 1
            else:
                playerDict = {"ratings": ratings, "compStats": compStats}
                # write JSON objects for the current battletag to the output file
                json.dump(playerDict, output)
                output.write("\n")
                # add the current battletag to the file of used battletags
                usedBattletags.write(str(battletag) + "\n")
                battletag_count += 1

                if (battletag_count % INTERVAL == 0):
                    print(f"""[checkAllTags] Current progress: 
                              {battletag_count}(valid)+{error_count}(error)/{len(battletags)}""")
                time.sleep(RATE_LIMIT) # rate limit per battletag
    
    return battletag_count

if __name__ == "__main__":
    """ Write a dictionary of JSON object containing player's competitive rating (ELO) and hero 
        statistics to PLAYER_JSON for every battletag in BATTLETAGS with valid information.
        BATTLETAG_PROGRESS will contain all battletags that have been checked.

        To avoid scraping the same battletags across multiple runs, BATTLETAGS should not contain
        any battletag in BATTLETAG_PROGRESS.

        This program takes around 45 minutes to scrape 1000 battletags (on average 40% of the 
        battletags have valid competitive stats). User should scrape all the battletags provided in
        BATTLETAGS in patches, by specifying a disjoint index range each time using START and END.

        If it is interrupted and user wants to continue scraping instead of starting over, user 
        should first move on to the next [START, END) range, and rerun the program on the 
        interrupted range after first round of scraping is done.
    """
    with open(PLAYER_JSON, "a+") as output:
        with open(BATTLETAGS, "r") as inFile:
            allTags = [tag.strip() for tag in inFile.readlines()]
            allTags = [tag for tag in allTags if tag]
            print(f"[MAIN] Total number of input battletags: {len(allTags)}")
            print(f"...Checking battletags from index {START} to {END}")
            battletag_count = checkAllTags(allTags[START:END], output)
            print(f"[MAIN] Scraping done. Total number of battletags with valid stats: {battletag_count}")
