import asyncio
import datetime
import json
import pathlib
from typing import Any

import pandas as pd

from scraper import scraper
from scraper.model import FuelPriceList

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

store_price_list = loop.run_until_complete(scraper.get_fuel_prices())

fuel_price_list = FuelPriceList.build(store_price_list, datetime.datetime.now())

print(fuel_price_list)
with open(pathlib.PurePath("latest.json"), "w") as f:
    json.dump(fuel_price_list.dict(), f, ensure_ascii=False, separators=(",", ":"))

rows: list[dict[str, Any]] = []
for store, fuel_price in store_price_list:

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
