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
        self.database_name = 'trivia-test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "nneka2000", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "How many states does matter have?", "answer": "three states", "category": 5, "difficulty": 1}    
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_question_retrival(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_question_retrival_exceeding_available_page(self):
        response = self.client().get('/questions?page=200')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_categories_retrival(self):
        response =self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    # def test_delete_question(self):
    #     response = self.client().delete('/questions/5') 
    #     data = json.loads(response.data) 

    #     question = Question.query.filter(Question.id == 5).one_or_none()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["question_deleted"], 5)   

    # def test_delete_question_not_found(self):
    #     response = self.client().delete('/questions/5') 
    #     data = json.loads(response.data) 

    #     question = Question.query.filter(Question.id == 5).one_or_none()
    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], 'unprocessable entity')

    def test_create_new_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)   
        self.assertTrue(data["question_id"])
        self.assertTrue((data["total_question"]))

    def test_create_new_question_on_wrong_endpoint(self):
        response = self.client().post('/questions/9', json=self.new_question)
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],'method not allowed')

    def test_search_questions_with_results(self):
        response = self.client().post('/questions/search', json={"searchTerm": "title"}) 
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_search_questions_without_results(self):
        response = self.client().post('/questions/search', json={"searchTerm": "fang"}) 
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"], [])

    def test_get_questions_in_category(self):
        response = self.client().get('categories/1/questions')
        data = json.loads(response.data)

        questions = Question.query.filter(Question.category == 1)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data["success"], True)

    def test_get_questions_in_category(self):
        response = self.client().get('categories/0/questions')
        data = json.loads(response.data)

        questions = Question.query.filter(Question.category == 3)
        self.assertEqual(response.status_code, 422)   
        self.assertEqual(data["success"], False)

    def test_quiz_play(self):
        response = self.client().post('/quizzes', json={'prev': 2, 'category':2})
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data["success"], True)    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    