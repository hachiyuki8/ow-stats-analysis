import json
import pandas as pd

# path to the folder with text files storing player data for each role
# files in these folders are outputs from parse_player_stats.py and
# contain data in a nested dictionary form that needs to be flattened
TANK_DATA_FOLDER = "/tanks" 
DAMAGE_DATA_FOLDER = "/damages"
SUPPORT_DATA_FOLDER = "/supports"

# TO-DO: flatten the dictionary
# TO-DO: produce one csv file for each role

from parse_player_stats import ROLES_LISTS, ROLES_STATS
