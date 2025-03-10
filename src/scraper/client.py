import datetime
import logging

import httpx
import msgspec
import stamina
from httpx_limiter import AsyncRateLimitedTransport

from scraper.model import FuelPricesResponse, StoresResponse

logger = logging.getLogger(__name__)


class Client:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            base_url="https://www.7eleven.com.au",
            transport=AsyncRateLimitedTransport.create(rate=5, capacity=5),
        )
        self._decoder = msgspec.json.Decoder()

    async def get_stores(self) -> StoresResponse:
        request = self._client.build_request("GET", url="/storelocator-retail/mulesoft/stores")

        response = await self._send_request(request=request)

        decoded = msgspec.json.decode(response.text, type=StoresResponse)

        return decoded

    async def get_fuel_prices(self, store_number: str) -> FuelPricesResponse:
        params = {"storeNo": store_number}
        request = self._client.build_request(
            "GET", url="/storelocator-retail/mulesoft/fuelPrices", params=params
        )

        response = await self._send_request(request=request)

        decoded = msgspec.json.decode(response.text, type=FuelPricesResponse)

        return decoded

    @stamina.retry(
        on=httpx.HTTPError,
        attempts=10,
        wait_initial=datetime.timedelta(seconds=5),
        wait_max=datetime.timedelta(seconds=60),
        wait_jitter=datetime.timedelta(seconds=0),
        wait_exp_base=2,
    )
    async def _send_request(self, request: httpx.Request) -> httpx.Response:
        response = await self._client.send(request=request)
        logger.info(response)
        logger.info(response.headers)
        response.raise_for_status()
        return response
