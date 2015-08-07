import requests

class scraper():
    def __init__(self):
        pass

    def get_top_games_by_player_count(self):
        url = 'http://store.steampowered.com/stats/'
        r = requests.get(url)
        print r.text.encode('utf-8')

if __name__ == "__main__":
    s = scraper()
    s.get_top_games_by_player_count()
