import datetime

import msgspec

from scraper.model import FuelPricesResponse, FuelType, StoresResponse


def test_store_data() -> None:
    with open("tests/store_data.json") as f:
        result = msgspec.json.decode(f.read(), type=StoresResponse)

    assert len(result.stores) == 712
    assert result.stores[0].storeId == "4221"
    assert result.stores[0].name == "Taigum"
    assert result.stores[0].location == (-27.34234, 153.04181)
    assert result.stores[0].address.address1 == "377 Handford Road"
    assert result.stores[0].address.address2 == ""
    assert result.stores[0].address.suburb == "Taigum"
    assert result.stores[0].address.state == "QLD"
    assert result.stores[0].address.postcode == "4018"


def test_fuel_price_data() -> None:
    with open("tests/fuel_price_data.json") as f:
        result = msgspec.json.decode(f.read(), type=FuelPricesResponse)

    assert len(result.data) == 5
    assert result.data[0].ean == FuelType.U91
    assert result.data[0].price == 1699
    assert result.data[0].priceDate == datetime.datetime.fromisoformat("2021-05-08T05:10:00+10:00")
    assert result.data[0].isRecentlyUpdated is True
    assert result.data[0].storeNo == "1286"
