from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rng@localhost:5432/example'
# ignore deprecation warning as this comes up every time you run SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# inheriting from db.Model, connects to SQLAlchemy's mappings between classes and tables
class Person(db.Model):
    # name of table
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # ability to customized a printable string (useful for debugging)
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

# detects models and create table(s) if they do not exist
db.create_all()

@app.route('/')
def index():
    person = Person.query.first()
    return "Hello " + person.name