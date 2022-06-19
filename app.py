from flask import Flask
from lunchmoneyapp import views
from dotenv import dotenv_values

keys=dotenv_values()
app = Flask(__name__)
app.config['SECRET_KEY'] = keys['FLASK_KEY']
app.register_blueprint(views,url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)