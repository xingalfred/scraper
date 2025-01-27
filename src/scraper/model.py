import datetime
import enum

import msgspec


class StoreAddress(msgspec.Struct):
    address1: str
    address2: str
    suburb: str
    state: str
    postcode: str | None


class Store(msgspec.Struct):
    storeId: str
    name: str
    location: tuple[float, float]
    address: StoreAddress


class StoresResponse(msgspec.Struct):
    stores: list[Store]


class FuelType(enum.Enum):
    U91 = "52"
    U95 = "55"
    U98 = "56"
    E10 = "57"
    Diesel = "53"
    LPG = "54"


class FuelPrice(msgspec.Struct):
    ean: FuelType
    price: int
    priceDate: datetime.datetime
    isRecentlyUpdated: bool
    storeNo: str


class FuelPricesResponse(msgspec.Struct):
    data: list[FuelPrice]
