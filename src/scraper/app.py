import asyncio
import logging
import pathlib
import sys

import msgspec


from scraper import scraper

root_logger = logging.getLogger()
root_logger.setLevel(level=logging.INFO)


def main() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    fuel_price_list = asyncio.run(scraper.get_fuel_price_list())

    build_dir = pathlib.Path("build")
    build_dir.mkdir(exist_ok=True)

    output_file = build_dir / "fuel_prices.json"
    with open(output_file, "wb") as f:
        encoded_json = msgspec.json.encode(fuel_price_list)
        f.write(encoded_json)
