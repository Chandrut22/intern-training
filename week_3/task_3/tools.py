import httpx
from langchain.tools import tool

UNIVERSITY_BASE_URL = "http://universities.hipolabs.com"

@tool
def search_universities(name: str, country: str = ""):
    """Search for universities by name and optional country using the Hipolabs University API."""

    try:
        response = httpx.get(
            f"{UNIVERSITY_BASE_URL}/search",
            params={"name": name, "country": country},
            timeout=10.0,
        )
        response.raise_for_status()


        return response.json()

    except httpx.TimeoutException:
        print("University API request timed out.")
        return []
    except httpx.HTTPStatusError as e:
        print(f"University API returned HTTP error: {e.response.status_code}")
        return []
    except httpx.RequestError as e:
        print(f"University API request failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

@tool
def calculate(expression: str) -> float:
    """Perform a mathematical calculation from a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def search_country_states(name:str) -> dict:
        """Search for states by country name using the Countries Space API."""
        try:
            response = httpx.post(
                "https://countriesnow.space/api/v0.1/countries/states",
                json={"country": name},
                follow_redirects=True,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

            print("Status:", response.status_code)
            print("URL:", response.url)
            print("Response:", response.text)

            if(data["error"]): return data["msg"]
            return data["data"]
    
        except httpx.TimeoutException:
            print("API request timed out.")
            return []
        except httpx.HTTPStatusError as e:
            print(f"API returned HTTP error: {e.response.status_code}")
            return []
        except httpx.RequestError as e:
            print(f"API request failed: {e}")
            return []
        except Exception as e:
            print(f"error: {e}")
            return []