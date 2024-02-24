import datetime
import enum


import pydantic


class StoreAddress(pydantic.BaseModel):
    address1: str
    address2: str
    suburb: str
    state: str
    postcode: str | None


class Store(pydantic.BaseModel):
    storeId: str
    name: str
    location: tuple[float, float]
    address: StoreAddress


class StoresResponse(pydantic.BaseModel):
    stores: list[Store]


class FuelType(enum.Enum):
    U91 = "52"
    U95 = "55"
    U98 = "56"
    E10 = "57"
    Diesel = "53"
    LPG = "54"


class FuelPrice(pydantic.BaseModel):
    ean: FuelType
    price: int
    priceDate: datetime.datetime
    isRecentlyUpdated: bool
    storeNo: str


class FuelPricesResponse(pydantic.BaseModel):
    data: list[FuelPrice]
