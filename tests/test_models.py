from app.models import Product, Order, SiteConfig

class TestProduct:
    def test_create_product(self, app):
        with app.app_context():
            p = Product(name='Test Juice', size='500ml', price=75.0, status='available')
            assert p.name == 'Test Juice'
            assert p.size == '500ml'
            assert p.price == 75.0
            assert p.status == 'available'
            assert str(p) == 'Test Juice (500ml)'

    def test_coming_soon_product(self, app):
        with app.app_context():
            p = Product(name='New Flavor', size='1L', price=None, status='coming_soon')
            assert p.status == 'coming_soon'
            assert p.price is None

    def test_product_repr(self, app):
        with app.app_context():
            p = Product(name='Mango', size='250ml', price=50.0, status='available')
            assert repr(p) == 'Mango (250ml)'

class TestOrder:
    def test_create_order(self, app):
        with app.app_context():
            from app import db
            o = Order(name='John', phone='923001234567', address='Test Address',
                       product_name='Mango Juice', size='250ml', quantity=2)
            db.session.add(o)
            db.session.commit()
            assert o.name == 'John'
            assert o.phone == '923001234567'
            assert o.quantity == 2
            assert o.status == 'pending'
            assert f'Order #{o.id}' in str(o)

    def test_order_status_default(self, app):
        with app.app_context():
            from app import db
            o = Order(name='Jane', phone='923001234568', address='Address')
            db.session.add(o)
            db.session.commit()
            assert o.status == 'pending'

class TestSiteConfig:
    def test_create_config(self, app):
        with app.app_context():
            c = SiteConfig(key='test_key', value='test_value')
            assert c.key == 'test_key'
            assert c.value == 'test_value'
            assert repr(c) == 'test_key: test_value'
