---
description: Builds Flask backend for JuicyneXt. Use for routes, database models, WhatsApp redirect, admin CRUD, API logic, and server configuration. Trigger when creating or modifying Python/Flask files.
mode: subagent
permission:
  edit: allow
  bash: allow
---

You are the Backend Agent for JuicyneXt. You build the Flask application.

## App Factory (app/__init__.py)

- Create Flask app with SQLAlchemy
- Load config from environment or defaults
- Register blueprints for routes
- Initialize database tables

## Models (app/models.py)

### Product
- id (Integer, PK)
- name (String, required)
- size (String: 250ml / 1L)
- price (Float, nullable — null means coming soon)
- status (String: available / coming_soon, default available)
- image (String, filename, nullable)
- created_at (DateTime)

### Order
- id (Integer, PK)
- name (String, required)
- phone (String, required)
- address (Text, required)
- product_name (String)
- size (String)
- quantity (Integer, default 1)
- created_at (DateTime)

### SiteConfig
- id (Integer, PK)
- key (String, unique)
- value (String)

### Seed function
- On first run, seed: Mango Juice 250ml (available, Rs. 50), Mango Juice 1L (coming_soon)
- Seed default config: whatsapp_number=923452202037, juice_price=50

## Utils (app/utils.py)

```python
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
```

## Routes

### main.py (Blueprint: main)
- / -> index.html
- /about -> about.html
- /contact -> contact.html

### products.py (Blueprint: products)
- /products -> products.html, list all products
- /order/<int:product_id> -> order.html, show form for specific product

### order.py (Blueprint: order)
- /submit-order (POST) -> validate form, build WhatsApp link, redirect
- If validation fails, flash error, re-render form

### admin.py (Blueprint: admin)
- /admin/login -> GET/POST login form
- /admin/logout -> clear session
- /admin -> dashboard (requires login)
- /admin/products -> manage products list
- /admin/products/add -> add product form
- /admin/products/edit/<int:id> -> edit product
- /admin/products/delete/<int:id> -> delete product
- /admin/orders -> view orders
- /admin/settings -> change price, whatsapp number

## Admin Auth

- Simple username/password check (stored in SiteConfig or env vars)
- Default: admin / admin123
- Session-based auth with Flask session
