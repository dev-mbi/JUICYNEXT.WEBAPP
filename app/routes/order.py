from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.models import Order, Product, SiteConfig
from app.utils import create_whatsapp_link

order_bp = Blueprint('order', __name__)

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
    if not address:
        errors.append('Address is required')
    if not quantity.isdigit() or int(quantity) < 1:
        errors.append('Valid quantity is required')

    product = Product.query.get(product_id) if product_id else None
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
        quantity=int(quantity)
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
