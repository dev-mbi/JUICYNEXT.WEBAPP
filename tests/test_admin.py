def test_admin_login_page(client):
    resp = client.get('/admin/login')
    assert resp.status_code == 200
    assert b'Admin Login' in resp.data or b'login' in resp.data.lower()

def test_admin_login_success(client):
    resp = client.post('/admin/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    assert resp.status_code == 302
    assert resp.location == '/admin'

def test_admin_login_failure(client):
    resp = client.post('/admin/login', data={
        'username': 'admin',
        'password': 'wrong'
    })
    assert resp.status_code == 200
    assert b'Invalid' in resp.data

def test_admin_dashboard_requires_login(client):
    resp = client.get('/admin/')
    assert resp.status_code == 302
    assert '/admin/login' in resp.location

def test_admin_dashboard(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.get('/admin/')
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data

def test_admin_products_list(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.get('/admin/products')
        assert resp.status_code == 200
        assert b'Products' in resp.data
        assert b'Mango Juice' in resp.data

def test_admin_orders_list(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.get('/admin/orders')
        assert resp.status_code == 200
        assert b'Orders' in resp.data

def test_admin_settings(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.get('/admin/settings')
        assert resp.status_code == 200
        assert b'Settings' in resp.data

def test_admin_add_product(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.post('/admin/products/add', data={
            'name': 'New Juice',
            'size': '250ml',
            'price': '55',
            'status': 'available'
        })
        assert resp.status_code == 302
        assert resp.location == '/admin/products'

def test_admin_delete_product(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.post('/admin/products/delete/1')
        assert resp.status_code == 302

def test_admin_toggle_product(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.post('/admin/products/toggle/1')
        assert resp.status_code == 302

def test_admin_update_settings(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.post('/admin/settings', data={
            'juice_price': '60',
            'whatsapp_number': '923001234567'
        })
        assert resp.status_code == 302

def test_admin_logout(client):
    with client:
        client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        resp = client.get('/admin/logout')
        assert resp.status_code == 302
        assert '/admin/login' in resp.location
