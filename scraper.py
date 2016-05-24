import requests
from bs4 import BeautifulSoup
import codecs
import unicodecsv
import sys

class scraper():
    def __init__(self):
        self.day_range = '9223372036854776000'
        self.language = 'english'
        self.recommendation_ids = []
        self.max_reviews = 1000
        self.csv_unicode_writer = None

        if len(sys.argv) > 1:
            self.get_all_reviews_for_appid(sys.argv[1])
        else:
            print "usage scraper.py app_id"

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
                recommendation_id = json['recommendationids'][index]
                if recommendation_id in self.recommendation_ids:
                    continue
                else:
                    has_new_data = True
                    self.recommendation_ids.append(recommendation_id)
                if len(self.recommendation_ids) > self.max_reviews:
                    return False
                persona_name = review.find('div',class_="persona_name").get_text(strip=True).replace("\n",'|')
                posted_date = review.find('div',class_="postedDate").get_text(strip=True)
                row = [app_id, json['recommendationids'][index], posted_date, type, persona_name, review_text ]
                if self.csv_unicode_writer is None:
                    self.init_unicodecsv('reviews_' + app_id + '.csv')
                self.csv_unicode_writer.writerow(row)
            print len(self.recommendation_ids)
            return has_new_data
        else:
            raise Exception("error, invalid json response")
            

    def init_unicodecsv(self,filename=None):
        if filename is None:
            filename = 'steam_reviews.csv'
        self.csv_fh = codecs.open(filename, 'wb')
        self.csv_fh.write(u'\uFEFF'.encode('utf8'))
        self.csv_unicode_writer = unicodecsv.writer(self.csv_fh, encoding='utf-8')
        header = ['app_id','review_id','date','type','username','review_text']
        self.csv_unicode_writer.writerow(header)

    def get_all_reviews_for_appid(self,app_id=None,type=None):
        self.get_reviews_for_appid(app_id, type, 0)
        self.get_reviews_for_appid(app_id, type, 5)
        offset = 25
        while self.get_reviews_for_appid(app_id, type, offset):
            offset += 25

if __name__ == "__main__":
    s = scraper()
    
    # s.get_all_reviews_for_appid('427820', type='all')
