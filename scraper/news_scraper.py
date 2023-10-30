import requests
from parsel import Selector
from database.sql_commands import Database
from scraper.news import News


class NewsScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    URL = 'https://m.akipress.org'
    HREF_XPATH = '//*[@id="content-tab"]/div[2]/div[1]/div/div[{row}]/a/@href'
    TITLE_XPATH = '//*[@id="content-tab"]/div[2]/div[1]/div/div[{row}]/a/@title'

    def parse_data(self, owner_telegram_id):
        html = requests.get(url=self.URL, headers=self.headers).text
        tree = Selector(text=html)
        result = []
        for news in range(10):
            title = tree.xpath(self.TITLE_XPATH.format(row=news)).extract_first()
            href = tree.xpath(self.HREF_XPATH.format(row=news)).extract_first()
            if title and href:
                row = Database().sql_insert_news_query(
                    owner_telegram_id=owner_telegram_id,
                    title=title,
                    href=href,
                )
                result.append(News(row["id"], owner_telegram_id, title, "http:" + href))

        return result
