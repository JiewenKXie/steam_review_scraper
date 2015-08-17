Steam review scraper

This script gets reviews for the current top 100 steam games shown on the store stats page, and outputs the data to a csv file. By default it will output 20 reviews per page. It is possible to choose type of review to output.

# Usage

## get reviews by app id

    s.get_reviews_for_appid(appid='730', offset=0, type='funny')

## get reviews for top 100 games with app ids

    s.get_reviews_for_all_games(type='all',pages=5)

type = ['all' (Helpful),'positive','negative','funny','recent']

reviews = pages * 20

output is sorted by appid ascending.

# Requirements

Python 2.7+

    pip install requests beautifulsoup4 unicodecsv
