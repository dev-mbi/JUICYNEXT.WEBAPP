# JuicyneXt

A clean, mobile-first juice company website built with Flask. Customers can browse products, place orders, and get redirected to WhatsApp to confirm. Built for the Pakistan market with simplicity and fast loading in mind.

## Features

- Product catalog with availability status (available / coming soon)
- Order form that redirects to WhatsApp with a pre-filled message
- Admin panel to manage products, update prices, change WhatsApp number, and view orders
- Fully responsive, mobile-first design
- Dockerized for easy deployment

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy
- HTML / CSS / JavaScript
- Docker + Gunicorn

## Products

| Product     | Size  | Price | Status      |
|-------------|-------|-------|-------------|
| Mango Juice | 250ml | Rs.50 | Available   |
| Mango Juice | 1L    | --    | Coming Soon |

## Getting Started

### Local Development

```bash
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

- Add or edit products
- Upload product images
- Toggle product availability
- Change juice price
- Change WhatsApp number
- View customer orders

Default login: admin / admin123

## Project Structure

```
juicynext/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── utils.py
│   └── routes/
│       ├── main.py
│       ├── products.py
│       ├── order.py
│       └── admin.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── order.html
│   ├── about.html
│   ├── contact.html
│   └── admin/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── .opencode/
│   ├── skills/juicynext/SKILL.md
│   └── agents/
├── run.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Environment Variables

- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database URL (defaults to SQLite)
- `ADMIN_USERNAME` - Admin username (default: admin)
- `ADMIN_PASSWORD` - Admin password (default: admin123)

## License

MIT
