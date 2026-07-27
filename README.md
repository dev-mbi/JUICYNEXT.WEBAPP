# JuicyneXt

A clean, mobile-first juice company website built with Flask. Customers can browse products, place orders, and get redirected to WhatsApp to confirm. Built for the Pakistan market with simplicity and fast loading in mind.

## Features

- Product catalog with availability status (available / coming soon)
- Order form with Pakistan phone validation, redirects to WhatsApp with pre-filled message
- Admin panel to manage products, update prices, change WhatsApp number, view and manage orders
- Order status tracking (pending / confirmed / delivered / cancelled)
- CSRF-protected forms, rate-limited admin login, password hashing
- Custom 404/500 error pages
- Fully responsive, mobile-first design (public + admin)
- Dockerized with PostgreSQL, Nginx, and health checks
- CI/CD pipeline with linting, testing, and deploy stages
- 30 automated tests

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy + PostgreSQL (SQLite for dev)
- Flask-WTF (CSRF protection)
- Flask-Limiter (rate limiting)
- HTML / CSS / JavaScript
- Docker + Gunicorn + Nginx

## Products

| Product       | Size  | Price | Status      |
|---------------|-------|-------|-------------|
| Mango Juice   | 250ml | Rs.50 | Available   |
| Mango Juice   | 1L    | --    | Coming Soon |
| Mixed Fruit   | 250ml | --    | Coming Soon |
| Orange Juice  | 250ml | --    | Coming Soon |

## Getting Started

### Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

The app will be available at http://localhost:5000.

### Docker

```bash
docker-compose up --build
```

## Admin Panel

Visit `/admin` to:

- Add, edit, delete, or toggle products
- Upload product images (max 5MB, auto-cleanup on delete)
- Change juice price and WhatsApp number
- View, search, filter, and update order statuses
- Order detail view with status management

Default login: admin / admin123

## Project Structure

```
juicynext/
├── app/
│   ├── __init__.py      # App factory, CSRF, limiter, logging, error handlers
│   ├── models.py        # Product, Order (with status), SiteConfig
│   ├── utils.py         # WhatsApp link builder
│   └── routes/
│       ├── main.py      # Home (DB-driven), About, Contact (with POST)
│       ├── products.py  # Product listing + order page
│       ├── order.py     # Submit order + phone validation
│       └── admin.py     # Admin CRUD + pagination + search
├── templates/
│   ├── base.html, index.html, products.html, order.html
│   ├── about.html, contact.html, 404.html, 500.html
│   └── admin/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_admin.py
├── run.py
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
└── .github/workflows/deploy.yml
```

## Environment Variables

- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database URL (defaults to SQLite, use PostgreSQL in production)
- `ADMIN_USERNAME` - Admin username (default: admin)
- `ADMIN_PASSWORD` - Admin password (default: admin123)
- `PORT` - Server port (default: 5000)
- `DB_PASSWORD` - PostgreSQL password (default: juicynext-pass)

## Tests

```bash
python -m pytest tests/ -v
```

## Order Flow

1. Browse products on home page or /products
2. Click "Buy Now" on available product
3. Fill order form (name, valid Pakistan phone, address, quantity)
4. Submit → validates → saves order → redirects to WhatsApp with pre-filled message
5. Admin manages orders (view, filter, update status)

## License

MIT
