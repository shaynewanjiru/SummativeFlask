import requests
import subprocess
import sys
import time
import os
import atexit

BASE_URL = "http://127.0.0.1:5000"

# ── Server Lifecycle Management ─────────────────────────────

_server_process = None
_we_started_server = False


def _is_server_running():
    """Check if Flask is already listening."""
    try:
        requests.get(f"{BASE_URL}/inventory", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False


def _start_server():
    """Launch Flask in a background process."""
    global _server_process, _we_started_server

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_path = os.path.join(root_dir, "run.py")

    if not os.path.exists(run_path):
        print(f"[ERROR] Could not find {run_path}")
        print("Make sure run.py is in the project root folder.")
        return False

    print(">>> Starting Flask server automatically...")
    print(f">>> Command: python {run_path}")

    if sys.platform == "win32":
        _server_process = subprocess.Popen(
            [sys.executable, run_path],
            cwd=root_dir,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        _server_process = subprocess.Popen(
            [sys.executable, run_path],
            cwd=root_dir
        )

    for i in range(10):
        time.sleep(1)
        if _is_server_running():
            print(">>> Server is ready at http://127.0.0.1:5000\n")
            _we_started_server = True
            return True
        print(f">>> Waiting for server... ({i + 1}/10)")

    print("[ERROR] Server failed to start.")
    return False


def _stop_server():
    """Kill the server if WE started it."""
    global _server_process
    if _we_started_server and _server_process:
        print("\n>>> Shutting down Flask server...")
        _server_process.terminate()
        try:
            _server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _server_process.kill()
        _server_process = None


atexit.register(_stop_server)


def ensure_server():
    """Guarantee the server is reachable before showing the menu."""
    if _is_server_running():
        print(">>> Connected to existing Flask server.\n")
        return True
    return _start_server()


# ── API Helpers ───────────────────────────────────────────

def api_get(path, params=None):
    try:
        return requests.get(f"{BASE_URL}{path}", params=params, timeout=5)
    except Exception as e:
        print(f"[ERROR] Could not reach server: {e}")
        return None


def api_post(path, json_data):
    try:
        return requests.post(f"{BASE_URL}{path}", json=json_data, timeout=5)
    except Exception as e:
        print(f"[ERROR] Could not reach server: {e}")
        return None


def api_patch(path, json_data):
    try:
        return requests.patch(f"{BASE_URL}{path}", json=json_data, timeout=5)
    except Exception as e:
        print(f"[ERROR] Could not reach server: {e}")
        return None


def api_delete(path):
    try:
        return requests.delete(f"{BASE_URL}{path}", timeout=5)
    except Exception as e:
        print(f"[ERROR] Could not reach server: {e}")
        return None


def safe_json(response):
    """Parse JSON safely; returns None (and prints a warning) on failure
    instead of crashing the CLI."""
    try:
        return response.json()
    except ValueError:
        print("[ERROR] Server returned an invalid response (not JSON).")
        return None


def prompt_item_id(label="Enter item ID: "):
    """Prompt for an item ID and validate it's an integer before hitting the API."""
    raw = input(label).strip()
    if not raw.isdigit():
        print("Invalid ID — must be a whole number.")
        return None
    return raw


# ####################################################################

def print_menu():
    print("\n" + "=" * 40)
    print("  INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. View Inventory")
    print("2. View Product")
    print("3. Add Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Search OpenFoodFacts")
    print("7. Exit")
    print("=" * 40)


def view_inventory():
    response = api_get("/inventory")
    if response is None:
        return
    if response.status_code != 200:
        print("Server error:", response.status_code)
        return

    items = safe_json(response)
    if items is None:
        return
    if not items:
        print("\nInventory is empty.")
        return

    print("\n--- All Items ---")
    for item in items:
        print(f"[{item['id']}] {item['product_name']} | Qty: {item['quantity']} | Brand: {item.get('brands', 'N/A')}")


def view_product():
    item_id = prompt_item_id()
    if item_id is None:
        return

    response = api_get(f"/inventory/{item_id}")
    if response is None:
        return
    if response.status_code == 404:
        print("Item not found.")
        return
    if response.status_code != 200:
        print("Server error:", response.status_code)
        return

    item = safe_json(response)
    if item is None:
        return

    print(f"\nID: {item['id']}")
    print(f"Name: {item['product_name']}")
    print(f"Brand: {item.get('brands', 'N/A')}")
    print(f"Quantity: {item['quantity']}")
    print(f"Barcode: {item.get('barcode', 'N/A')}")


def add_product():
    print("\n--- Add New Product ---")
    name = input("Product name: ").strip()
    brand = input("Brand: ").strip()
    qty = input("Quantity: ").strip()

    if not name or not qty:
        print("Name and quantity are required.")
        return

    try:
        qty = int(qty)
    except ValueError:
        print("Quantity must be a number.")
        return

    if qty < 0:
        print("Quantity cannot be negative.")
        return

    payload = {
        "product_name": name,
        "brands": brand,
        "quantity": qty,
        "barcode": "000000000000",
        "ingredients_text": ""
    }

    response = api_post("/inventory", payload)
    if response is None:
        return

    if response.status_code == 201:
        data = safe_json(response)
        if data:
            print(f"\nAdded: {data['product_name']} (ID: {data['id']})")
    else:
        err = safe_json(response)
        print("Error:", (err or {}).get("error", "Unknown"))


def update_product():
    item_id = prompt_item_id("Enter item ID to update: ")
    if item_id is None:
        return

    print("\nLeave blank to skip.")
    name = input("New product name: ").strip()
    brand = input("New brand: ").strip()
    qty = input("New quantity: ").strip()

    payload = {}
    if name:
        payload["product_name"] = name
    if brand:
        payload["brands"] = brand
    if qty:
        try:
            qty = int(qty)
        except ValueError:
            print("Quantity must be a number.")
            return
        if qty < 0:
            print("Quantity cannot be negative.")
            return
        payload["quantity"] = qty

    if not payload:
        print("Nothing to update.")
        return

    response = api_patch(f"/inventory/{item_id}", payload)
    if response is None:
        return

    if response.status_code == 200:
        data = safe_json(response)
        if data:
            print(f"\nUpdated: {data['product_name']}")
    elif response.status_code == 404:
        print("Item not found.")
    else:
        err = safe_json(response)
        print("Error:", (err or {}).get("error", "Unknown"))


def delete_product():
    item_id = prompt_item_id("Enter item ID to delete: ")
    if item_id is None:
        return

    response = api_delete(f"/inventory/{item_id}")
    if response is None:
        return

    if response.status_code == 200:
        print("Item deleted successfully.")
    elif response.status_code == 404:
        print("Item not found.")
    else:
        print("Error:", response.status_code)


def search_external():
    print("\n--- Search OpenFoodFacts ---")
    print("1. Search by barcode")
    print("2. Search by name")
    choice = input("Select: ").strip()

    if choice == "1":
        barcode = input("Enter barcode: ").strip()
        if not barcode:
            print("Barcode cannot be empty.")
            return
        response = api_get("/external/search", params={"barcode": barcode})
    elif choice == "2":
        name = input("Enter product name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        response = api_get("/external/search", params={"name": name})
    else:
        print("Invalid choice.")
        return

    if response is None:
        return

    if response.status_code == 404:
        print("Product not found.")
        return
    if response.status_code != 200:
        err = safe_json(response)
        print("Error:", (err or {}).get("error", f"Server returned {response.status_code}"))
        return

    data = safe_json(response)
    if data is None:
        return

    print("\n--- Result ---")
    if isinstance(data, list):
        if not data:
            print("No matches found.")
            return
        for product in data:
            _print_product_summary(product)
            print("-" * 30)
    else:
        _print_product_summary(data)


def _print_product_summary(product):
    """Show only the fields relevant to inventory, instead of the full raw API dict."""
    name = product.get("product_name") or "(no name listed)"
    brands = product.get("brands") or "N/A"
    barcode = product.get("code") or product.get("barcode") or "N/A"
    ingredients = product.get("ingredients_text") or "N/A"

    print(f"Name: {name}")
    print(f"Brand: {brands}")
    print(f"Barcode: {barcode}")
    print(f"Ingredients: {ingredients}")


def menu():
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            view_product()
        elif choice == "3":
            add_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            search_external()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


# ── Entry Point ───────────────────────────────────────────

if __name__ == "__main__":
    if not ensure_server():
        sys.exit(1)
    menu()