import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://hants:46566656@instagram.cjkeu5klelix.us-west-2.rds.amazonaws.com:5432/instadb'

#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
db.create_all()
db.session.commit()