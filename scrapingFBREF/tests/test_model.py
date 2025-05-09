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

def test_error():
    with pytest.raises(TypeError, match="String must be entered for date_start, date_end and league."):
        scrapingFBREF(2025, "2024-01-01", "Ligue 1")
        scrapingFBREF("2023-10-01", "2024-01-01", ['Ligue 1', 'Premier League'])
        scrapingFBREF("2017-10-30", "2017-10-31", "Premier League", "summary")
    with pytest.raises(ValueError, match="The end date must be after the start date"):
        scrapingFBREF("2017-10-30", "2015-10-31", "Premier League")
    with pytest.raises(ValueError, 
                       match="The dates are not possible. You must enter date between 1/01/1900 and yesterday"):
        scrapingFBREF("2026-01-01", "2027-01-01", "Premier League")

if __name__ == "__main__":
    pytest.main()