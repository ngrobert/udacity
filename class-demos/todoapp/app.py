from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rng@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# create models for database
db.create_all()

# define route that listens to the below
@app.route('/todos/create', methods=['POST'])
# handler
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        # create from class
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


# listens to our homepage
@app.route('/')
def index():
    # returns html file
    # pass in variables we want to pass into our template
    # include data from our database
    return render_template('index.html', data=Todo.query.all())
