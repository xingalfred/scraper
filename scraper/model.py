from __future__ import annotations

import datetime

import enum
import pydantic


class FuelType(enum.Enum):
    U91 = "52"
    U95 = "55"
    U98 = "56"
    E10 = "57"
    DIESEL = "53"
    LPG = "54"


class FuelPriceResponse(pydantic.BaseModel):
    ean: FuelType
    price: int
    priceDate: datetime.datetime
    isRecentlyUpdated: bool
    storeNo: str


class FuelPriceDataResponse(pydantic.BaseModel):
    data: list[FuelPriceResponse]


class AddressResponse(pydantic.BaseModel):
    address1: str
    address2: str
    suburb: str
    state: str
    postcode: str | None


class StoreResponse(pydantic.BaseModel):
    storeId: str
    name: str
    location: tuple[float, float]
    address: AddressResponse


class StoreDataResponse(pydantic.BaseModel):
    stores: list[StoreResponse]


class FuelPrice(pydantic.BaseModel):
    type: str
    price: float
    latitude: float
    longitude: float
    name: str
    city: str
    state: str
    postcode: str

    @classmethod
    def build(cls, store: StoreResponse, price: FuelPriceResponse) -> FuelPrice:
        return FuelPrice(
            type=price.ean.name,
            price=price.price / 10,
            latitude=store.location[0],
            longitude=store.location[1],
            name=store.name,
            city=store.address.suburb,
            state=store.address.state,
            postcode=store.address.postcode,
        )


class FuelPriceList(pydantic.BaseModel):
    data: list[FuelPrice]
    last_modified: int

    @classmethod
    def build(
        cls,
        store_price_list: list[tuple[StoreResponse, FuelPriceResponse]],
        timestamp: datetime.datetime,
    ) -> FuelPriceList:

        data = [FuelPrice.build(store, price) for store, price in store_price_list]

        return FuelPriceList(data=data, last_modified=timestamp.timestamp())
