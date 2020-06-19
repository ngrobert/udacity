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


  @app.after_request
  def after_request(response):
    """
    After request is received, add headers and allow the following methods
    """
    response.headers.add('Access-Control-Allow', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  def paginate(request, all_questions):
    """
    Paginate ten questions per page
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]
    return current_questions



  @app.route('/categories', methods=['GET'])
  def get_categories():
    """
    Return all available categories
    """
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

  @app.route('/questions', methods=['GET'])
  def get_questions():
    """
    Return a list of questions, number of total questions, current category, categories
    """
    all_questions = Question.query.order_by(Question.id).all()
    paginated_questions = paginate(request, all_questions)

    if len(paginated_questions) == 0:
      abort(404)

    categories = set()
    for question in paginated_questions:
      categories.add(question['category'])

    all_categories = Category.query.order_by(Category.id).all()
    categories = [category.type for category in all_categories]

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'categories': categories,
      'total_questions': len(all_questions)
    })


  # '''
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  # '''


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """
    Delete specified question
    """
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


  @app.route('/questions', methods=['POST'])
  def create_question():
    """
    Create new question with answer, category, and difficulty score
    """
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
        'category': category_type,
        'total_questions': len(all_questions)
      })

    except:
      abort(422)


  # '''
  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # '''


  @app.route('/search_question', methods=['POST'])
  def search_question():
    """
    Return questions based on a search term
    """
    try:
      body = request.get_json()
      search_term = body.get('search_term', None)
      found_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      paginated_questions = paginate(request, found_questions)

      if len(paginated_questions) == 0:
        abort(404)

      categories = set()
      for question in paginated_questions:
        categories.add(Category.query.get(question['category']).type)

      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'category': None,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  #
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  # '''


  @app.route('/category/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    """
    Return questions based on category
    """
    try:
      category_questions = Question.query.filter(Question.category == str(category_id)).order_by(
        Question.id).all()
      paginated_questions = paginate(request, category_questions)

      if len(paginated_questions) == 0:
        abort(404)

      chosen_category = Category.query.get(category_id).type

      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'category': chosen_category,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  # '''
  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.
  # '''

  @app.route('/trivia', methods=['POST'])
  def play_trivia():
    """
    endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    pass

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable entity"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error"
    }), 500

  return app

    