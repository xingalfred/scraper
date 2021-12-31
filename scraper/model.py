import datetime
import enum
from typing import Optional

import pydantic


class FuelType(enum.Enum):
    U91 = "52"
    Diesel = "53"
    LPG = "54"
    U95 = "55"
    U98 = "56"
    E10 = "57"


class FuelPrice(pydantic.BaseModel):
    ean: FuelType
    price: int
    priceDate: datetime.datetime
    isRecentlyUpdated: bool
    storeNo: str


class FuelPriceData(pydantic.BaseModel):
    data: list[FuelPrice]


class Address(pydantic.BaseModel):
    address1: str
    address2: str
    suburb: str
    state: str
    postcode: Optional[str]


class Store(pydantic.BaseModel):
    storeId: str
    name: str
    location: tuple[float, float]
    address: Address


class StoreData(pydantic.BaseModel):
    stores: list[Store]
