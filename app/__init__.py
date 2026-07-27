from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from datetime import datetime, timezone

db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'juicynext-dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///juicynext.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('juicynext.log')
        ]
    )

    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.order import order_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from app.models import Product, SiteConfig
    if Product.query.count() == 0:
        products = [
            Product(name='Mango Juice', size='250ml', price=50.0, status='available', image='mango-250ml.jpg'),
            Product(name='Mango Juice', size='1L', price=None, status='coming_soon', image=None),
            Product(name='Mixed Fruit', size='250ml', price=60.0, status='coming_soon', image=None),
            Product(name='Orange Juice', size='250ml', price=55.0, status='coming_soon', image=None),
        ]
        db.session.add_all(products)

    if SiteConfig.query.count() == 0:
        configs = [
            SiteConfig(key='whatsapp_number', value='923452202037'),
            SiteConfig(key='juice_price', value='50'),
        ]
        db.session.add_all(configs)

    db.session.commit()
