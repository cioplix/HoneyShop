from flask import Flask
from admin import admin_bp
from public import public_bp
app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)
app.secret_key = "secret_honey_key"

if __name__ =='__main__':
    app.run(debug=True)