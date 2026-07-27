from flask import Blueprint, render_template, request, redirect, session, flash
import os
from functools import wraps
from werkzeug.utils import secure_filename
from app import db
from app.models import Product, Order, SiteConfig

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

ADMIN_USER = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASSWORD', 'admin123')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect('/admin')
        flash('Invalid credentials')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

@admin_bp.route('/')
@login_required
def dashboard():
    product_count = Product.query.count()
    order_count = Order.query.count()
    return render_template('admin/dashboard.html', product_count=product_count, order_count=order_count)

@admin_bp.route('/products')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        size = request.form.get('size')
        price = request.form.get('price')
        status = request.form.get('status', 'available')

        price_val = float(price) if price else None

        product = Product(name=name, size=size, price=price_val, status=status)
        db.session.add(product)
        db.session.commit()

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f'{name.lower().replace(" ", "-")}-{size}.{ext}')
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image = filename
            db.session.commit()

        flash('Product added')
        return redirect('/admin/products')
    return render_template('admin/product_form.html')

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name', product.name)
        product.size = request.form.get('size', product.size)
        price = request.form.get('price')
        product.price = float(price) if price else None
        product.status = request.form.get('status', product.status)

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f'{product.name.lower().replace(" ", "-")}-{product.size}.{ext}')
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image = filename

        db.session.commit()
        flash('Product updated')
        return redirect('/admin/products')
    return render_template('admin/product_form.html', product=product)

@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted')
    return redirect('/admin/products')

@admin_bp.route('/products/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_product(id):
    product = Product.query.get_or_404(id)
    product.status = 'coming_soon' if product.status == 'available' else 'available'
    db.session.commit()
    flash(f'Product status changed to {product.status}')
    return redirect('/admin/products')

@admin_bp.route('/orders')
@login_required
def order_list():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        price = request.form.get('juice_price')
        whatsapp = request.form.get('whatsapp_number')

        if price:
            cfg = SiteConfig.query.filter_by(key='juice_price').first()
            if cfg:
                cfg.value = price
            else:
                db.session.add(SiteConfig(key='juice_price', value=price))

        if whatsapp:
            cfg = SiteConfig.query.filter_by(key='whatsapp_number').first()
            if cfg:
                cfg.value = whatsapp
            else:
                db.session.add(SiteConfig(key='whatsapp_number', value=whatsapp))

        db.session.commit()
        flash('Settings updated')
        return redirect('/admin/settings')

    price = SiteConfig.query.filter_by(key='juice_price').first()
    whatsapp = SiteConfig.query.filter_by(key='whatsapp_number').first()
    return render_template('admin/settings.html', price=price, whatsapp=whatsapp)
