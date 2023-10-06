# Standard Library
import asyncio
import json
import logging
import pathlib
import sys

# First Party
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
    with open(output_file, "w") as f:
        json.dump(
            fuel_price_list.model_dump(), f, ensure_ascii=False, separators=(",", ":")
        )


if __name__ == "__main__":
    main()
