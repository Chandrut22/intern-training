import os

import httpx
from dotenv import load_dotenv
from pydantic import TypeAdapter
from schemas import CurrencyResponse, University, WeatherResponse

load_dotenv()

UNIVERSITY_BASE_URL = "http://universities.hipolabs.com"

WEATHER_BASE_URL = "https://api.weatherstack.com"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

CURRENCY_BASE_URL = "https://api.currencyapi.com"
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

UniversityList = TypeAdapter(list[University])


def get_universities(
    client: httpx.Client,
    name: str,
    country: str = "",
) -> list[University] | None:

    try:
        response = client.get(
            "/search",
            params={
                "name": name,
                "country": country,
            },
        )

        print("URL:", response.url)
        print("Status:", response.status_code)

        response.raise_for_status()

        universities = UniversityList.validate_python(response.json())

        print(f"Found {len(universities)} universities")

        for university in universities:
            print(f"\nName: {university.name}")
            print(f"Country: {university.country}")
            print(f"Code: {university.alpha_two_code}")
            print(f"State: {university.state_province}")
            print(f"Domains: {university.domains}")
            print(f"Web Pages: {university.web_pages}")

        return universities

    except httpx.TimeoutException:
        print("University API request timed out.")
        return []

    except httpx.HTTPStatusError as e:
        print(f"University API returned HTTP error: {e.response.status_code}")
        print("Response:", e.response.text)
        return []

    except httpx.RequestError as e:
        print(f"University API request failed: {e}")
        return []

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


with httpx.Client(
    base_url=UNIVERSITY_BASE_URL,
    timeout=10.0,
) as client:
    get_universities(
        client,
        name="middle",
        country="",
    )


def get_india_cities(client: httpx.Client, location: str) -> WeatherResponse | None:
    try:
        response = client.get(
            "/current",
            params={"access_key": os.getenv("WEATHER_API_KEY"), "query": location},
        )
        print("\nURL:", response.url)
        print("Status:", response.status_code)
        response.raise_for_status()
        city = WeatherResponse.model_validate(response.json())

        print(f"""
            City: {city.location.name}
            Country: {city.location.country}
            Region: {city.location.region}

            Temperature: {city.current.temperature}°C
            Feels Like: {city.current.feelslike}°C
            Condition: {city.current.weather_descriptions[0]}
            Humidity: {city.current.humidity}%
            Wind: {city.current.wind_speed} km/h {city.current.wind_dir}
            Pressure: {city.current.pressure} hPa
            Visibility: {city.current.visibility} km
            UV Index: {city.current.uv_index}

            Sunrise: {city.current.astro.sunrise}
            Sunset: {city.current.astro.sunset}

            Air Quality:
            CO: {city.current.air_quality.co}
            NO2: {city.current.air_quality.no2}
            O3: {city.current.air_quality.o3}
            SO2: {city.current.air_quality.so2}
            PM2.5: {city.current.air_quality.pm2_5}
            PM10: {city.current.air_quality.pm10}

            Local Time: {city.location.localtime}
            """)

        return city

    except httpx.TimeoutException:
        print("API request timed out.")
        return []

    except httpx.HTTPStatusError as e:
        print(f"API returned HTTP error: {e.response.status_code}")
        print("Response:", e.response.text)
        return []

    except httpx.RequestError as e:
        print(f"API request failed: {e}")
        return []

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


with httpx.Client(
    base_url=WEATHER_BASE_URL,
    timeout=30.0,
) as client:
    cities = get_india_cities(client, "Chennai")


def get_currency_rate(
    client: httpx.Client, baseCurrency: str, date: str, currencies: str
) -> CurrencyResponse | None:
    try:
        response = client.get(
            "/v3/historical",
            params={
                "base_currency": baseCurrency,
                "date": date,
                "currencies": currencies,
            },
            headers={"apiKey": CURRENCY_API_KEY},
        )
        print("\nURL:", response.url)
        print("Status:", response.status_code)
        response.raise_for_status()
        data = CurrencyResponse.model_validate(response.json())
        return data

    except httpx.TimeoutException:
        print("API request timed out.")
        return []

    except httpx.HTTPStatusError as e:
        print(f"API returned HTTP error: {e.response.status_code}")
        print("Response:", e.response.text)
        return []

    except httpx.RequestError as e:
        print(f"University API request failed: {e}")
        return []

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


with httpx.Client(base_url=CURRENCY_BASE_URL, timeout=10.0) as client:
    response = get_currency_rate(client, "USD", "2026-08-9", "")
    print(f"Last Updated: {response.meta.last_updated_at}")

    print("\nCurrencies:")
    for currency_code, currency in response.data.items():
        print(f"{currency.code}: {currency.value}")
