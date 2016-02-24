# Steam review scraper

## Usage

    python scraper.py app_id

## Output

    csv file: `reviews_{app_id}.csv`

    max. count (default = 1000)

## Method

    s.get_all_reviews_for_appid(app_id='427820', type='all')

where type is one of the following:

type = ['all' (Helpful),'positive','negative','funny','recent']

# Requirements

Python 2.7+

    pip install requests beautifulsoup4 unicodecsv
