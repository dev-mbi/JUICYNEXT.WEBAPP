---
name: juicynext
description: Use for anything related to the JuicyneXt juice company website project — Flask backend, mobile-first UI, product management, order/WhatsApp flow, admin panel, Docker deployment, and GitHub workflows.
---

# JuicyneXt Skill

## Project Goal

Build a scalable juice company website with:
- 250ml juice available for order
- 1L juice coming soon
- More flavours coming soon
- Order redirects to WhatsApp
- Clean, modern, mobile-first UI
- Flask backend

## Tech Stack

- Python / Flask + Flask-SQLAlchemy
- HTML / CSS / JavaScript
- SQLite (dev) / PostgreSQL (prod)
- Docker + Gunicorn + Nginx

## Directory Structure

```
juicynext/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Product, Order, SiteConfig
│   ├── utils.py             # WhatsApp link builder
│   └── routes/
│       ├── __init__.py
│       ├── main.py          # Home, About, Contact
│       ├── products.py      # Product listing
│       ├── order.py         # Order form + WhatsApp
│       └── admin.py         # Admin panel
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── about.html
│   ├── contact.html
│   ├── order.html
│   └── admin/
│       ├── dashboard.html
│       ├── products.html
│       ├── orders.html
│       └── settings.html
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│       ├── logo.png
│       ├── mango-250ml.jpg
│       └── hero-bg.jpg
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Color Palette

- Orange: #FF6B35 (primary)
- Yellow: #FFD700 (accent)
- Green: #2ECC71 (fresh)
- White: #FFFFFF
- Dark: #2C3E50 (text)

## Data Models

### Product
- id (int, PK)
- name (string)
- size (string: 250ml / 1L / other)
- price (float, nullable for coming-soon)
- status (string: available / coming_soon)
- image (string, filename)
- created_at (datetime)

### Order
- id (int, PK)
- name (string)
- phone (string)
- address (text)
- product_name (string)
- size (string)
- quantity (int)
- created_at (datetime)

### SiteConfig
- id (int, PK)
- key (string, unique)
- value (string)

Default config keys: whatsapp_number, juice_price

## Product Logic

- 250ml available -> "Buy Now" button -> order form -> WhatsApp
- 1L -> "Coming Soon" badge
- Other flavours -> "Coming Soon" badge
- Price read from SiteConfig (default Rs. 50), changeable via admin

## Order Flow

1. User browses products
2. Clicks "Buy Now" on available product
3. Fills order form (name, phone, address, quantity)
4. Submits -> validates -> builds WhatsApp link
5. Redirects to wa.me/923452202037 with pre-filled message
6. WhatsApp number configurable from admin panel

## WhatsApp Message Format

```
Hello JuicyneXt
I want to order:
Product: Mango Juice (250ml)
Quantity: 2
Name: [User Name]
Phone: [User Phone]
Address: [User Address]
```

## Admin Panel

Route: /admin
Features:
- Login (username/password from config)
- Dashboard with summary
- CRUD products (add, edit, delete, upload image, toggle status)
- View orders list
- Settings: change juice price, change WhatsApp number

## Sub-Agents

This project uses 5 sub-agents:
- ui-agent: Mobile-first UI templates, CSS, JS
- backend-agent: Flask routes, models, API logic
- product-agent: Product data management, seeding
- qa-agent: Testing forms, responsiveness, performance
- devops-agent: Docker, CI/CD, deployment

## UI Rules

- Mobile-first responsive design
- No emojis in UI
- Smooth CSS transitions and hover effects
- Clean, modern, fresh look
- Juice-themed gradients and colors
- All Pakistan delivery messaging

## Deployment

- Docker with Gunicorn
- Nginx reverse proxy (optional)
- GitHub Actions CI/CD on push to main
