import asyncio

import httpx
from parsel import Selector


class Good:
    def __init__(self, good_id, brand, desc):
        self.__good_id = good_id
        self.__brand = brand
        self.__desc = desc

    @property
    def good_id(self):
        return self.__good_id

    @property
    def brand(self):
        return self.__brand

    @property
    def desc(self):
        return self.__desc

    def __str__(self):
        return f"Good id: {self.__good_id}, brand: {self.__brand}, description: {self.__desc}"


class AsyncNewsScraper:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    URLS = {
        "KOBIETA": 'https://www.decathlon.pl/kobieta/kurtki-damskie?from={page}&size=39',
        "MEZCZYZNA": 'https://www.decathlon.pl/mezczyzna/kurtki-meskie?from={page}&size=39',
        "DZIECKO": 'https://www.decathlon.pl/dziecko/kurtki-dzieciece?from={page}&size=39'
    }

    BASE_XPATH = '//*[@id="app"]/main/div[2]/div[1]/section/div/div[{row}]'
    ID_XPATH = BASE_XPATH + '/@data-supermodelid'
    BRAND_XPATH = BASE_XPATH + '/div[3]/a[1]/strong/text()'
    DESC_XPATH = BASE_XPATH + '/div[3]/a[1]/span/text()'

    async def async_generator(self, limit):
        for page in range(0, 39 * (limit + 1), 39):
            yield page

    async def parse_pages(self, target_url):
        result = []
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            async for page in self.async_generator(limit=3):
                goods = await self.get_url(
                    client=client,
                    url=target_url.format(page=page)
                )
                result.extend(goods)
        return result

    async def get_url(self, client, url):
        response = await client.get(url)
        print(response.url)
        return await self.scrape_links(html=response.text, client=client)

    async def scrape_links(self, html, client):
        tree = Selector(text=html)
        result = []
        for row in range(39):
            good_id = tree.xpath(self.ID_XPATH.format(row=row)).get()
            if good_id:
                brand = tree.xpath(self.BRAND_XPATH.format(row=row)).get()
                description = tree.xpath(self.DESC_XPATH.format(row=row)).get()
                result.append(Good(good_id, brand, description))
        return result


async def gather():
    tasks = []
    for key, url in AsyncNewsScraper.URLS.items():
        scraper = AsyncNewsScraper()
        task = scraper.parse_pages(target_url=url)
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return {key: result for key, result in zip(AsyncNewsScraper.URLS.keys(), results)}


if __name__ == "__main__":
    category_results = asyncio.run(gather())
    for category, goods in category_results.items():
        print(f"Category: {category}: {len(goods)}")
