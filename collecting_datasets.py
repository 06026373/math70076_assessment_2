from scrapingFBREF import *

def collect():
    """
    Scrap the folowing league : 
    - Premier League, saison 23/24 and 22/23
    - Ligue 1, saison 23/24 and 22/23
    """
    df = scrapingFBREF("2023-08-12", "2024-05-20","Premier League")
    df = simple_position(df)
    df = accent_removal(df)
    df = winner(df)
    df = remove_goalkeepers(df)
    df.to_csv('data/Premier_League2324.csv', index = False)
    df = scrapingFBREF("2022-08-06", "2023-05-29","Premier League")
    df = simple_position(df)
    df = accent_removal(df)
    df = winner(df)
    df = remove_goalkeepers(df)




if __name__ == "__main__":
    collect()