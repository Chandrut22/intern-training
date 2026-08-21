
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class University(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    state_province: str | None = Field(
        default=None,
        alias="state-province",
    )

    name: str
    domains: list[str]
    alpha_two_code: str
    web_pages: list[HttpUrl]
    country: str


class RequestModel(BaseModel):
    type: str
    query: str
    language: str
    unit: str


class LocationModel(BaseModel):
    name: str
    country: str
    region: str
    lat: str
    lon: str
    timezone_id: str
    localtime: str
    localtime_epoch: int
    utc_offset: str


class AstroModel(BaseModel):
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: int


class AirQualityModel(BaseModel):
    co: str
    no2: str
    o3: str
    so2: str
    pm2_5: str
    pm10: str
    us_epa_index: str = Field(alias="us-epa-index")
    gb_defra_index: str = Field(alias="gb-defra-index")


class CurrentWeatherModel(BaseModel):
    observation_time: str
    temperature: int
    weather_code: int
    weather_icons: list[str]
    weather_descriptions: list[str]

    astro: AstroModel
    air_quality: AirQualityModel

    wind_speed: int
    wind_degree: int
    wind_dir: str
    pressure: int
    precip: float
    humidity: int
    cloudcover: int
    feelslike: int
    uv_index: int
    visibility: int
    is_day: str


class WeatherResponse(BaseModel):
    request: RequestModel
    location: LocationModel
    current: CurrentWeatherModel


class MetaModel(BaseModel):
    last_updated_at: str


class CurrencyModel(BaseModel):
    code: str
    value: float


class CurrencyResponse(BaseModel):
    meta: MetaModel
    data: dict[str, CurrencyModel]
