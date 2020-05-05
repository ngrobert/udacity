from flask import Flask, render_template

# creates application that gets named after the name of our file
app = Flask(__name__)

# listens to our homepage
@app.route('/')
def index():
    # returns html file
    # pass in variables we want to pass into our template
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }])
