import json
from flask import request, jsonify
from app import app
from app.services import (
    get_all_items, get_item_by_id, create_item,
    update_item, delete_item, fetch_and_save
)
from app.requester import fetch_products, search_products

# ---------------------------------------------------------------
# INVENTORY CRUD
# ---------------------------------------------------------------

@app.route("/inventory", methods=["GET"])
def list_inventory():
    try:
        return jsonify(get_all_items())
    except Exception as e:
        app.logger.exception("Failed to list inventory")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        item = get_item_by_id(item_id)
    except Exception:
        app.logger.exception("Failed to get item %s", item_id)
        return jsonify({"error": "Internal server error"}), 500

    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(force=True, silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON object"}), 400
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        item = create_item(data)
    except ValueError as e:
        # e.g. validation errors raised by the service layer
        return jsonify({"error": str(e)}), 400
    except Exception:
        app.logger.exception("Failed to create item")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        item = update_item(item_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        app.logger.exception("Failed to update item %s", item_id)
        return jsonify({"error": "Internal server error"}), 500

    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    try:
        item = delete_item(item_id)
    except Exception:
        app.logger.exception("Failed to delete item %s", item_id)
        return jsonify({"error": "Internal server error"}), 500

    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})


# ---------------------------------------------------------------
# EXTERNAL API HELPER ROUTES
# ---------------------------------------------------------------

@app.route("/external/search", methods=["GET"])
def search_external():
    barcode = (request.args.get("barcode") or "").strip()
    name = (request.args.get("name") or "").strip()

    if barcode:
        try:
            product = fetch_products(barcode)
        except Exception:
            app.logger.exception("External fetch failed for barcode %s", barcode)
            return jsonify({"error": "External service error"}), 502

        if product:
            return jsonify(product)
        return jsonify({"error": "Product not found"}), 404

    if name:
        try:
            products = search_products(name)
        except Exception:
            app.logger.exception("External search failed for name %s", name)
            return jsonify({"error": "External service error"}), 502
        return jsonify(products)

    return jsonify({"error": "Provide barcode or name"}), 400


@app.route("/external/add", methods=["POST"])
def add_external():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON object"}), 400

    barcode = (data.get("barcode") or "").strip()
    if not barcode:
        return jsonify({"error": "Barcode required"}), 400

    try:
        item = fetch_and_save(barcode)
    except Exception:
        app.logger.exception("Failed to fetch/save barcode %s", barcode)
        return jsonify({"error": "Internal server error"}), 500

    if not item:
        return jsonify({"error": "Failed to fetch or save product"}), 404
    return jsonify(item), 201