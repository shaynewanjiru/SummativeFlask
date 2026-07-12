# Inventory Management System

A simple Flask-based inventory app for managing products, viewing details, and importing product data from OpenFoodFacts.

## What this project does

This project lets you:
- view all inventory items
- view a single item by ID
- add new products
- update product details
- delete items
- search for product information using an external barcode or name lookup

It also includes a simple command-line interface so you can use the app without writing API requests manually.

## Main features

- REST API with Flask
- In-memory inventory storage for easy testing and demo use
- Product search through OpenFoodFacts
- CLI menu for common actions
- Basic validation for item data

## Project structure

- app/__init__.py: creates the Flask app
- app/routes.py: API endpoints
- app/services.py: business logic for CRUD and external imports
- app/database.py: sample inventory data
- app/requester.py: OpenFoodFacts API requests
- CLI/menu.py: terminal-based menu for interacting with the app
- run.py: starts the Flask server

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run the app

Start the Flask server:

```bash
python run.py
```

The app will run at:

```text
http://127.0.0.1:5000
```

## Use the CLI

From the project folder, run:

```bash
python CLI/menu.py
```

The CLI will start the server automatically if needed and give you menu options to:
- view inventory
- view one item
- add an item
- update an item
- delete an item
- search external product data

## API overview

### Inventory endpoints

- GET /inventory: list all items
- GET /inventory/<id>: get one item
- POST /inventory: add a new item
- PATCH /inventory/<id>: update an item
- DELETE /inventory/<id>: delete an item

### External lookup endpoints

- GET /external/search?barcode=...: search by barcode
- GET /external/search?name=...: search by product name
- POST /external/add: fetch a product from OpenFoodFacts and save it to inventory

## Notes

- Inventory data is stored in memory, so it resets when the server restarts.
- The app uses OpenFoodFacts for external product lookup, so internet access is required for those features.

## Example

A typical workflow is:
1. start the server
2. use the CLI or API to add inventory items
3. search for product data from OpenFoodFacts
4. update stock or remove items as needed
