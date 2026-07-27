from flask import Flask, render_template, request,flash,redirect,url_for
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)

app.secret_key = "secret_honey_key"
@app.route('/')

def home():
    return render_template('home.html')

@app.route('/honey')
def honey():
    conn = get_db_connection()
    honey_from_db = conn.execute("SELECT * FROM products WHERE category = 'honey'").fetchall()
    conn.close()
    return render_template('honey.html', honey_products=honey_from_db)

@app.route('/wax')
def wax():
    conn = get_db_connection()
    wax_from_db = conn.execute("SELECT * FROM products WHERE category = 'wax'").fetchall()
    conn.close()
    return render_template('wax.html', wax_figures=wax_from_db)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_message = request.form.get('message')
        if not user_name or not user_message:
            flash("Eroare! Te rugam sa completezi toate campurile.","error")
            return redirect(url_for('contact'))
       #salvam in text file pana cream database
        msg_path = os.path.join(BASE_DIR, 'messages.txt')
        with open(msg_path,"a", encoding="utf-8") as file:
            file.write(f"{user_name}: {user_message}\n")
            file.write("-"*30+"\n")

        flash(f"Multumim, {user_name}! Mesajul a fost trimis cu succes.","success")
        return redirect(url_for('home'))
    return render_template('contact.html')


@app.route('/honey/<product_name>')
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


@app.route('/wax/<product_name>')
def wax_detail(product_name):
    conn = get_db_connection()
    selected_item = conn.execute("SELECT * FROM products WHERE category = 'wax' AND name = ?",
                                 (product_name,)).fetchone()
    conn.close()

    if selected_item != None:
        return render_template('detail.html', product=selected_item, category="wax")
    return "Produsul nu a fost găsit (Product not found)", 404

if __name__ =='__main__':
    app.run(debug=True)