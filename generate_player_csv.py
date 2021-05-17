import json
import pandas as pd
import numpy as np
from io import StringIO
from csv import writer  

from parse_player_stats import ROLES_LISTS, ROLES_STATS, ROLES
from parse_player_stats import TANK_DATA, DAMAGE_DATA, SUPPORT_DATA


# path to the folder with text files storing player data for each role
# files in these folders are outputs from parse_player_stats.py and
# contain data in a nested dictionary form that needs to be flattened
TANK_DATA_FOLDER = "parsed_stats/" 
DAMAGE_DATA_FOLDER = "parsed_stats/"
SUPPORT_DATA_FOLDER = "parsed_stats/"

ROLES_FOLDERS = dict(zip(ROLES, [TANK_DATA_FOLDER, DAMAGE_DATA_FOLDER, SUPPORT_DATA_FOLDER]))

ROLES_OUTFILES = {role : ROLES_FOLDERS[role] + role + '_data.csv' for role in ROLES}

ROLES_DATA = dict(zip(ROLES, [TANK_DATA, DAMAGE_DATA, SUPPORT_DATA]))


# TO-DO: flatten the dictionary
# TO-DO: produce one csv file for each role

ROLE_ATTRIBUTES = {}

INTERVAL = 500

# from https://stackoverflow.com/questions/23981553/get-all-values-from-nested-dictionaries-in-python

def NestedDictValues(dictionary):
    """ Returns a list of values from a nested dictionary as a list
    """
    for value in dictionary.values():
        if isinstance(value, dict):
            yield from NestedDictValues(value)
        else:
            yield value


def get_attributes(role):
    """ Get flattened attribute list from the stats file for 
        a particular role, as well as nested dict of attributes
    """

    # rating is a separate stat, so add it separately
    attributes = ["rating"]
    attributes_nested = {hero : [] for hero in ROLES_LISTS[role]}

    for hero in ROLES_LISTS[role]:

        # timePlayed is currently not within any category in role_STATS
        # so need to add it manually
        attributes.append(hero + '_' + 'timePlayed')
        attributes_nested[hero].append('timePlayed')

        for stats_for_hero in ROLES_STATS[role][hero].values():
            # stats_for_hero is a list of attributes within some category for this hero
            for statName in stats_for_hero:
                attributes.append(hero + '_' + statName)
                attributes_nested[hero].append(statName)

    return attributes, attributes_nested


def generate_df(role):
    """ Parses all rows in role_DATA and puts in flattened DataFrame

    args:
        role -- role for which to create df

    return:
        pd.DataFrame with flattened data
    """

    attributes, attributes_nested = get_attributes(role)

    # df = pd.DataFrame(columns = attributes)
    output = StringIO()
    csv_writer = writer(output)
    with open(ROLES_DATA[role], "r") as infile:
        
        for i, line in enumerate(infile):

            if i % INTERVAL == 0:
                print(f"[generate_df]: {role} : processes {i} rows")

            dict_line = json.loads(line)

            # take the rating value separately of any roles
            values_line = [dict_line[attributes[0]]]

            for hero in ROLES_LISTS[role]:
                if hero not in dict_line:
                    # player hasn't played this hero
                    # add nans to the df
                    values_line += [np.nan] * len(attributes_nested[hero])
                else:
                    # player played this hero
                    # go over all the attributes for this hero and append values
                    for attr in attributes_nested[hero]:
                        # for some reason, some players miss some attributes
                        # even for the hero they played, so just appending
                        # dict_line[hero].values() doesn't work
                        if attr in dict_line[hero]:
                            values_line.append(dict_line[hero][attr])
                        else:
                            values_line.append(np.nan)

            csv_writer.writerow(values_line)
            # df.loc[i] = values_line

    output.seek(0)
    df = pd.read_csv(output, names=attributes)

    return df


if __name__ == "__main__":

    for role in ROLES:
        df = generate_df(role)
        df.to_csv(ROLES_OUTFILES[role])
        print(role, ": dataframe shape is ", df.shape)
