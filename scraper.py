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
        for item in self.game_name_for_appid:
            print item, self.game_name_for_appid[item]

    def get_reviews_for_appid(self,appid=None,offset=0,type=None):
        if type is None:
            type = 'all'
        if appid is None:
            return
        url = 'http://store.steampowered.com/appreviews/%s?start_offset=%i&day_range=180&filter=%s&language=english' % (appid,offset,type)
        # print url
        r = requests.get(url)
        json = r.json()
        if json.get('success') == 1:
            # print json
            html = json['html']
            soup = BeautifulSoup(html, "lxml")
            # print soup.text.encode('utf-8')
            content = soup.find_all('div',class_="content")
            for item in content:
                print item.get_text(strip=True).encode('utf-8') + "\n"


if __name__ == "__main__":
    s = scraper()
    # s.get_top_games_by_player_count()

    s.get_reviews_for_appid('730', 0, 'funny')




# http://store.steampowered.com//appreviews/570?start_offset=5&day_range=180&filter=all&language=english
# http://store.steampowered.com//appreviews/570?start_offset=0&day_range=180&filter=funny&language=english
