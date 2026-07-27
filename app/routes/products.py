from flask import Blueprint, render_template, abort
from app import db
from app.models import Product

products_bp = Blueprint('products', __name__)


@products_bp.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('products.html', products=products)


@products_bp.route('/order/<int:product_id>')
def order_page(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        abort(404)
    if product.status != 'available':
        abort(404)
    return render_template('order.html', product=product)
