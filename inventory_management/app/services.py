from app.database import inventory
from app.requester import fetch_product

def get_items():
    return inventory

def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def create_item(data):
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
