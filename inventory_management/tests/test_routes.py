def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_single_product(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_add_product(client):
    response = client.post("/inventory", json={
        "product_name": "Rice",
        "brands": "Daawat",
        "quantity": 40
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Rice"
    assert data["id"] == 4


def test_update_product(client):
    response = client.patch("/inventory/1", json={"quantity": 75})
    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 75
    assert data["product_name"] == "Organic Almond Milk"


def test_delete_product(client):
    response = client.delete("/inventory/3")
    assert response.status_code == 200
    
    # Verify it's actually gone
    response = client.get("/inventory/3")
    assert response.status_code == 404