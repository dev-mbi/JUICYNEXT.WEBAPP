from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.models import Order, Product, SiteConfig
from app.utils import create_whatsapp_link
import re

order_bp = Blueprint('order', __name__)

def validate_pakistan_phone(phone):
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    if re.match(r'^03\d{9}$', cleaned):
        return True, '92' + cleaned[1:]
    if re.match(r'^923\d{9}$', cleaned):
        return True, cleaned
    if re.match(r'^\+923\d{9}$', cleaned):
        return True, cleaned[1:]
    if re.match(r'^3\d{9}$', cleaned):
        return True, '92' + cleaned
    return False, None

@order_bp.route('/submit-order', methods=['POST'])
def submit_order():
    product_id = request.form.get('product_id')
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    quantity = request.form.get('quantity', '1')

    errors = []
    if not name:
        errors.append('Name is required')
    if not phone:
        errors.append('Phone number is required')
    else:
        valid, normalized = validate_pakistan_phone(phone)
        if not valid:
            errors.append('Invalid phone number. Use Pakistan format (e.g. 03XX-XXXXXXX)')
        else:
            phone = normalized
    if not address:
        errors.append('Address is required')
    if not quantity.isdigit() or int(quantity) < 1:
        errors.append('Valid quantity is required')

    product = db.session.get(Product, int(product_id)) if product_id and product_id.isdigit() else None
    if not product or product.status != 'available':
        errors.append('Product is not available')

    if errors:
        for error in errors:
            flash(error)
        if product:
            return render_template('order.html', product=product), 400
        return redirect('/products')

    order = Order(
        name=name,
        phone=phone,
        address=address,
        product_name=product.name,
        size=product.size,
        quantity=int(quantity),
        status='pending'
    )
    db.session.add(order)
    db.session.commit()

    config = SiteConfig.query.filter_by(key='whatsapp_number').first()
    number = config.value if config else '923452202037'

    link = create_whatsapp_link({
        'product_name': product.name,
        'size': product.size,
        'quantity': quantity,
        'name': name,
        'phone': phone,
        'address': address,
    }, number)

    return redirect(link)
