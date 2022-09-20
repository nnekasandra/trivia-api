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
    @DONE
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
            abort(404)    
    """
    @DONE
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
    @DONE
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
    @DONE
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if (not new_question or not new_answer  or
        not new_category or not new_difficulty):
         abort(422)   

        question = Question(
        question=new_question, 
        answer=new_answer, 
        category=new_category,
        difficulty=new_difficulty)

        question.insert()   

        return jsonify({
                'success': True,
                'question_id': question.id,
                'total_question': len(Question.query.all())
                })   
    """
    @DONE
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
            try:
                body = request.get_json()
                search_term = body.get('searchTerm')
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
            except:
                abort(422)    
    """
    @DONE
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):
        try:
            category_ide = Category.query.get_or_404(category_id)
            questions = Question.query.filter(Question.category == category_id)
            current_questions = pagination(questions)
            return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_question': len(current_questions),
                    'current_category': category_ide.type
                })
        except:
            abort(422)        
    """
    @DONE
    """

    @app.route('/quizzes', methods=['POST'])
    def play_trivia():
        body = request.get_json()
        
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
      
        try:
            
            if quiz_category['id'] == 0:
                questions = Question.query.filter(
                Question.id.notin_(previous_questions)).all()
                        
            else:
                questions = Question.query.filter(
                Question.category == quiz_category['id'],
                Question.id.notin_(previous_questions)).all()
                        
            if len(questions) > 0:
                next_question = random.choice(questions).format()
            else:
                next_question = None        
            return jsonify({
                    'success': True,
                    'question': next_question
                    })
        except:
            abort(422)
        
    """
    @DONE
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

