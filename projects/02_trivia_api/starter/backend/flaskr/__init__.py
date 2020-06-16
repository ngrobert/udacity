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

  # paginates ten questions per page
  def paginate(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]

    return current_questions


  # return all available categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.order_by(Category.id).all()
      categories = [category.type for category in categories]
      try:
        if len(categories) == 0:
          abort(404)

        return jsonify({
          'success': True,
          'categories': categories,
        })

      except:
        abort(422)

  # return a list of questions, number of total questions, current category, categories
  @app.route('/questions', methods=['GET'])
  def get_questions():
    all_questions = Question.query.order_by(Question.id).all()
    ten_questions = paginate(request, all_questions)

    if len(ten_questions) == 0:
      abort(404)

    categories = set()
    for question in ten_questions:
      categories.add(question['category'])

    all_categories = Category.query.order_by(Category.id).all()
    categories = [category.type for category in all_categories]

    return jsonify({
      'success': True,
      'questions': ten_questions,
      'categories': categories,
      'total_questions': len(all_questions)
    })


  # '''
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  # '''


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      all_questions = Question.query.order_by(Question.id).all()

      if len(all_questions) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': len(all_questions)
      })

    except:
      abort(422)



  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.

  # Create new question with answer, category, and difficulty score
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
      category_id = body.get('category', None)
      new_question = Question(
        question=body.get('question', None),
        answer=body.get('answer', None),
        category=category_id,
        difficulty=body.get('difficulty', None)
      )
      new_question.insert()

      all_questions = Question.query.order_by(Question.id).all()
      category_type = Category.query.get(category_id).type

      return jsonify({
        'success': True,
        'created': new_question.id,
        'current_category': category_type,
        'total_questions': len(all_questions)
      })

    except:
      abort(422)


  # '''
  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # '''

  # get questions based on a search term
  @app.route('/search_question', methods=['POST'])
  def search_question():
    try:
      body = request.get_json()
      search_term = body.get('search_term', None)
      found_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%'))\
        .order_by(Question.id).all()
      current_questions = paginate(request, found_questions)

      if len(current_questions) == 0:
        abort(404)

      categories = set()
      for question in current_questions:
        categories.add(Category.query.get(question['category']).type)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'current_category': None,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)



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

    