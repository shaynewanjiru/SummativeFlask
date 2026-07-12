from app.database import inventory
from app.requester import fetch_products


REQUIRED_FIELDS = ("product_name",)


def get_all_items():
    # Return a shallow copy so external code can't mutate our internal list
    return list(inventory)


def get_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def _validate_quantity(value):
    """Ensure quantity is a non-negative integer. Raises ValueError if not."""
    if isinstance(value, bool): 
        raise ValueError("quantity must be a number, not a boolean")
    try:
        qty = int(value)
    except (TypeError, ValueError):
        raise ValueError("quantity must be a valid integer")
    if qty < 0:
        raise ValueError("quantity cannot be negative")
    return qty


def _validate_new_item_data(data):
    for field in REQUIRED_FIELDS:
        if not data.get(field):
            raise ValueError(f"'{field}' is required")


def create_item(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dict")

    _validate_new_item_data(data)

    highest_id = 0
    for item in inventory:
        if item["id"] > highest_id:
            highest_id = item["id"]

    new_id = highest_id + 1
    new_item = {"id": new_id}

    for key, value in data.items():
        if key == "id":
            # Never let the caller set/override the generated id
            continue
        new_item[key] = value


    new_item["quantity"] = _validate_quantity(new_item.get("quantity", 0))

    inventory.append(new_item)
    return new_item


def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if not item:
        return None

    if "quantity" in data:
        data = dict(data)  # avoid mutating caller's dict
        data["quantity"] = _validate_quantity(data["quantity"])

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
    # Prevent duplicate imports of the same barcode
    for item in inventory:
        if item.get("barcode") == barcode:
            return item  # already have it, return existing instead of duplicating

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