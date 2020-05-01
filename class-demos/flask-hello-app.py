from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rng@localhost:5432/example'
db = SQLAlchemy(app)

# inheriting from db.Model, connects to SQLAlchemy's mappings between classes and tables
class Person(db.Model):
    # name of table
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

# detects models and create table(s) if they don't exist
db.create_all()

@app.route('/')
def index():
    return "Hello world"