class TestMainRoutes:
    def test_home_page(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'JuicyneXt' in resp.data
        assert b'Mango Juice' in resp.data

    def test_about_page(self, client):
        resp = client.get('/about')
        assert resp.status_code == 200
        assert b'About' in resp.data

    def test_contact_page_get(self, client):
        resp = client.get('/contact')
        assert resp.status_code == 200
        assert b'Contact' in resp.data

    def test_contact_page_post(self, client):
        resp = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        })
        assert resp.status_code == 302

class TestProductRoutes:
    def test_product_list(self, client):
        resp = client.get('/products')
        assert resp.status_code == 200
        assert b'Our Products' in resp.data
        assert b'Mango Juice' in resp.data

    def test_order_page_existing(self, client):
        resp = client.get('/order/1')
        assert resp.status_code == 200
        assert b'Place Your Order' in resp.data

    def test_order_page_not_found(self, client):
        resp = client.get('/order/999')
        assert resp.status_code == 404

class TestOrderRoutes:
    def test_submit_order_success(self, client):
        resp = client.post('/submit-order', data={
            'product_id': '1',
            'name': 'Test User',
            'phone': '03001234567',
            'address': 'Test Address 123',
            'quantity': '2'
        })
        assert resp.status_code == 302
        assert 'wa.me' in resp.location

    def test_submit_order_missing_fields(self, client):
        resp = client.post('/submit-order', data={
            'product_id': '1',
            'name': '',
            'phone': '',
            'address': '',
            'quantity': '1'
        })
        assert resp.status_code == 400

    def test_submit_order_invalid_phone(self, client):
        resp = client.post('/submit-order', data={
            'product_id': '1',
            'name': 'Test',
            'phone': '123',
            'address': 'Addr',
            'quantity': '1'
        })
        assert resp.status_code == 400

class TestUtils:
    def test_whatsapp_link(self, app):
        from app.utils import create_whatsapp_link
        data = {
            'product_name': 'Mango Juice',
            'size': '250ml',
            'quantity': '2',
            'name': 'Test',
            'phone': '03001234567',
            'address': 'Addr'
        }
        link = create_whatsapp_link(data, '923452202037')
        assert link.startswith('https://wa.me/923452202037')
        assert 'Mango%20Juice' in link
