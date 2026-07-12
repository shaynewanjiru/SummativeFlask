import re
import requests

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student project)"
}

BARCODE_PATTERN = re.compile(r"^\d{6,14}$")  # typical EAN/UPC barcode length


class ExternalServiceError(Exception):
    """Raised when the external API fails in a way distinct from 'no results'."""
    pass


def _validate_barcode(barcode):
    barcode = str(barcode).strip()
    if not BARCODE_PATTERN.match(barcode):
        raise ValueError("Invalid barcode format")
    return barcode


def fetch_products(barcode):
    try:
        barcode = _validate_barcode(barcode)
    except ValueError:
        print("Invalid barcode format:", barcode)
        return None

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=5)

        if response.status_code != 200:
            print("Status:", response.status_code)
            print(response.text)
            return None

        data = response.json()

        if data.get("status") == 1:
            return data["product"]

        return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


def search_products(name):
    if not name or not name.strip():
        return []

    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": name.strip(),
        "json": 1,
        "page_size": 5
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=5)

        if response.status_code != 200:
            print("Search status:", response.status_code)
            print(response.text)
            raise ExternalServiceError(f"OpenFoodFacts returned {response.status_code}")

        data = response.json()
        return data.get("products", [])

    except requests.exceptions.RequestException as e:
        print("Search request failed:", e)
        raise ExternalServiceError(str(e)) from e
    except ValueError as e:
        # response.json() failed to parse
        print("Search response was not valid JSON:", e)
        raise ExternalServiceError("Invalid response from OpenFoodFacts") from e