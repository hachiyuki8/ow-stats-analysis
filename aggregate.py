import pandas as pd
import numpy as np
import math
import pickle

from parse_player_stats import ROLES, ROLES_LISTS

DATA_PATH = "test_train/"
TANK_STATS = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
              "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "heroDamageDoneAvgPer10Min",
              "objectiveKillsAvgPer10Min", "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", 
              "timeSpentOnFireAvgPer10Min", "weaponAccuracy", "winPercentage"]
DAMAGE_STATS = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
                "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "heroDamageDoneAvgPer10Min",
                "objectiveKillsAvgPer10Min", "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", 
                "timeSpentOnFireAvgPer10Min", "weaponAccuracy", "winPercentage"]
SUPPORT_STATS = ["barrierDamageDoneAvgPer10Min", "criticalHitsAvgPer10Min", "deathsAvgPer10Min", 
                 "eliminationsAvgPer10Min", "finalBlowsAvgPer10Min", "healingDoneAvgPer10Min", 
                 "heroDamageDoneAvgPer10Min", "objectiveKillsAvgPer10Min", 
                 "objectiveTimeAvgPer10Min", "soloKillsAvgPer10Min", "timeSpentOnFireAvgPer10Min",
                 "weaponAccuracy", "winPercentage"]
THRESHOLD = 0.3 # remove a column if the percentage of missing value in this column is larger than threshold
STATS = {"tank": TANK_STATS, "damage": DAMAGE_STATS, "support": SUPPORT_STATS}

def hero_with_time(row):
    """
    For each player (row), return a list of hero names that the player has play time on 
    
    args:
        row: pd.series

    return:
        hero_list: a list of strings
    """

    hero_list = []
    for stat_name, stat_value in row.items():
        if stat_name.endswith("timePlayed") and not math.isnan(stat_value):
            hero_name = stat_name.split("_")[0]
            hero_list.append(hero_name)
    
    return hero_list

def get_missing_percent(df, col):
    """
    Get the percentage of missing for the given column in the given data frame
    
    args:
        df: a data frame
        col: a valid column of the data frame

    return:
        prop: a float
    """
    count = 0
    for val in df[col]:
        if math.isnan(val):
            count += 1
    prop = count/len(df[col])
    return round(prop, 4)

def aggregate_by_role(row, role):
    """
    Aggregate the same statistics for different tanks for each player

    This function is applies to each row in a data frame, and takes the average of the same 
    statistics for different tanks. For example, if a player has played two tanks with 0.5 
    win percentage on one and 0.3 win percentage on the other, then this player's aggregated
    death is 0.4.
    
    args:
        df: a data frame
        col: a valid column of the data frame

    return:
        prop: a float
    """
    hero_list = hero_with_time(row)
    result = {}
    stat_list = STATS[role]

    for stat in stat_list:
        stat_count = 0
        stat_total = 0
        for hero in hero_list:
            cur_stat = hero + "_" + stat
            if cur_stat in row.keys() and not math.isnan(row[cur_stat]):
                stat_count += 1
                stat_total += row[cur_stat]
            if stat_count:
                result[stat] = stat_total/stat_count

    if len(result):
        result["rating"] = row["rating"]
    
    return result

def aggregate(df, role):
    """
    Aggregate a data frame for the given role by combining same statistics across different heroes

    args:
        df: a data frame
        role: a string
    
    return:
        X: a data frame of predictors (features, aggregated)
        y: pd.series of response
    """

    aggregated = df.apply(aggregate_by_role, role = "tank", axis = 1)
    new_df = pd.DataFrame.from_dict(aggregated.tolist(), orient = "columns")

    # drop columns whose missing data percentage is greater than threshold
    for col in new_df.columns.values:
        missing = get_missing_percent(new_df, col)
        if missing > THRESHOLD:
            new_df = new_df.drop(col, axis = 1)
            
    # fill missing values with 0
    new_df.fillna(0, inplace = True)
    # split the data frame into predictors and response
    X = new_df.drop("rating", axis = 1)
    y = new_df["rating"]

    return X, y

if __name__ == "__main__":
    tank_train = pd.read_csv(DATA_PATH + "tank_train.csv")
    tank_test = pd.read_csv(DATA_PATH + "tank_test.csv")
    damage_train = pd.read_csv(DATA_PATH + "damage_train.csv")
    damage_test = pd.read_csv(DATA_PATH + "damage_test.csv")
    support_train = pd.read_csv(DATA_PATH + "support_train.csv")
    support_test = pd.read_csv(DATA_PATH + "support_test.csv")

    train_lst = {"tank": tank_train, "damage": damage_train, "support": support_train}
    test_lst = {"tank": tank_test, "damage": damage_test, "support": support_test}

    for role in ROLES:
        train_X, train_y = aggregate(train_lst[role], role)
        test_X, test_y = aggregate(test_lst[role], role)

        with open(f"{role}_train_X.pickle", "wb") as handle:
            pickle.dump(train_X, handle)

        with open(f"{role}_train_y.pickle", "wb") as handle:
            pickle.dump(train_y, handle)

        with open(f"{role}_test_X.pickle", "wb") as handle:
            pickle.dump(test_X, handle)

        with open(f"{role}_test_y.pickle", "wb") as handle:
            pickle.dump(test_y, handle)

        