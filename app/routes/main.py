from flask import Blueprint, render_template, request, flash, redirect
from app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    products = Product.query.filter_by(status='available').all()
    coming_soon = Product.query.filter_by(status='coming_soon').all()
    return render_template('index.html', products=products, coming_soon=coming_soon)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        if name and message:
            flash('Thank you for your message! We will get back to you soon.')
        else:
            flash('Please fill in all required fields.', 'error')
        return redirect('/contact')
    return render_template('contact.html')
