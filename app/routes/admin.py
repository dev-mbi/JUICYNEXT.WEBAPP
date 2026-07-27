from flask import Blueprint, render_template, request, redirect, session, flash, abort
import os
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, limiter
from app.models import Product, Order, SiteConfig

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024

ADMIN_USER = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASS_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123'))


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_product(name, size, price_str, status):
    errors = []
    if not name or len(name.strip()) < 1:
        errors.append('Product name is required')
    elif len(name) > 100:
        errors.append('Product name must be under 100 characters')
    if not size or len(size.strip()) < 1:
        errors.append('Size is required')
    elif len(size) > 20:
        errors.append('Size must be under 20 characters')
    if price_str and price_str.strip():
        try:
            val = float(price_str)
            if val < 0:
                errors.append('Price must be positive')
        except ValueError:
            errors.append('Price must be a valid number')
    if status not in ('available', 'coming_soon'):
        errors.append('Invalid status')
    return errors


@admin_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
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
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/products.html', products=products, search=search)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        size = request.form.get('size', '').strip()
        price_str = request.form.get('price', '').strip()
        status = request.form.get('status', 'available')

        errors = validate_product(name, size, price_str, status)
        if errors:
            for err in errors:
                flash(err)
            return render_template('admin/product_form.html'), 400

        price_val = float(price_str) if price_str else None
        product = Product(name=name, size=size, price=price_val, status=status)
        db.session.add(product)
        db.session.commit()

        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            if len(file.read()) > MAX_IMAGE_SIZE:
                flash('Image must be under 5MB')
                db.session.delete(product)
                db.session.commit()
                return render_template('admin/product_form.html'), 400
            file.seek(0)
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
    product = db.session.get(Product, id)
    if not product:
        return render_template('404.html'), 404
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        size = request.form.get('size', '').strip()
        price_str = request.form.get('price', '').strip()
        status = request.form.get('status', 'available')

        errors = validate_product(name, size, price_str, status)
        if errors:
            for err in errors:
                flash(err)
            return render_template('admin/product_form.html', product=product), 400

        product.name = name
        product.size = size
        product.price = float(price_str) if price_str else None
        product.status = status

        file = request.files.get('image')
        if file and file.filename and allowed_file(file.filename):
            if len(file.read()) > MAX_IMAGE_SIZE:
                flash('Image must be under 5MB')
                return render_template('admin/product_form.html', product=product), 400
            file.seek(0)
            if product.image:
                old_path = os.path.join(UPLOAD_FOLDER, product.image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f'{name.lower().replace(" ", "-")}-{size}.{ext}')
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image = filename

        db.session.commit()
        flash('Product updated')
        return redirect('/admin/products')
    return render_template('admin/product_form.html', product=product)


@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        abort(404)
    if product.image:
        img_path = os.path.join(UPLOAD_FOLDER, product.image)
        if os.path.exists(img_path):
            os.remove(img_path)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted')
    return redirect('/admin/products')


@admin_bp.route('/products/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_product(id):
    product = db.session.get(Product, id)
    if not product:
        abort(404)
    product.status = 'coming_soon' if product.status == 'available' else 'available'
    db.session.commit()
    flash(f'Product status changed to {product.status}')
    return redirect('/admin/products')


@admin_bp.route('/orders')
@login_required
def order_list():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '').strip()
    query = Order.query
    if status_filter:
        query = query.filter(Order.status == status_filter)
    if search:
        query = query.filter(Order.name.ilike(f'%{search}%') | Order.phone.ilike(f'%{search}%'))
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter, search=search)


@admin_bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    order = db.session.get(Order, id)
    if not order:
        abort(404)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/orders/<int:id>/status', methods=['POST'])
@login_required
def update_order_status(id):
    order = db.session.get(Order, id)
    if not order:
        abort(404)
    new_status = request.form.get('status')
    if new_status in ('pending', 'confirmed', 'delivered', 'cancelled'):
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {new_status}')
    return redirect('/admin/orders')


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        price = request.form.get('juice_price', '').strip()
        whatsapp = request.form.get('whatsapp_number', '').strip()

        if price:
            try:
                val = float(price)
                if val < 0:
                    flash('Price must be positive')
                    return redirect('/admin/settings')
                cfg = SiteConfig.query.filter_by(key='juice_price').first()
                if cfg:
                    cfg.value = str(val)
                else:
                    db.session.add(SiteConfig(key='juice_price', value=str(val)))
            except ValueError:
                flash('Invalid price value')

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
