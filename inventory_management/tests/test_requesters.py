from unittest.mock import patch
from app.requester import fetch_products, search_products


@patch("app.requester.requests.get")
def test_fetch_products(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero"
        }
    }

    product = fetch_products("3017620422003")

    assert product["product_name"] == "Nutella"
    assert product["brands"] == "Ferrero"


@patch("app.requester.requests.get")
def test_search_products(mock_get):
    mock_response = mock_get.return_value
    
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {"product_name": "Nutella", "brands": "Ferrero"},
            {"product_name": "Nutella Biscuits", "brands": "Ferrero"}
        ]
    }
    
    products = search_products("nutella")
    
    assert len(products) == 2
    assert products[0]["product_name"] == "Nutella"

    assert len(products) == 2
    assert products[0]["product_name"] == "Nutella"