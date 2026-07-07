

from app.database import inventory

def reset_database(seed_data=None):
    """Reset the global inventory list in-place."""
    inventory[:] = seed_data if seed_data else []

def seed_inventory():
    return [
        {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "ingredients_text": "...", "quantity": 10, "barcode": "025293600107"},
        {"id": 2, "product_name": "Nutella", "brands": "Ferrero", "ingredients_text": "...", "quantity": 25, "barcode": "3017620422003"},
        {"id": 3, "product_name": "Coca-Cola", "brands": "Coca-Cola", "ingredients_text": "...", "quantity": 50, "barcode": "049000050103"}
    ]