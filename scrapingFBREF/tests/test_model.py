import pytest

from scrapingFBREF import *

def test():
    df = scrapingFBREF("2017-10-30", "2017-10-31", "Ligue 2", ["summary"])
    assert df['Player'].iloc[0] == 'Maxime Barthelmé'
    assert df.shape == (26,30)
    df = simple_position(df)
    df = accent_removal(df)
    df = remove_goalkeepers(df)
    df = winner(df)
    assert df.shape == (24, 32)
    assert df['Player'].iloc[0] == 'Maxime Barthelme'
    df = scrapingFBREF("2017-10-30", "2017-10-31", "Premier League")
    assert df.shape == (26, 129)

if __name__ == "__main__":
    pytest.main()