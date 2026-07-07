import requests

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student project)"
}

def fetch_products(barcode):
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
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": name,
        "json": 1,
        "page_size": 5
    }
    try:
        response = requests.get(url, params = params, timeout = 5)
        return response.json().get("products", [])
    except Exception:
        return []


