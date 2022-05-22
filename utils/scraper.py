import time
import asyncio
from typing import Optional

import aiohttp

from .models import WebsiteParser

class Scraper:

    BASE = "https://fungenerators.com/random/facts/"
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML," 
                 " like Gecko) Chrome/81.0.4044.138 Safari/537.36")

    def __init__(self, session: Optional[aiohttp.ClientSession]):
        self.session = session

    async def _require_session(self) -> None:
        if (self.session is None) or (self.session and self.session.closed):
            self.session = aiohttp.ClientSession()

    async def get_head(self, endpoint) -> WebsiteParser:
        await self._require_session()
        url = self.BASE + endpoint
        async with self.session.get(url, headers={'User-Agent': self.USER_AGENT}) as response:
            text = await response.text()
            return WebsiteParser(text, "lxml")

    async def scrape(self) -> str:
        website_parser = await self.get_head("space")
        fact = website_parser.get_head(2, {'class': 'wow'})
        return fact.text


async def test_main():
    start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        scraper = Scraper(session)
        parser = await scraper.scrape()
        print(parser)
    end = time.perf_counter()
    print(f"Time taken: {end - start}")

if __name__ == "__main__":
    asyncio.run(test_main())