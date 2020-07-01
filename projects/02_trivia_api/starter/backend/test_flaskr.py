import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_paginate(self):
        """
        Tests paginate function
        """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) <= 10)

    def test_get_categories(self):
        """
        Tests get_categories function
        """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """
        Tests get_questions function
        """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_delete_question(self):
        """
        Tests delete_question function
        """
        response = self.client().delete('/questions/50')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == 50).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 50)
        self.assertEqual(question, None)

    def test_create_question(self):
        """
        Tests create_question function
        """
        total_questions_before = len(Question.query.all())
        new_question = {
            "question": "question?",
            "answer": "answer!",
            "category": "1",
            "difficulty": "2"
        }
        response = self.client().post('questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        added_question = data['total_questions'] - total_questions_before
        self.assertTrue(added_question, 1)

    def test_search_question(self):
        """
        Tests search_question function
        """
        search = {
            "search_term": "original"
        }
        response = self.client().post('search_question', json=search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) >= 1)

    def test_get_questions_by_category(self):
        """
        Tests get_question_by_category function
        """
        response = self.client().get('/category/4/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['category'] == "History")

    def test_play_trivia(self):
        """
        Tests play_trivia function
        """
        response = self.client().post(
            'quizzes', data=json.dumps({
                "previous_questions": [10, 2],
                "quiz_category": {"type": "History", "id": "4"},
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()