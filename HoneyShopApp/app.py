from flask import Flask, render_template, request
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/honey')
def honey():
    conn = get_db_connection()
    honey_from_db = conn.execute("SELECT * FROM products WHERE category = 'honey'").fetchall()
    return render_template('honey.html', honey_products=honey_from_db)

@app.route('/wax')
def wax():
    conn = get_db_connection()
    wax_from_db = conn.execute("SELECT * FROM products WHERE category = 'wax'").fetchall()
    return render_template('wax.html', wax_figures=wax_from_db)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_message = request.form.get('message')
       #salvam in text file pana creem database
        with open("messages.txt","a", encoding="utf-8") as file:
            file.write(f"{user_name}: {user_message}\n")
            file.write("-"*30+"\n")

        return render_template('success.html', user_name=user_name)
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