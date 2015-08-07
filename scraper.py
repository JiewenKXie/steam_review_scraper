import requests
from bs4 import BeautifulSoup
import re

class scraper():
    def __init__(self):
        self.game_name_for_appid = {}

    def get_top_games_by_player_count(self):
        url = 'http://store.steampowered.com/stats/'
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('a',class_="gameLink")
        for item in links:
            url = item['href']
            game_name = item.get_text().encode('utf-8')
            # print url, game_name
            m = re.search('app/(\d+)/',url)
            if m:
                self.game_name_for_appid[m.group(1)] = game_name



if __name__ == "__main__":
    s = scraper()
    s.get_top_games_by_player_count()

    for item in s.game_name_for_appid:
        print item, s.game_name_for_appid[item]


# http://store.steampowered.com//appreviews/570?start_offset=5&day_range=180&filter=all&language=english
# http://store.steampowered.com//appreviews/570?start_offset=0&day_range=180&filter=funny&language=english
