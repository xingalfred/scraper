import msgspec


class FuelPrice(msgspec.Struct):
    type: str
    price: float
    latitude: float
    longitude: float
    name: str
    city: str
    state: str
    postcode: str


class FuelPriceList(msgspec.Struct):
    data: list[FuelPrice]
    last_modified: int
