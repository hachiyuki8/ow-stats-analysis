import json
import pandas as pd
from get_player_json import PLAYER_JSON

TANK_DATA = "tank_data.txt" # file name to store all tank data
DAMAGE_DATA = "damage_data.txt" # file name to store all damage data
SUPPORT_DATA = "support_data.txt" # file name to store all support data
PLAYER_INFO = PLAYER_JSON # file containing all player info scraped in get_player_json.py

ROLES = ["tank", "damage", "support"]
RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Masters", "Grandmaster"]
# lists of heroes for each role
TANK_LIST = ["dVa", "orisa", "reinhardt", "roadhog", "sigma", "winston", "wreckingBall", "zarya"]
DAMAGE_LIST = ["ashe", "bastion", "doomfist", "echo", "genji", "hanzo", "junkrat", "mccree", "mei", 
               "pharah", "reaper", "soldier76", "sombra", "symmetra", "torbjorn", "tracer", "widowmaker"]
SUPPORT_LIST = ["ana", "baptiste", "brigitte", "lucio", "mercy", "moira", "zenyatta"]

# lists of statistics for each role
TANK_AVERAGE = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
                "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "heroDamageDoneAvgPer10Min",
                "objectiveKillsAvgPer10Min", "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", 
                "timeSpentOnFireAvgPer10Min"]
TANK_COMBAT = ["weaponAccuracy"]
DAMAGE_AVERAGE = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
                  "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "heroDamageDoneAvgPer10Min",
                  "objectiveKillsAvgPer10Min", "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", 
                  "timeSpentOnFireAvgPer10Min"]
DAMAGE_COMBAT = ["criticalHitsAccuracy", "weaponAccuracy"]
SUPPORT_ASSIST = ["defensiveAssistsAvgPer10Min", "offensiveAssistsAvgPer10Min"]
SUPPORT_AVERAGE = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
                   "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "healingDoneAvgPer10Min", 
                   "heroDamageDoneAvgPer10Min", "objectiveKillsAvgPer10Min", 
                   "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", "timeSpentOnFireAvgPer10Min"]
SUPPORT_COMBAT = ["weaponAccuracy"]
GAME = ["timePlayed", "winPercentage"]

# hero specific statistics
TANK_HERO_SPECIFIC = {
    "dVa": ["damageBlockedAvgPer10Min", "mechsCalledAvgPer10Min", "selfDestructKillsAvgPer10Min"],
    "orisa": ["damageBlockedAvgPer10Min", "superchargerAssistsAvgPer10Min"],
    "reinhardt": ["chargeKillsAvgPer10Min", "damageBlockedAvgPer10Min", 
                  "earthshatterKillsAvgPer10Min", "fireStrikeKillsAvgPer10Min"],
    "roadhog": ["enemiesHookedAvgPer10Min", "hookAccuracy", "selfHealingAvgPer10Min",
                "wholeHogKillsAvgPer10Min"],
    "sigma": ["accretionKillsAvgPer10Min", "damageAbsorbedAvgPer10Min", 
              "damageBlockedAvgPer10Min", "graviticFluxKillsAvgPer10Min"],
    "winston": ["damageBlockedAvgPer10Min", "jumpPackKillsAvgPer10Min", 
                "playersKnockedBackAvgPer10Min", "primalRageKillsAvgPer10Min", 
                "primalRageMeleeAccuracy", "teslaCannonAccuracy"],
    "wreckingBall": ["grapplingClawKillsAvgPer10Min", "minefieldKillsAvgPer10Min",
                    "piledriverKillsAvgPer10Min", "playersKnockedBackAvgPer10Min"],
    "zarya": ["averageEnergy", "damageBlockedAvgPer10Min", "gravitonSurgeKillsAvgPer10Min",
              "highEnergyKillsAvgPer10Min", "primaryFireAccuracy"]
}
DAMAGE_HERO_SPECIFIC = {
    "ashe": ["bobKillsAvgPer10Min", "dynamiteKillsAvgPer10Min", "scopedAccuracy",
             "scopedCriticalHitsAccuracy"],
    "bastion": ["reconKillsAvgPer10Min", "selfHealingAvgPer10Min", "sentryKillsAvgPer10Min"],
    "doomfist": ["abilityDamageDoneAvgPer10Min", "meteorStrikeKillsAvgPer10Min",
                 "shieldsCreatedAvgPer10Min"],
    "echo": ["duplicateKillsAvgPer10Min", "focusingBeamKillsAvgPer10Min", 
             "stickyBombsKillsAvgPer10Min"],
    "genji": ["damageReflectedAvgPer10Min", "dragonbladesKillsAvgPer10Min"],
    "hanzo": ["dragonstrikeKillsAvgPer10Min", "stormArrowKillsAvgPer10Min"],
    "junkrat": ["concussionMineKillsAvgPer10Min", "enemiesTrappedAvgPer10Min", 
                "ripTireKillsAvgPer10Min"],
    "mccree": ["deadeyeKillsAvgPer10Min", "fanTheHammerKillsAvgPer10Min"],
    "mei": ["blizzardKillsAvgPer10Min", "damageBlockedAvgPer10Min", "enemiesFrozenAvgPer10Min",
            "selfHealingAvgPer10Min"],  
    "pharah": ["barrageKillsAvgPer10Min", "directHitsAccuracy", "rocketDirectHitsAvgPer10Min"],
    "reaper": ["deathsBlossomKillsAvgPer10Min", "selfHealingAvgPer10Min"],
    "soldier76": ["bioticFieldHealingDone", "helixRocketKillsAvgPer10Min", 
                  "tacticalVisorKillsAvgPer10Min"],
    "sombra": ["enemiesEmpdAvgPer10Min", "enemiesHackedAvgPer10Min"],
    "symmetra": ["damageBlockedAvgPer10Min", "playersTeleportedAvgPer10Min", "primaryFireAccuracy",
                 "secondaryFireAccuracy", "sentryTurretsKillsAvgPer10Min"],
    "torbjorn": ["moltenCoreKillsAvgPer10Min", "turretsDamageAvgPer10Min", "turretsKillsAvgPer10Min"],
    "tracer": ["healthRecoveredAvgPer10Min", "pulseBombsKillsAvgPer10Min"],
    "widowmaker": ["scopedAccuracy", "scopedCriticalHitsAccuracy"]      
}
SUPPORT_HERO_SPECIFIC = {
    "ana": ["enemiesSleptAvgPer10Min", "nanoBoostAssistsAvgPer10Min", "scopedAccuracy", 
            "selfHealingAvgPer10Min", "unscopedAccuracy"],
    "baptiste": ["amplificationMatrixAssistsAvgPer10Min", "healingAccuracy",
                 "immortalityFieldDeathsPreventedAvgPer10Min", "selfHealingAvgPer10Min"],
    "brigitte": ["armorProvidedAvgPer10Min", "damageBlockedAvgPer10Min", "inspireUptimePercentage"],
    "lucio": ["soundBarriersProvidedAvgPer10Min", "selfHealingAvgPer10Min"],
    "mercy": ["damageAmplifiedAvgPer10Min", "playersResurrectedAvgPer10Min"],
    "moira": ["coalescenceHealingAvgPer10Min", "coalescenceKillsAvgPer10Min", 
              "secondaryFireAccuracy", "selfHealingAvgPer10Min"],
    "zenyatta": ["transcendenceHealingBest"]
}

