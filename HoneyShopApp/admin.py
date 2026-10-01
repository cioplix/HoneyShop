import os
import sqlite3
from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for, session

admin_bp = Blueprint('admin', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_login=session.get('admin_logged_in')
    if not admin_login:
        flash("Acces interzis!","error")
        return redirect(url_for('public.login'))

    conn = get_db_connection()

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_price = request.form.get('price')
        new_description = request.form.get('description')
        new_image = request.form.get('image')
        new_category = request.form.get('category')

        conn.execute('''
                     INSERT INTO products (name, price, description, image, category)
                     VALUES (?, ?, ?, ?, ?)
                     ''', (new_name, new_price, new_description, new_image, new_category))
        conn.commit()
        conn.close()
        flash(f"Produsul {new_name} a fost adaugat!", "success")
        return redirect(url_for('admin.admin'))

    all_products = conn.execute('SELECT * FROM products').fetchall()
    all_orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('admin.html', products=all_products,orders=all_orders)


@admin_bp.route('/admin/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    flash(f"Produsul a fost sters din baza de date!", "error")
    return redirect(url_for('admin.admin'))


@admin_bp.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()

    if request.method == 'POST':
        updated_name = request.form.get('name')
        updated_price = request.form.get('price')
        updated_desc = request.form.get('description')
        updated_image = request.form.get('image')
        updated_cat = request.form.get('category')

        conn.execute('''
                     UPDATE products
                     SET name        = ?,
                         price       = ?,
                         description = ?,
                         image       = ?,
                         category    = ?
                     WHERE id = ?
                     ''', (updated_name, updated_price, updated_desc, updated_image, updated_cat, product_id))

        conn.commit()
        conn.close()

        flash("Produsul a fost actualizat cu succes!", "success")
        return redirect(url_for('admin.admin'))

    product_to_edit = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    return render_template('edit.html', product=product_to_edit)


@admin_bp.route('/admin/review/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    # 1. Your Standard Admin Bouncer
    admin_login = session.get('admin_logged_in')
    if not admin_login:
        flash("Acces interzis!", "error")
        return redirect(url_for('public.login'))

    # 2. The Executioner
    conn = get_db_connection()
    conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()

    flash("Recenzia a fost ștearsă cu succes.", "success")

    # 3. Bounce them right back to the product page they were looking at
    return redirect(request.referrer or url_for('admin.admin'))
