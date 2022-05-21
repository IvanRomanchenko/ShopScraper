# Shop Scraper 
#### _Сlothing stores scraper to help filling the database of thematic websites_  

## Start:
```sh
git clone 
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
cd ShopScraper/app/
```

## Setting up
#### Choose the suitable for you pipeline in `ShopScraper/settings.py` or all simultaneously. Just uncomment needed.
##### _For RedisWriterPipeline, you need to install and run Redis_
```python
ITEM_PIPELINES = {
   # 'ShopScraper.pipelines.JsonWriterPipeline': 300,
   'ShopScraper.pipelines.JsonLineWriterPipeline': 400,
   # 'ShopScraper.pipelines.RedisWriterPipeline': 500,
}
```

## Usage
#### Run command to start scraping
```sh
scrapy crawl macys --nolog
```
