from app.database import inventory
from app.requester import fetch_products

def get_all_items():
    return inventory

def get_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def create_item(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dict")
    highest_id = 0
    for item in inventory:
        if item["id"] > highest_id:
            highest_id = item["id"]

    new_id = highest_id +1
    new_item ={"id": new_id}

    for key, value in data.items():
        new_item[key] = value 

    inventory.append(new_item)

    return new_item    

def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if not item:
        return None
    for key, value in data.items():
        if key != "id":
            item[key] = value 
    return item     


def delete_item(item_id):
    item_to_delete = get_item_by_id(item_id)
    if item_to_delete is None:
        return None

    inventory.remove(item_to_delete) 
    return item_to_delete

def fetch_and_save(barcode):
    """
    Business rule: When we import from OpenFoodFacts,
    we start with quantity = 0 because we haven't stocked it yet.
    """
    product = fetch_products(barcode)
    if not product:
        return None
    item = {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "quantity": 0,
        "barcode": barcode
            }
    return create_item(item)

