import urllib.parse

def create_whatsapp_link(data, number):
    message = f"""Hello JuicyneXt
I want to order:
Product: {data['product_name']} ({data['size']})
Quantity: {data['quantity']}
Name: {data['name']}
Phone: {data['phone']}
Address: {data['address']}"""
    return f"https://wa.me/{number}?text=" + urllib.parse.quote(message)
