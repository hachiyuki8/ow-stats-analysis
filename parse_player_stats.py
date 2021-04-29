TANK_JSON = "tank_json.txt" # file name to store all JSON objects for tanks
DAMAGE_JSON = "damage_json.txt" # file name to store all JSON objects for damages
SUPPORT_JSON = "support_json.txt" # file name to store all JSON objects for supports

ROLES = ["tank", "damage", "support"] # list of roles
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