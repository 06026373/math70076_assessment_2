# Comparing expected goal statistics to real goals: can we deduce player's competence

This project is a data science's student project.

In the last decades, a statistic called "[expected Goal](https://en.wikipedia.org/wiki/Expected_goals)" (xG), has been developed. It represents the likelihood of a shot being scored and is based on several factor like the distance to the goal, the body part used, the distance to the closest defender, \dots It has been constantly improved by new studies during the last decades. However, this likelihood is not just due to luck: the difference in individual competence of each player also plays a significant role. Some players consistently outperform their expected goals, suggesting superior finishing skills, decision-making under pressure, \dots.

This project aims to see if a player scoring more or less than there expected goal can be due to a personal competence of simply luck. To do this we will construct a Bayesian hierarchical model to try to measure the competence of the players during their shots. Then we will modify our model to also include a defensive competence from the opposing team.

We will use the data from the Premier League, saisons 23/24 and 22/23. We will load the data from the website [FBREF](https://fbref.com), which contains a lot of data about each matchs in several leagues.

As the website [FBREF](https://fbref.com) contains a lot of data for many leagues and many years, I have developed a package to scrap easily any league and any saison. This package allows any person to scrap the data they want to create their own analysis, their own statistics, \dots

## Motivation

Quantifying such competence is important for coachs who want to select the best player, or who want to improve the performance of their players. So if a difference in competence is proven, it might be interesting for coachs to use and improve such analysis.

## Organization

- `data` contains the .csv files used for the analysis
- `output` contains the results of the analysis (.csv files)
- `scrapingFBREF` contains the package to scrap the website FBREF
- `collecting_datasets.py` is the code I used to scrap the data needed on the website FBREF
- `main.Rmd` is the notebook with the analysis
- `main.pdf` is the output of the notebook, the code is at the end