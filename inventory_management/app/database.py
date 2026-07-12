inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar...",
        "quantity": 10,
        "barcode": "012345678901"
    },
    {
        "id": 2,
        "product_name": "Cottage cheese",
        "brands": "Opco",
        "ingredients_text": "milk, vinegar",
        "quantity": 60,
        "barcode": "7928374298928"
    },
    {
        "id": 3,
        "product_name": "Coca-Cola Classic",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, high fructose corn syrup, caramel color, phosphoric acid, natural flavors, caffeine",
        "quantity": 50,
        "barcode": "049000050103"
    },
    {
        "id": 4,
        "product_name": "Greek Yogurt Plain",
        "brands": "Chobani",
        "ingredients_text": "Cultured nonfat milk, live and active cultures",
        "quantity": 20,
        "barcode": "894700010045"
    },
    {
        "id": 5,
        "product_name": "Spaghetti Pasta",
        "brands": "Barilla",
        "ingredients_text": "Semolina wheat, durum wheat flour",
        "quantity": 35,
        "barcode": "076808502947"
    }
]

# Optional but recommended: catch this kind of typo automatically at import time
_barcodes = [item["barcode"] for item in inventory]
_ids = [item["id"] for item in inventory]
assert len(_barcodes) == len(set(_barcodes)), "Duplicate barcode found in seed inventory data"
assert len(_ids) == len(set(_ids)), "Duplicate id found in seed inventory data"
for _item in inventory:
    assert "brands" in _item, f"Item id {_item.get('id')} is missing 'brands' key"
    assert "product_name" in _item, f"Item id {_item.get('id')} is missing 'product_name'"