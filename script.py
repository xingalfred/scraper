import asyncio
import datetime
import pathlib
from typing import Any

import pandas as pd

from scraper.client import Client
from scraper.model import FuelType, Store, FuelPrice

client = Client()
loop = asyncio.get_event_loop()

store_id_to_store: dict[str, Store] = {}

store_data = loop.run_until_complete(client.get_stores())

for store in store_data.stores:
    store_id_to_store[store.storeId] = store

best_fuel_prices: dict[FuelType, FuelPrice] = {}

fuel_price_data_list = loop.run_until_complete(
    client.get_fuel_prices(store_id_to_store.keys(), loop)
)

for fuel_price_data in fuel_price_data_list:
    for fuel_price in fuel_price_data.data:
        if fuel_price.ean not in best_fuel_prices:
            best_fuel_prices[fuel_price.ean] = fuel_price

        if best_fuel_prices[fuel_price.ean].price < fuel_price.price:
            continue

        best_fuel_prices[fuel_price.ean] = fuel_price

rows: list[dict[str, Any]] = []
for fuel_type, fuel_price in best_fuel_prices.items():
    store = store_id_to_store[fuel_price.storeNo]

    row = {
        "type": fuel_price.ean.name,
        "price": fuel_price.price / 10,
        "latitude": store.location[0],
        "longitude": store.location[1],
        "name": store.name,
        "city": store.address.suburb,
        "state": store.address.state,
        "postcode": store.address.postcode,
    }
    rows.append(row)

df = pd.DataFrame(rows)
print(df)
df.to_csv(pathlib.PurePath("latest.csv"), index=False, mode="w")
