from flask import Flask, render_template

app = Flask(__name__)

honey_products= [{"name": "Miere de tei",
                  "price": 35,
                  "description": "1 kg",
                  "image": "tei.jpg"},
                 {"name": "Miere de salcam",
                  "price": 40,
                  "description": "1kg",
                  "image": "salcam.jpg"},
                 {"name": "Miere de poliflora",
                  "price": 30,
                  "description": "1kg",
                  "image": "poliflora.jpg"},
                 {"name": "Miere de floarea soarelui",
                  "price": 35,
                  "description": "1kg",
                  "image": "sunflower.jpg"},
                 {"name": "Miere de mana",
                  "price": 35,
                  "description": "1kg",
                  "image": "mana.jpg"}]

wax_figures= [   {"name": "Albine",
                  "price": 15,
                  "description": "mica",
                  "image": "albine.jpg"},
                 {"name": "Motociclete",
                  "price": 20,
                  "description": "medii",
                  "image": "moto.jpg"},
                 {"name": "Festive",
                  "price": 15,
                  "description": "medii",
                  "image": "craciun.jpg"},
                 {"name": "Paste",
                  "price": 15,
                  "description": "medii",
                  "image": "paste.jpg"},

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