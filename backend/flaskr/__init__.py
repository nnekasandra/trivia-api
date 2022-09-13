import os
from re import search
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination(questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    format_questions = [ques.format() for ques in questions]
    current_questions = format_questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTION"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def all_categories():
        try:
            categories = Category.query.all()
            format_category = {category.id:category.type for category in categories}
            if len(categories) == 0:
                abort(404)
            return jsonify(
            {
                'success': True,
                'category': len(format_category),
                'categories': format_category
            }  
            )
        except:
            abort(422)    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.all()
            current_questions = pagination(questions)
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'total_questions': len(Question.query.all()),
                'questions': current_questions,
                'categories': {category.id : category.type for category in categories},
                'current_category': 'History'
            })
        except:
            abort(422) 
                
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            if question is None:
                abort(404)
            question.delete()
            questions = Question.query.all()
            current_questions = pagination(questions)
            return jsonify({
                'success': True,
                'total_questions': len(Question.query.all()),
                'question_deleted': question_id
            })
        except:
            abort(422)        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        question = Question(question=new_question, answer=new_answer,  category=new_category, difficulty=new_difficulty)
        question.insert()   

        return jsonify({
                'success': True,
                'question_id': question.id,
                'total_question': len(Question.query.all())
                })   
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
            body = request.get_json()
            search_term = body.get('searchTerm')
            #questions = Question.query.filter(Question.question.ilike( f'%{search_term}%' )).all()
            questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))
                )
            current_questions = pagination(questions)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_question': len(current_questions),
                'current_category': 'All'
            })
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):
        category_ide = Category.query.get_or_404(category_id)
        questions = Question.query.filter(Question.category == category_id)
        current_questions = pagination(questions)
        return jsonify({
                'success': True,
                'questions': current_questions,
                'total_question': len(current_questions),
                'current_category': category_ide.type
            })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes/<category>/<prev>', methods=['POST'])
    def play_quiz(category, prev):
        body = request.get_json()
        prev = body.get('previous_questions')
        category = body.get('quiz_category')
        questions = Question.query.all()
        random_question = [question for question in questions]
        # categories = Category.query.all()
        # loopcat =[cat.type for cat in category]
        # ques = Question.query.filter(Question.category == loopcat)
        
        return jsonify({
            'success': True,
            'prev_question': prev,
            'quiz_category': category,
            'question': random_question

        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable entity"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "internal server error"}),
            500,
        )

    return app

