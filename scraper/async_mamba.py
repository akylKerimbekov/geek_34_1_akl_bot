import asyncio

import httpx
from parsel import Selector

from database.sql_commands import Database


class KeyNews:
    def __init__(self, title, href):
        self.__title = title
        self.__href = href

    @property
    def title(self):
        return self.__title

    @property
    def href(self):
        return self.__href

    def __str__(self):
        return f"Key News title: {self.__title}, link: {self.__href}"


class AsyncMambaScraper:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    URL = 'https://www.prnewswire.com/news-releases/news-releases-list/?page={page}&pagesize=25'
    NEWS_XPATH = '//div[@class="row newsCards"]/div/a'
    LINK_XPATH = '//div[@class="row newsCards"]/div/a/@href'
    TITLE_XPATH = '//div[@class="row newsCards"]/div/a/div[2]/h3/text()'
    PLUS_URL = 'https://www.prnewswire.com'
    DATE_XPATH = '//h3/small/text()'



    async def async_generator(self, limit):
        for page in range(1, limit + 1):
            yield page

    async def parse_pages(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            async for page in self.async_generator(limit=2):
                await self.get_url(
                    client=client,
                    url=self.URL.format(
                        page=page
                    )
                )

    async def get_url(self, client, url):
        response = await client.get(url)
        print(response.url)
        await self.scrape_links(html=response.text, client=client)

    async def scrape_links(self, html, client):
        key_words = Database().sql_select_all_keyword_query()
        words = [item['word'] for item in key_words]
        print(words)

        tree = Selector(text=html)
        for news in tree.xpath(self.NEWS_XPATH):
            link = news.xpath('./@href').get()

            title_full = news.xpath('string(./div[2]/h3)').get().strip()
            time_text = news.xpath('string(./div[2]/h3/small)').get().strip()
            title = title_full.replace(time_text, '').strip()

            if any(word.lower() in title.lower() for word in words):
                print("A word from the list is present in the text.")
                Database().sql_insert_key_news_query(
                    title=title,
                    href=self.PLUS_URL + link
                )


if __name__ == "__main__":
    scraper = AsyncMambaScraper()
    asyncio.run(scraper.parse_pages())
