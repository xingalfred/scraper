import logging
from urllib import parse


import httpx


from scraper import api

logger = logging.getLogger(__name__)


class Client:
    def __init__(self) -> None:
        self._base_url: str = "https://www.7eleven.com.au/storelocator-retail/mulesoft/"
        self._client = httpx.AsyncClient()

    async def get_stores(self) -> api.StoresResponse:
        url = parse.urljoin(self._base_url, "stores")
        request = httpx.Request("GET", url=url)
        logger.info("Sending %s", request)

        response = await self._client.send(request)
        response.raise_for_status()

        stores = api.StoresResponse.model_validate_json(response.text)

        return stores

    async def get_fuel_prices(self, store_number: str) -> api.FuelPricesResponse:
        url = parse.urljoin(self._base_url, "fuelPrices")
        params = {"storeNo": store_number}
        request = httpx.Request("GET", url=url, params=params)
        logger.info("Sending %s", request)

        response = await self._client.send(request)
        response.raise_for_status()

        fuel_prices = api.FuelPricesResponse.model_validate_json(response.text)

        return fuel_prices
