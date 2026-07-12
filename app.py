from flask import Flask

app = Flask(__name__)

@app.route('/')

def home():
    return "Bine a-ti venit la magazinul nostru!"

if __name__ =='__main__':
    app.run(debug=True)