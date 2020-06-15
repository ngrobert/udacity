import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # any origins from the client can access the uri
  CORS(app, resources={r"/*": {"origins": "*"}})

  # after request is received, add headers and allow the following methods
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # return all available categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.order_by(Category.id).all()
      categories = [category.type for category in categories]

      if len(categories) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'categories': categories,
      })

  # return a list of questions, number of total questions, current category, categories
  # pagination (every 10 questions)
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    all_questions = Question.query.order_by(Question.id).all()
    paginate_questions = [question.format() for question in all_questions]

    if len(paginate_questions) == 0:
      abort(404)

    categories = set()
    for question in paginate_questions:
      categories.add(question['category'])

    all_categories = Category.query.order_by(Category.id).all()
    categories = [category.type for category in all_categories]

    return jsonify({
      'success': True,
      'questions': paginate_questions[start:end],
      'categories': categories,
      'total_questions': len(all_questions)
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    