#lists of statistics for each hero, separated by category
TANK_STATS = {}
for tank in TANK_LIST:
    TANK_STATS[tank] = {"average": TANK_AVERAGE, "combat": TANK_COMBAT,
                        "heroSpecific": TANK_HERO_SPECIFIC[tank]}
DAMAGE_STATS = {}
for damage in DAMAGE_LIST:
    DAMAGE_STATS[damage] = {"average": DAMAGE_AVERAGE, "combat": DAMAGE_COMBAT,
                            "heroSpecific": DAMAGE_HERO_SPECIFIC[damage]}
SUPPORT_STATS = {}
for support in SUPPORT_LIST:
    SUPPORT_STATS[support] = {"assists": SUPPORT_ASSIST, "average": SUPPORT_AVERAGE, 
                              "combat": SUPPORT_COMBAT, 
                              "heroSpecific": SUPPORT_HERO_SPECIFIC[support]}

ALL_SRS = {"tank": [], "damage": [], "support": []}
ALL_RANKS = {"tank": 0, "damage": 0, "support": 0}
TIME_THRESHOLD = 3600 # only keep statistics for heroes with time played above this many seconds
INTERVAL = 1000 # print the current scraping progress after every INTERVAL number of players

def srToRank(sr):
    """ Map an sr to the corresponding rank

    args:
        sr: an integer

    return:
        a string of rank of invalid if sr < 0 or sr > 5000
    """
    if 0 <= sr and sr < 1500:
        return "Bronze"
    elif sr < 2000:
        return "Silver"
    elif sr < 2500:
        return "Gold"
    elif sr < 3000:
        return "Platinum"
    elif sr < 3500:
        return "Diamond"
    elif sr < 4000:
        return "Masters"
    elif sr <= 5000:
        return "Grandmaster"
    else:
        return "Invalid"

def formatDuration(timeStr):
    """
    args:
        time: a string of format hh:mm:ss or mm:ss or ss

    return:
        sec: an integer, number of seconds corresponding to time
    """

    timeLst = timeStr.split(":")
    if len(timeLst) == 0:
        return 0
    
    sec = int(timeLst[-1])
    if len(timeLst) == 2:
        sec += int(timeLst[-2]) * 60 
    elif len(timeLst) == 3:
        sec += int(timeLst[-3]) * 3600
    return sec

