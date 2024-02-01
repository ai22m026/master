# Abmessungen Generali Arena
PITCH_X = 105
PITCH_X_HALF = PITCH_X / 2.0
PITCH_Y = 68
PITCH_Y_HALF = PITCH_Y / 2.0


#General constants
FOLDERNAME = 'input_data'
FILE_NAME = 'AUT_RAW_GAME_OPT$2239802.TXT'
FILE_NAME_REL = FOLDERNAME + '/' + FILE_NAME


# Deterministic Approach constants
POSESSION_RADIUS = 1  # 1m
DUAL_ZONE_RADIUS = 1  # 1m



class_colors = {
    '0': 'blue',  # Team A
    '1': 'green',  # Team B
    '2': 'red',  # Ref
    '3': 'yellow', # Goalie Team A
    '4': 'black', # Goalie Team B
    '5': 'gold', # Ball
}