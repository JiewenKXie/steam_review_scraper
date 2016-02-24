# Steam review scraper

# Requirements

Python 2.7+

    pip install requests beautifulsoup4 unicodecsv

lxml [Windows](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml), [other os](http://lxml.de/installation.html)

## Usage

    python scraper.py app_id

## Output

    csv file: `reviews_{app_id}.csv`

    max. count (default = 1000)

## Method

    s.get_all_reviews_for_appid(app_id='427820', type='all')

where type is one of the following:

type = ['all' (Helpful),'positive','negative','funny','recent']
