from flask import Flask, render_template

app = Flask(__name__)

honey_products= [{"name": "Miere de tei",
                  "price": 35,
                  "description": "1 kg"},
                 {"name": "Miere de salcam",
                  "price": 40,
                  "description": "1kg"},
                 {"name": "Miere de poliflora",
                  "price": 30,
                  "description": "1kg"},
                 {"name": "Miere de floarea soarelui",
                  "price": 35,
                  "description": "1kg"},
                 {"name": "Miere de mana",
                  "price": 35,
                  "description": "1kg"}]

wax_figures= [   {"name": "Albine",
                  "price": 15,
                  "description": "mica"},
                 {"name": "Motociclete",
                  "price": 20,
                  "description": "medii"},
                 {"name": "Festive",
                  "price": 15,
                  "description": "medii"},
                 {"name": "Paste",
                  "price": 15,
                  "description": "medii"},

]




@app.route('/')

def home():
    return render_template('home.html')

@app.route('/honey')
def honey():
    return render_template('honey.html', honey_products=honey_products)

@app.route('/wax')
def wax():
    return render_template('wax.html', wax_figures=wax_figures)


if __name__ =='__main__':
    app.run(debug=True)