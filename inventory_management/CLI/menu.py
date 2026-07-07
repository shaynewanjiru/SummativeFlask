import requests

BASE_URL = "http://127.0.0.1:5000"


import requests

def view_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")

        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)

    except Exception as e:
        print("ERROR:", e)


def view_product():
    product_id = input("Enter product ID: ")

    response = requests.get(
        f"{BASE_URL}/inventory/{product_id}"
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Product not found")


def add_product():
    product_name = input("Product Name: ")
    brand = input("Brand: ")
    quantity = int(input("Quantity: "))
    barcode = input("Barcode: ")
    ingredient_text = input("Ingredients: ")


    product_data = {
        "product_name": product_name,
        "brand": brand,
        "quantity": quantity,
        "barcode": barcode,
        "ingredients": ingredient_text

    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=product_data
    )

    print(response.json())


def update_product():
    product_id = input("Product ID: ")
    quantity = int(input("New Quantity: "))

    response = requests.patch(
        f"{BASE_URL}/inventory/{product_id}",
        json={"quantity": quantity}
    )

    print(response.json())


def delete_product():
    product_id = input("Product ID: ")

    response = requests.delete(
        f"{BASE_URL}/inventory/{product_id}"
    )

    print(response.json())


def search_openfoodfacts():
    barcode = input("Barcode: ")

    response = requests.get(
        f"{BASE_URL}/external/search",
        params={"barcode": barcode}
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Status:", response.status_code)
        print(response.text)
        
def menu():
    while True:

        print("\n\n===== INVENTORY SYSTEM =====")
        print("1. View Inventory")
        print("2. View Product")
        print("3. Add Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Search Product")
        print("7. Exit")
        print("\n============================")

        choice = input("Select an option: ")

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
            search_openfoodfacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()