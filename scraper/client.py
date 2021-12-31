import asyncio.events
from collections import Iterable
from urllib import parse

import aiohttp

from scraper import model


class Client:
    def __init__(self):
        self.base_url: str = "https://www.7eleven.com.au/storelocator-retail/mulesoft/"

    async def get_stores(self) -> model.StoreData:
        url = parse.urljoin(self.base_url, "stores")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                response_text = await response.text()
                return model.StoreData.parse_raw(response_text)

    async def _get_fuel_prices(
        self, store_no: str, session: aiohttp.ClientSession
    ) -> model.FuelPriceData:
        url = parse.urljoin(self.base_url, "fuelPrices")
        params = {"storeNo": store_no}

        async with session.get(url, params=params) as response:
            response.raise_for_status()
            response_text = await response.text()
            return model.FuelPriceData.parse_raw(response_text)

    async def get_fuel_prices(
        self, store_numbers: Iterable[str], loop: asyncio.events.AbstractEventLoop
    ) -> list[model.FuelPriceData]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                loop.create_task(self._get_fuel_prices(store_no, session))
                for store_no in store_numbers
            ]
            return await asyncio.gather(*tasks)
