import os
import sqlite3
from asyncio.windows_events import NULL

from flask import Blueprint, Flask, render_template, request,flash ,redirect, url_for,session
from werkzeug.security import check_password_hash
public_bp = Blueprint('public', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@public_bp.route('/')
def home():
    return render_template('home.html')

@public_bp.route('/honey')
def honey():
    conn = get_db_connection()
    honey_from_db = conn.execute("SELECT * FROM products WHERE category = 'honey'").fetchall()
    conn.close()
    return render_template('honey.html', honey_products=honey_from_db)

@public_bp.route('/wax')
def wax():
    conn = get_db_connection()
    wax_from_db = conn.execute("SELECT * FROM products WHERE category = 'wax'").fetchall()
    conn.close()
    return render_template('wax.html', wax_figures=wax_from_db)

@public_bp.route('/honey/<product_name>')
def honey_detail(product_name):
    conn = get_db_connection()
    # We use fetchone() because we only want ONE item, not a whole list.
    # The '?' is a placeholder that safely injects the product_name into the SQL command.
    selected_item = conn.execute("SELECT * FROM products WHERE category = 'honey' AND name = ?",
                                 (product_name,)).fetchone()
    conn.close()

    if selected_item != None:
        return render_template('detail.html', product=selected_item, category="honey")
    return "Produsul nu a fost găsit (Product not found)", 404


@public_bp.route('/wax/<product_name>')
def wax_detail(product_name):
    conn = get_db_connection()
    selected_item = conn.execute("SELECT * FROM products WHERE category = 'wax' AND name = ?",
                                 (product_name,)).fetchone()
    conn.close()

    if selected_item != None:
        return render_template('detail.html', product=selected_item, category="wax")
    return "Produsul nu a fost găsit (Product not found)", 404


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_message = request.form.get('message')
        if not user_name or not user_message:
            flash("Eroare! Te rugam sa completezi toate campurile.","error")
            return redirect(url_for('public.contact'))
       #salvam in text file pana cream database
        msg_path = os.path.join(BASE_DIR, 'messages.txt')
        with open(msg_path,"a", encoding="utf-8") as file:
            file.write(f"{user_name}: {user_message}\n")
            file.write("-"*30+"\n")

        flash(f"Multumim, {user_name}! Mesajul a fost trimis cu succes.","success")
        return redirect(url_for('public.home'))
    return render_template('contact.html')


@public_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # 1. Grab the current cart (or an empty list if it's their first click)
    current_cart = session.get('cart', [])

    # 2. Force a BRAND NEW list by adding the old list and the new item together
    # This completely bypasses the memory bug!
    session['cart'] = current_cart + [product_id]

    flash("Produs adăugat în coș!", "success")
    return redirect(request.referrer or url_for('public.home'))

@public_bp.route('/cart/')
def view_cart():
    cart_ids = session.get('cart',[])

    conn = get_db_connection()
    cart_items = []

    for product_id in cart_ids:
        item = conn.execute("SELECT * FROM products WHERE id = ?",(product_id,)).fetchone()
        if item :
            cart_items.append(item)
    conn.close()

    grand_total = 0

    for item in cart_items:
        grand_total += item['price']

    if grand_total > 200:
        grand_total -= grand_total * (10/100)


    return render_template('cart.html', items = cart_items, total=grand_total)


@public_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    current_cart = session.get('cart', [])

    if product_id in current_cart:
        # Remove the item from the temporary list
        current_cart.remove(product_id)

        # Wrap it in list() to force a brand new memory object!
        session['cart'] = list(current_cart)

        flash("Produs eliminat din coș!", "success")

    return redirect(url_for('public.view_cart'))


@public_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Changed to match the database column!
    total_price = 0
    order_summary = ""
    conn = get_db_connection()
    cart_ids = session.get('cart', [])

    if not cart_ids:
        flash("Coșul tău este gol! Adaugă produse înainte de a finaliza comanda.", "error")
        return redirect(url_for('public.view_cart'))

    if request.method == 'POST':
        customer_name = request.form.get('name')
        customer_phone = request.form.get('phone')
        delivery_method = request.form.get('delivery')
        delivery_address = request.form.get('address')

        # THE UPGRADE: set() removes duplicates so we only query each unique product once!
        unique_ids = set(cart_ids)

        for item_id in unique_ids:
            # 1. Ask the original list: "How many times did they click add for this item?"
            quantity = cart_ids.count(item_id)

            # 2. Fetch the product details
            item = conn.execute("SELECT * FROM products WHERE id = ?", (item_id,)).fetchone()

            # 3. Add the price multiplied by the quantity
            total_price += (item['price'] * quantity)

            # 4. Format the summary string beautifully with the quantity!
            order_summary += f"- {item['name']} (x{quantity})\n"

        # Apply the 10% discount if over 200 RON
        if total_price > 200:
            total_price -= total_price * (10 / 100)

        # Match the database blueprint exactly (total_price)
        cursor = conn.execute('''
                              INSERT INTO orders (customer_name, phone, delivery_method, address, order_summary,
                                                  total_price)
                              VALUES (?, ?, ?, ?, ?, ?)
                              ''', (customer_name, customer_phone, delivery_method, delivery_address, order_summary,
                                    total_price))

        new_order_id = cursor.lastrowid

        conn.commit()
        session.pop('cart', None)
        conn.close()

        flash("Comanda a fost plasată cu succes!", "success")
        return redirect(url_for('public.receipt', order_id=new_order_id))

    return render_template('checkout.html')

@public_bp.route('/receipt/<int:order_id>')
def receipt(order_id):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM orders WHERE id = ? ",(order_id,)).fetchone()
    conn.close()
    return render_template("receipt.html", order = order)

@public_bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?",(email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password) is True:
            session['admin_logged_in'] = True
            flash("Admin Logged in!", "success")
            return redirect(url_for('public.home'))
        else:
            flash("Email sau parola incorect", "error")
            return redirect(url_for('public.login'))


    return render_template('login.html')

@public_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Te-ai delogat cu succes!", "success")
    return redirect(url_for('public.home'))