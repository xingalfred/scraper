import pydantic


class FuelPrice(pydantic.BaseModel):
    type: str
    price: float
    latitude: float
    longitude: float
    name: str
    city: str
    state: str
    postcode: str


class FuelPriceList(pydantic.BaseModel):
    data: list[FuelPrice]
    last_modified: int
