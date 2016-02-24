import requests
from bs4 import BeautifulSoup
import re
import codecs
import unicodecsv

class scraper():
    def __init__(self):
        self.game_name_for_appid = {}
        self.init_unicodecsv()
        self.day_range = 180
        self.language = 'english'

        self.recommendation_ids = []

    def get_reviews_for_appid(self,app_id=None,type=None,offset=0):
        if type is None:
            type = 'all'

        url = 'http://store.steampowered.com//appreviews/{0}?start_offset={1}&day_range={2}&filter={3}&language={4}'
        url = url.format(app_id,offset,self.day_range,type,self.language)
        print url
        r = requests.get(url)
        json = r.json()
        if json.get('success') == 1:
            # print json['html'].encode('utf-8')
            soup = BeautifulSoup(json['html'], "lxml")
            review_box = soup.find_all('div',class_="review_box")
            index = -1
            has_new_data = False
            for review in review_box:
                index += 1
                review_text = review.find('div',class_="content").get_text(strip=True).replace('\n','|')
                # print json['recommendationids'][index], review_text.encode('utf-8') + "\n"
                # print review_text.encode('utf-8')
                recommendation_id = json['recommendationids'][index]
                print recommendation_id
                if recommendation_id in self.recommendation_ids:
                    continue
                else:
                    has_new_data = True
                    self.recommendation_ids.append(recommendation_id)
                persona_name = review.find('div',class_="persona_name").get_text(strip=True).replace("\n",'|')
                row = [app_id, self.game_name_for_appid.get(app_id), json['recommendationids'][index], type, persona_name, review_text ]
                self.csv_unicode_writer.writerow(row)
            return has_new_data

    def init_unicodecsv(self,filename=None):
        if filename is None:
            filename = 'steam_reviews.csv'
        self.csv_fh = codecs.open(filename, 'wb')
        self.csv_fh.write(u'\uFEFF'.encode('utf8'))
        self.csv_unicode_writer = unicodecsv.writer(self.csv_fh, encoding='utf-8')
        header = ['appid','game_name','id','type','username','text']
        self.csv_unicode_writer.writerow(header)

    def get_reviews_for_top_100_games(self,type=None,pages=1):
        self.get_top_games_by_player_count()
        if type is None:
            type = 'all'
        count = 1
        for appid in sorted(self.game_name_for_appid,key=int):
            for page in range(pages):
                print count, page, appid, self.game_name_for_appid[appid]
                offset = page * 20
                self.get_reviews_for_appid(appid, offset=offset, type=type)
            count = count + 1

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

    def get_all_reviews_for_appid(self,app_id,type):
        offset = 0
        while self.get_reviews_for_appid(app_id, type, offset):
            offset += 25

if __name__ == "__main__":
    s = scraper()

    s.get_all_reviews_for_appid('427820', type='all')
