import requests
from bs4 import BeautifulSoup
import re
import codecs
import unicodecsv

class scraper():
    def __init__(self):
        self.game_name_for_appid = {}
        self.init_unicodecsv()

    def get_top_games_by_player_count(self):
        url = 'http://store.steampowered.com/stats/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        links = soup.find_all('a',class_="gameLink")
        for item in links:
            url = item['href']
            game_name = item.get_text().encode('utf-8')
            m = re.search('app/(\d+)/',url)
            if m:
                self.game_name_for_appid[m.group(1)] = game_name

    def get_reviews_for_appid(self,appid=None,offset=0,type=None):
        if type is None:
            type = 'all'
        if appid is None:
            return
        url = 'http://store.steampowered.com/appreviews/%s?start_offset=%i&day_range=180&filter=%s&language=english' % (appid,offset,type)
        r = requests.get(url)
        json = r.json()
        if json.get('success') == 1:
            soup = BeautifulSoup(json['html'], "lxml")
            content = soup.find_all('div',class_="content")

            index = 0
            for item in content:
                review_text = item.get_text(strip=True).replace('\n','|')
                # print json['recommendationids'][index], review_text.encode('utf-8') + "\n"
                row = [appid, self.game_name_for_appid[appid], \
                       json['recommendationids'][index], type, review_text ]
                self.csv_unicode_writer.writerow(row)
                index = index + 1

    def init_unicodecsv(self,filename=None):
        if filename is None:
            filename = 'steam_reviews.csv'
        self.csv_fh = codecs.open(filename, 'wb')
        self.csv_fh.write(u'\uFEFF'.encode('utf8'))
        self.csv_unicode_writer = unicodecsv.writer(self.csv_fh, encoding='utf-8')
        header = ['appid','game_name','id','type','text']
        self.csv_unicode_writer.writerow(header)

    def get_reviews_for_all_games(self,type=None):
        self.get_top_games_by_player_count()
        if type is None:
            type = 'all'
        count = 1
        for appid in sorted(self.game_name_for_appid,key=int):
            print count, appid, self.game_name_for_appid[appid]
            self.get_reviews_for_appid(appid, offset=0, type=type)
            count = count + 1

if __name__ == "__main__":
    s = scraper()
    # s.get_top_games_by_player_count()

    # s.get_reviews_for_appid('730', 0, 'funny')
    s.get_reviews_for_all_games(type='funny')

# http://store.steampowered.com//appreviews/570?start_offset=5&day_range=180&filter=all&language=english
# http://store.steampowered.com//appreviews/570?start_offset=0&day_range=180&filter=funny&language=english
