from unidecode import unidecode
import pandas as pd

def simple_position_1(position):
    """
    This function simplifies the position of the players
    to only forward, midfielders, defenders.

    Parameters:
    position (str): the position of the player given by FBREF

    Return:
    str: the simplified position
    """
    if not isinstance(position, str):
        raise TypeError("Str must be entered.")
    position = position[:2]
    if position in ['FW','LW','RW']:
        return 'Forward'
    elif position in ['DF','FB','LB','RB','CB','WB']:
        return 'Defenders'
    elif position in ['MF','AM','DM','CM','LM','RM','WM']:
        return 'Midfielders'
    elif position == 'GK':
        return 'GK'
    else:
        raise ValueError("The value entered correspond to none of the values known")

def simple_position(df):
    """
    This function returns a new dataset with simplified position.

    Parameters:
    df (data.frame): original data frame

    Return:
    (data.frame): data frame with simplified position
    """
    df['Simple_Position'] = df['Position'].apply(simple_position_1)
    return df

def accent_removal_1(name):
    """
    This function remove accent from players' name.

    Parameters:
    position (str): Name of the player

    Return:
    str: name without accent
    """
    if not isinstance(name, str):
        raise TypeError("String must be entered.")
    return unidecode(name)

def accent_removal(df):
    """"
    This function returns a new dataset with players name without accent (to avoid mistake).

    Parameters:
    df (data.frame): original data frame

    Return:
    (data.frame): data frame with name without accent
    """
    df['Player'] = df['Player'].apply(accent_removal_1)
    return df

def winner_1(row):
    """
    This function determines wich teams won, or if there is an equality and return points accordingly.
    (1 for win, .5 for draw, 0 for loss)

    Parameter:
    row (list): a row of the dataset

    Return:
    float: point marked
    """
    if not isinstance(row, pd.Series):
        raise TypeError("pd.Series must be entered.")
    if row["id_team_A"] == row["team tag"]:
        if row["score_team_A"] > row["score_team_B"]:
            return 1.
        elif row["score_team_A"] == row["score_team_B"]:
            return 0.5
        else: 
            return 0.
    else:
        if row["score_team_B"] > row["score_team_A"]:
            return 1.
        elif row["score_team_B"] == row["score_team_A"]:
            return 0.5
        else:
            return 0.
#######
def winner(df):
    """
    This function returns a new column with the point won (1 for win, 0.5 for draw, 0 for loss).

    Parameters:
    df (data.frame): original data frame

    Return:
    (data.frame): data frame with point won
    """
    df['Point_won'] = df.apply(winner_1, axis=1)
    return df
  
def remove_goalkeepers(df):
    """
    Remove the goalkeepers from the dataset.

    Parameters:
    df (data.frame): the dataframe with the statistics of the players

    Return:
    (data.frame): the dataframe without the goalkeepers. 
    """
    return df.loc[df['Position'] != 'GK']