def storeStats(role, sr, playerStats, outputFile, heroList, heroStats):
    """
    args:
        role: a string, tank, damage, or support
        sr: an integer in [0, 5000] indicating player's SR
        playerStats: a dictionary of player's competitive statistics
        outputFile: an opened file corresponding to the input role to store player stats
        heroList: a list of all hero names under the input role
        heroStats: a dictionary of all statistics names for each hero under the input role
    
    return:
        numHeroes: number of heroes under the given role with valid stats for the given player
    """

    allStats = dict()
    allStats["rating"] = sr
    for curHero, curStats in playerStats.items():
        # only check heroes for the current role
        if curHero not in heroList:
            continue

        # only check heroes with time played above TIME_THRESHOLD
        if "timePlayed" not in curStats["game"]:
            continue
        elif formatDuration(curStats["game"]["timePlayed"]) < TIME_THRESHOLD:
            continue

        statsToSave = dict()
        statsToSave["timePlayed"] = formatDuration(curStats["game"]["timePlayed"])
        # only keep the stats specified in TANK/DAMAGE/SUPPORT_HERO_SPECIFIC
        for statCategory, statDict in curStats.items():
            if not statDict:
                continue

            statsToKeep = heroStats[curHero]
            if statCategory in statsToKeep.keys():
                for statName, stat in statDict.items():
                    if statName in statsToKeep[statCategory]:
                        statsToSave[statName] = stat
        
        allStats[curHero] = statsToSave
    
    outputFile.write(str(allStats) + "\n")
    numHeroes = len(allStats) - 1
    return numHeroes
        
def separateDataByRole(allPlayers, tankOutput, damageOutput, supportOutput):
    """ For each player, save the followings to the output file of the corresponding role:
        1) rating: an integer, player's SR for that role
        2) compStats: a dictionary, player's competitive stats for all heroes played under that role
        compStats is a nested dictionary {hero: {name of the statistic: number}}. 
        Keys in the outer dictionary are names of all heroes played by a hero under a given role 
        (see TANK_LIST, DAMAGE_LIST, and SUPPORT_LIST). Keys in the inner dictionary are names of
        statistics for a given hero (see TANK_STATS, DAMAGE_STATS, and SUPPORT_STATS).
        Global variable ALL_SRS will contain a list of SRs for each role.

    args:
        allPlayers: an list of player info
        tankOutput: file name under which to store info for tanks
        damageOutput: file name under which to store info for damages
        supportOutput: file name under which to store info for supports

    return:
        player_count: total number of players processed
    """
    playerCount = 0
    with open(tankOutput, "a+") as tankFile, open(damageOutput, "a+") as damageFile, open(supportOutput, "a+") as supportFile:
        for player in allPlayers:
            player = json.loads(player)
            # extract player's SR(s)
            for srInfo in player["ratings"]:
                curLevel = srInfo["level"]
                curRole = srInfo["role"]
                if curLevel < 0 or curLevel > 5000:
                    print("[separateDataByRole] Invalid player SR")
                    continue

                ALL_SRS[curRole].append(curLevel)
                numTanks, numDamages, numSupports = 0, 0, 0
                if curRole == "tank":
                    numTanks = storeStats(curRole, curLevel, player["compStats"], tankFile, TANK_LIST, TANK_STATS)
                elif curRole == "damage":
                    numDamages = storeStats(curRole, curLevel, player["compStats"], damageFile, DAMAGE_LIST, DAMAGE_STATS)
                else:
                    numSupports = storeStats(curRole, curLevel, player["compStats"], supportFile, SUPPORT_LIST, SUPPORT_STATS)

            playerCount += 1

            if playerCount % INTERVAL == 0:
                print(f"[separateDataByRole] Current number of players added: {playerCount}/{len(allPlayers)}")
                for role, srs in ALL_SRS.items():
                    print(f"[separateDataByRole] Number of {role}s so far: {len(srs)}")

    return playerCount

if __name__ == "__main__":
    with open(PLAYER_INFO, "r") as inFile:
        allPlayers = inFile.readlines()
        print(f"Total number of players in the input file: {len(allPlayers)}")
        playerCount = separateDataByRole(allPlayers, TANK_DATA, DAMAGE_DATA, SUPPORT_DATA)

        # map SRs to ranks for each role
        for role, sr in ALL_SRS.items():
            sr = pd.Series(sr)
            rank = sr.map(srToRank).astype("category").cat.reorder_categories(RANKS)
            ALL_RANKS[role] = rank

        # show rank distribution for each role
        for role, rank in ALL_RANKS.items():
            print(f"Rank distribution (percentage) of {role} from a total of {len(ALL_RANKS[role])} players:")
            print(round(rank.groupby(rank).count()/len(rank)*100, 1))