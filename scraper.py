import requests
from bs4 import BeautifulSoup

class scraper():
    def __init__(self):
        pass

    def get_top_games_by_player_count(self):
        url = 'http://store.steampowered.com/stats/'
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('a',class_="gameLink")
        for item in links:
            print item['href'], item.get_text().encode('utf-8')


if __name__ == "__main__":
    s = scraper()
    s.get_top_games_by_player_count()
