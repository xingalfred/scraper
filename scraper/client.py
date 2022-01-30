import asyncio.events
from typing import Iterable
from urllib import parse

import aiohttp

from scraper import model


class Client:
    def __init__(self):
        self._base_url: str = "https://www.7eleven.com.au/storelocator-retail/mulesoft/"

    async def get_stores(self) -> model.StoreDataResponse:
        url = parse.urljoin(self._base_url, "stores")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                response_text = await response.text()
                store_data = model.StoreDataResponse.parse_raw(response_text)

                return store_data

    async def _get_fuel_prices(
        self, store_no: str, session: aiohttp.ClientSession
    ) -> model.FuelPriceDataResponse:
        url = parse.urljoin(self._base_url, "fuelPrices")
        params = {"storeNo": store_no}

        async with session.get(url, params=params) as response:
            response.raise_for_status()
            response_text = await response.text()
            fuel_price_data = model.FuelPriceDataResponse.parse_raw(response_text)

            return fuel_price_data

    async def get_fuel_prices(
        self, store_numbers: Iterable[str]
    ) -> list[model.FuelPriceDataResponse]:
        async with aiohttp.ClientSession() as session:
            coroutines = [
                self._get_fuel_prices(store_no, session) for store_no in store_numbers
            ]
            fuel_price_data_list = await asyncio.gather(*coroutines)

            return fuel_price_data_list
