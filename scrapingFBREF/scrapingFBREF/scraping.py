import bs4
import lxml
import urllib
from urllib import request
import time
from datetime import datetime, date
from tqdm import tqdm
import pandas as pd

def scrapingFBREF(date_start, date_end, league, 
                  table_list = ["summary","passing","passing_types","defense","possession","misc"]):
    """
    Scraps the website FBREF, collecting the information about all the matches in a given league, between
    two dates (the end date is not scraped).

    Parameters:
    date_start (str): format: yyyy-mm-dd
    date_end (str): format: yyyy-mm-dd, not scraped
    league (str): league chosen (as written on the website FBREF)
    table_list (list[str]): list with the name of the table to scrap (inspect FBREF to chose: if there is 
    only one table, write ["summary"])

    Return:
    (data.frame): Table with all the data about the players
    """
    # Initialization and test
    if not isinstance(date_start, str):
        raise TypeError("String must be entered for date_start, date_end and league.")
    if not isinstance(date_end, str):
        raise TypeError("String in 'YYYY-MM-DD' format must be entered for date_start, date_end and league.")
    if not isinstance(league, str):
        raise TypeError("String in 'YYYY-MM-DD' format must be entered for date_start, date_end and league.")
    if not isinstance(table_list, list):
        raise TypeError("List of string must be entered for table_list")
    url = 'https://fbref.com/fr/matchs/' + date_start
    url_end = 'https://fbref.com/fr/matchs/' + date_end
    league = league + '">'
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
    delta_date = (date_end - date_start).days
    if delta_date <= 0:
        raise ValueError("The end date must be after the start date")
    if (date_end-date.today()).days >= 0 or (date_start-datetime.strptime("1900-01-01", '%Y-%m-%d').date()).days <0:
        raise ValueError("The dates are not possible. You must enter date between 1/01/1900 and yesterday")
    progress_bar = tqdm(total=delta_date, desc="Scrapping the matchs list")
    Refs_Matchs = []
    # Find all the urls of the matches played
    while url != url_end:
        time.sleep(7) # important, otherwise the website is blocked
        Refs_Matchs_update, url = scraping_league(url, league)
        progress_bar.update(1)
        Refs_Matchs += Refs_Matchs_update
    progress_bar.close()
    # Scrap the tables for each match
    df_league = pd.DataFrame()
    for tag in tqdm(Refs_Matchs, "Scraping the data"):
        time.sleep(5) # important, otherwise the website is blocked
        url_match = 'https://fbref.com/en/matchs/' + tag
        df_match = scrap_match(url_match, table_list)
        df_league = pd.concat([df_league, df_match], ignore_index = False)
    return df_league

def scraping_league(url, league):
    """
    Scrap the url of all the matches that append at a precise day, in a league.

    Parameters:
    url (str): url of the form "https://fbref.com/fr/matchs/yyyy-mm-dd" (replace yyyy-mm-dd with the chosen date)
    league (str): league chosen (as written on the website FBREF)

    Return:
    (list): List of all the urls of the matches
    """
    Refs_Matchs = []
    request_text = request.urlopen(url).read() 
    page = bs4.BeautifulSoup(request_text, 'lxml')
    L1=page.find_all('div',class_ = 'table_wrapper')
    L2=[]
    for e in L1:
        # Find all the league
        L2.append(e.find('span').text)
    if league in L2:
        urls_matchs=L1[L2.index(league)].find_all('td',attrs={'data-stat' : 'match_report'})
        for e in urls_matchs:
            # Take the reference of the match, it is enough to find the page of the match
            Refs_Matchs.append(e.find('a')['href'].split('/')[3])   
    # Next page
    url='https://fbref.com'+page.find('a',class_ = 'button2 next')['href']
    return Refs_Matchs, url

def scrap_match(url_match, table_list):
    """
    Scrap the information for a given match.

    Parameters:
    url_match (str): url of the form: "https://fbref.com/en/matchs/tag/" (replace tag with the tag of the match)
    table_list: a list of the tables to be scraped (inspect FBREF to chose: if there is 
    only one table, write ["summary"])

    Return:
    (data.frame): Table with all the data about the players
    """
    # Open the page
    request_text = request.urlopen(url_match).read() 
    page = bs4.BeautifulSoup(request_text, "lxml")

    
    def scrap_table(table):
        """
        This function scraps the dataframe of a given table for a match.

        Parameters:
        table (str): the name of the table

        Return:
        (data.frame): the statistics of the players in this table
        """
 
        # id of both team
        List_link = []
        scorebox = page.find("div", {"class": "scorebox"})
        strong_scorebox = scorebox.find_all('strong', {'class': None})
        for tag in strong_scorebox :
            team = tag.find("a")
            if team :
                link = team.get('href') # url of the page for both team
                List_link.append(link)

        Tag_team = []
        for link in List_link[:len(List_link)-1]: # The 3rd element is useless
            elements = link.split('/')
            Tag_team.append(elements[3])

        # Scrap the score of the match
        all_score = scorebox.find_all('div',{"class": "score"})
        match_score = [int(score.text) for score in all_score]
        final_table = pd.DataFrame()

        for tag in Tag_team : 
            idtable = "div_stats_" + tag + "_" + table # table id uses team tag
            tableau_resume = page.find(id = idtable)
            table_tbody = tableau_resume.find("tbody")
            rows = table_tbody.find_all('tr')

            dico_joueur = dict()
            for i in range(len(rows)):
                tag_player = rows[i].find("th")['data-append-csv']
                cols = [ele.text.strip() for ele in rows[i]] # Scrap all the stat on each line
                cols.insert(0,tag_player)
                if len(cols) > 0 : 
                    dico_joueur[cols[0]] = cols[1:]
        
            # Name of each columns
            header = tableau_resume.find("thead")
            var = header.find_all('tr')
            var2 = var[1].find_all("th")
            var_list = [(var2[i]['aria-label']) for i in range(len(var2))]

            # Concatenate the table of each team        
            table_tag = (pd.DataFrame.from_dict(dico_joueur,orient='index'))
            table_tag.columns = var_list
            table_tag['team tag'] = tag
            table_tag['match tag'] = url_match.split('/')[5]
            table_tag['player tag'] = table_tag.index.tolist() #Add the player tag
            final_table = pd.concat([final_table,table_tag], ignore_index = False)
    
        # Add the score of each teams
        final_table['id_team_A'] = Tag_team[0]
        final_table['score_team_A'] = match_score[0]
        final_table['id_team_B'] = Tag_team[1]
        final_table['score_team_B'] = match_score[1]

        return final_table

    # Scrape all the tables and combine them in one dataset
    match_table = scrap_table(table_list[0])  # Scrap the first table
    # Scrap the other tables and combine them 
    for table in range(1,len(table_list)):
        type_table = scrap_table(table_list[table])
        # These columns are present in all tables: (so we supress them)
        suffix = ['score_team_A', 'id_team_B', 'Age', 
                    'match tag', 'id_team_A', 'Position', 
                    'Nation', 'Minutes', 'player tag', 
                    'score_team_B', 'Shirt Number', "team tag"] 
        type_table = type_table.drop(columns=suffix)
        match_table = pd.merge(match_table, type_table, on = "Player")
    return match_table
