import logging
from urllib import parse


import httpx
import msgspec

from scraper.model import FuelPricesResponse, StoresResponse
from httpx_limiter import AsyncRateLimitedTransport

logger = logging.getLogger(__name__)


class Client:
    def __init__(self) -> None:
        self._base_url: str = "https://www.7eleven.com.au"
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            transport=AsyncRateLimitedTransport.create(rate=5, capacity=10),
        )
        self._decoder = msgspec.json.Decoder()

    async def get_stores(self) -> StoresResponse:
        url = parse.urljoin(self._base_url, "/storelocator-retail/mulesoft/stores")
        request = self._client.build_request("GET", url=url)
        logger.info("Sending %s", request)

        response = await self._client.send(
            request,
        )
        response.raise_for_status()

        decoded = msgspec.json.decode(response.text, type=StoresResponse)

        return decoded

    async def get_fuel_prices(self, store_number: str) -> FuelPricesResponse:
        url = parse.urljoin(self._base_url, "/storelocator-retail/mulesoft/fuelPrices")
        params = {"storeNo": store_number}
        request = self._client.build_request("GET", url=url, params=params)
        logger.info("Sending %s", request)

        response = await self._client.send(request)
        response.raise_for_status()

        decoded = msgspec.json.decode(response.text, type=FuelPricesResponse)

        return decoded
