import re
def format_product_name(name):
    if not name:
        return "This product does not exist"
    return name.upper()

def validate_barcode(barcode):
    pattern = r"^\d{8,14}$"
    if re.match(pattern, barcode):
        return True
    return False

def clean_ingredients(text):
    if not text: 
        return ""
    if len(text) > 500:
        return "You have reached your limit"
    
def item_to_string(item):
    return f"[{item['id']}] {item['product_name']} (Qty: {item['quantity']})"    