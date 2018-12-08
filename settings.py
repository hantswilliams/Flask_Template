import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'INSERT YOUR DB LINK HERE'

#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
db.create_all()
db.session.commit()