from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'juicynext-dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///juicynext.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.order import order_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        from app.models import Product, Order, SiteConfig
        db.create_all()
        seed_data()

    return app

def seed_data():
    from app.models import Product, SiteConfig
    if Product.query.count() == 0:
        products = [
            Product(name='Mango Juice', size='250ml', price=50.0, status='available', image='mango-250ml.jpg'),
            Product(name='Mango Juice', size='1L', price=None, status='coming_soon', image=None),
        ]
        db.session.add_all(products)

    if SiteConfig.query.count() == 0:
        configs = [
            SiteConfig(key='whatsapp_number', value='923452202037'),
            SiteConfig(key='juice_price', value='50'),
        ]
        db.session.add_all(configs)

    db.session.commit()
