from scraper.client import Client
from scraper.model import FuelPriceResponse, FuelType, StoreResponse


async def get_fuel_prices() -> list[tuple[StoreResponse, FuelPriceResponse]]:
    client = Client()

    store_data = await client.get_stores()
    store_id_to_store: dict[str, StoreResponse] = {
        store.storeId: store for store in store_data.stores
    }

    fuel_price_data_list = await client.get_fuel_prices(store_id_to_store.keys())

    best_fuel_prices: dict[FuelType, FuelPriceResponse] = {}

    for fuel_price_data in fuel_price_data_list:

        for fuel_price in fuel_price_data.data:
            if fuel_price.ean not in best_fuel_prices:
                best_fuel_prices[fuel_price.ean] = fuel_price
                continue

            if best_fuel_prices[fuel_price.ean].price >= fuel_price.price:
                best_fuel_prices[fuel_price.ean] = fuel_price

    store_price_list: list[tuple[StoreResponse, FuelPriceResponse]] = []
    for fuel_type in FuelType:
        fuel_price_data = best_fuel_prices[fuel_type]
        store = store_id_to_store[fuel_price_data.storeNo]
        store_price_list.append((store, fuel_price_data))

    return store_price_list
