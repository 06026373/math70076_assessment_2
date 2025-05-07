# scrapingFBREF

**scrapingFBREF** is a web scraping package that scrap the website [FBREF](https://fbref.com/en/). This website contains the results of football matches from many leagues in different countries, with a lot of details for some leagues like the Premier League (in UK) or La Liga (in Spain).

## Installation

You must install the package from source.

### Install from Source (GitHub)

```bash
git clone ...
cd scrapingFBREF
pip install .
```

## Documentation

### Scraping

You can use the function `scraping` to collect the data of the players on all the matches for a given league, between two given dates (the last date is not scraped).

#### Example

```python
from scrapingFBREF import scrapingFBREF
import pandas as pd

# Scrap results for the matches in Premier League for the 29th October 2027 and 30th October 2027
df = scraping("2017-10-29", "2017-10-31","Premier League")
df.head(5)
```

### Cleaning

You can use several functions to clean the dataset:
- `simple_position`: Add a new column (Simple_Position), with only 3 different position
- `accent_removal`: Add a new column (Player_clear), with the players' names without accent, to avoid problem during analysis
- `winner`: Add a new column (Point_won), takes the value 1 if the team has won, 0.5 for a draw, 0 for a loss
- `remove_goalkeepers`: Remove the Goalkeeper from the dataset

#### Example

```python
from scrapingFBREF import simple_position, accent_removal, winner, remove_goalkeepers
from scrapingFBREF import scrapingFBREF
import pandas as pd

# Scrap results for the matches in Premier League for the 29th October 2027 and 30th October 2027
df = scraping("2017-10-29", "2017-10-31","Ligue 2", ["summary"])
df.head(5)

# Clean the dataset
df = remove_goalkeepers(df)
df = simple_position(df)
df = accent_removal(df)
df = winner(df)
df.head(5)
```