import asyncio
import datetime
import json
import pathlib

from scraper import scraper
from scraper.model import FuelPriceList

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

store_price_list = loop.run_until_complete(scraper.get_fuel_prices())

fuel_price_list = FuelPriceList.build(store_price_list, datetime.datetime.now())

print(fuel_price_list)
with open(pathlib.PurePath("latest.json"), "w") as f:
    json.dump(fuel_price_list.dict(), f, ensure_ascii=False, separators=(",", ":"))
