import asyncio
import datetime
import logging


from scraper import api
from scraper.client import Client
from scraper.decorators import duration
from scraper.model import FuelPrice, FuelPriceList

logger = logging.getLogger(__name__)


def get_cheapest_prices(
    stores: api.StoresResponse, prices_list: list[api.FuelPricesResponse]
) -> list[tuple[api.Store, api.FuelPrice]]:
    lowest_prices: dict[api.FuelType, api.FuelPrice] = {}
    for prices in prices_list:
        for price in prices.data:
            if (
                price.ean not in lowest_prices
                or lowest_prices[price.ean].price >= price.price
            ):
                lowest_prices[price.ean] = price

    store_id_to_store: dict[str, api.Store] = {
        store.storeId: store for store in stores.stores
    }

    store_price_list: list[tuple[api.Store, api.FuelPrice]] = []
    for fuel_type in api.FuelType:
        price = lowest_prices[fuel_type]
        store = store_id_to_store[price.storeNo]
        store_price_list.append((store, price))

    return store_price_list


def create_fuel_price_list(
    store_price_list: list[tuple[api.Store, api.FuelPrice]],
    timestamp: datetime.datetime,
) -> FuelPriceList:
    output = []

    for store, fuel_price in store_price_list:
        output.append(
            FuelPrice(
                type=fuel_price.ean.name,
                price=fuel_price.price / 10,
                latitude=store.location[0],
                longitude=store.location[1],
                name=store.name,
                city=store.address.suburb,
                state=store.address.state,
                postcode=store.address.postcode or "",
            )
        )

    return FuelPriceList(data=output, last_modified=int(timestamp.timestamp()))


@duration
async def get_fuel_price_list() -> FuelPriceList:
    client = Client()

    stores_response = await client.get_stores()

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(client.get_fuel_prices(store.storeId))
            for store in stores_response.stores
        ]
    prices_list = [task.result() for task in tasks]

    store_price_list = get_cheapest_prices(stores_response, prices_list)
    update_datetime = datetime.datetime.now()

    fuel_price_list = create_fuel_price_list(store_price_list, update_datetime)

    logger.info(fuel_price_list)

    return fuel_price_list
