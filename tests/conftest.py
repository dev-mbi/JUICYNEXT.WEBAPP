import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-key'

from app import create_app, db as _db

@pytest.fixture(scope='function')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        from app.models import Product, SiteConfig
        if Product.query.count() == 0:
            _db.session.add(Product(name='Mango Juice', size='250ml', price=50.0, status='available', image='mango-250ml.jpg'))
            _db.session.add(Product(name='Mango Juice', size='1L', price=None, status='coming_soon', image=None))
            _db.session.commit()
        if SiteConfig.query.count() == 0:
            _db.session.add(SiteConfig(key='whatsapp_number', value='923452202037'))
            _db.session.add(SiteConfig(key='juice_price', value='50'))
            _db.session.commit()

    yield app

    with app.app_context():
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
