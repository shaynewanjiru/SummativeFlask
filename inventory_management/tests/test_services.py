import unittest

from app.services import (
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item
)


class TestServices(unittest.TestCase):

    def test_get_all_items(self):
        items = get_all_items()
        assert type(items) == list
        assert len(items) > 0

    def test_get_item_by_id(self):
        item = get_item_by_id(1)
        assert item["id"] == 1
        assert item["product_name"] == "Organic Almond Milk"

    def test_create_item(self):
        new_item = {
            "product_name": "Bread",
            "brands": "Sunblest",
            "quantity": 20,
            "ingredients_text": "Filtered water",
            "barcode": "01234598701"
                }

        item = create_item(new_item)

        assert item["product_name"] == "Bread"
        assert item["brands"] == "Sunblest"
        assert item["quantity"] == 20
        assert item["ingredients_text"] == "Filtered water"
        assert item["barcode"] == "01234598701"

    def test_update_item(self):
        item = update_item(1, {"quantity": 100})

        assert item["quantity"] == 100

    def test_delete_item(self):
        item = delete_item(2)

        assert item["id"] == 2
        assert get_item_by_id(2) is None


if __name__ == "__main__":
    unittest.main()