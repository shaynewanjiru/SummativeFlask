from flask import request, jsonify
from app import app
from app.services import (
    get_all_items, get_item_by_id, create_item,
    update_item, delete_item, fetch_and_save
)
from app.requester import fetch_products, search_products

#  INVENTORY CRUD

@app.route("/inventory", methods=["GET"])
def list_inventory():
    return jsonify(get_all_items())

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = get_item_by_id(item_id)   # <-- was get_item(item_id), now get_item_by_id
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
 
    if data is None and request.data:
        try:
            import json
            data = json.loads(request.data)
        except:
            pass
    
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON object"}), 400
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    item = create_item(data)
    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    item = update_item(item_id, data)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    item = delete_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})

#  EXTERNAL API HELPER ROUTES 

@app.route("/external/search", methods=["GET"])
def search_external():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    
    if barcode:
        product = fetch_products(barcode)
        if product:
            return jsonify(product)
        return jsonify({"error": "Product not found"}), 404
    
    if name:
        products = search_products(name)
        return jsonify(products)
    
    return jsonify({"error": "Provide barcode or name"}), 400

@app.route("/external/add", methods=["POST"])
def add_external():
    data = request.get_json()
    barcode = data.get("barcode") if data else None
    
    if not barcode:
        return jsonify({"error": "Barcode required"}), 400
    
    item = fetch_and_save(barcode)
    if not item:
        return jsonify({"error": "Failed to fetch or save product"}), 404
    return jsonify(item), 201