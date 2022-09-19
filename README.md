# API Development and Documentation Final Project By Udacity Nanodegree Program

## Trivia App

### Introduction

Trivia App as the name goes is a Q & A platform where users can come and answer quizzes. It was a final project in the Udacity **API Development and Documentation** lesson. I implemented my knowledge about building and testing out API endpoints into this project.

![App Screenshot](https://cdn.hashnode.com/res/hashnode/image/upload/v1663517568480/CG88z0PZ4.png)

In this app, users are able to get questions they want to answer. Questions are arranged by category. They can add new questions to the trivia database, delete questions, search for questions and play trivia game by category.


## Getting Started

The project has both the frontend and backend servers running on `localhost:3000` and `localhost:5000` respectively.
If you want to have a feel of how the project is working, [Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine and work locally.

### Backend Pre-requisite

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Installation 
* Set up a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the project
* Install all the dependencies required to smoothly run the project.

```
pip install -r requirements.txt

```

Run the flask App and see the app is inside the flaskr folder in the backend folder. See [here](https://flask.palletsprojects.com/en/2.2.x/quickstart) for instructions on how to set up and run a flask app.

#### Database Set up
This project uses postgres database. Ensure you have postgres database set up and running. Check [here](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm) for instructions to set up postgres server.

From the backend terminal run to populate the questions into the database for api manipulations
 ```
    psql trivia < trivia.psql

```


### Frontend Pre-requisite
The frontend is built with React so install npm dependencies and start the frontend server. 


#### Installation
In the frontend terminal, run:

```
    npm install
    npm start
```    
## API Reference

### Introduction
The frontend consumes data from the backend and database using API the different API endpoints. There are endpoints to retrieve questions, categories, delete questions and so on.

### Getting Started
**Base URL**: This project has not been deployed but the base url locally is `localhost:3000`.
**API KEY** : This API does not use API key and authenthication.

### Error Handling 
There are different error that were specifically called out in this API
| Errors | Meaning | Description |
| ----------- | ----------- | ------------
| 500 | Internal Server Error | The server encountered some glitches and can not complete the requests. |
| 404 | Not found | The particular response/resource you are requesting is not available on the server. |
| 422 | Unprocessible Entity | Your requests is not properly formatted so the server can not process it. |
| 405 | Method not allowed | The method on the endpoint is not the correct method. |
| 400 | Bad Request | The request sent is bad and cannot be processed by the server. |

### Resource Endpoints Library
There are various endpoints for the requests you want to carry out.

#### GET Requests
```
`GET /categories`
Sample Request: curl http://127.0.0.1:5000/categories
* Fetches and retrieves all the endpoints available.
* Request arguments: None.
* Returns: a dictionary with the id and type of the category arranged as key value pairs.

Sample Response

{
  'categories': 
  { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" 
  }
}
```

```
GET '/questions?page=${integer}'
Sample Request: curl http://127.0.0.1:5000/questions or curl  http://127.0.0.1:5000/questions?page=1
* Fetches and retrieves all questions available paginated 10 books per page
* Return argument: Page
* Returns: dictionary with questions, total questions available, dictionary of categories in key value pairs and current category

Sample Response

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "History", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    ],
  "success": true, 
  "total_questions": 19
}  
```

```
GET 'categories/${id}/questions'
Sample Request: curl http://127.0.0.1:5000/categories/2/questions
* Fetches questions according to the categories
* Request Arguments: id - integer
* Returns: A dictionary of questions belonging to the category, total questions in the category and the category type.

Sample Response
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_question": 4
}
```

#### POST Requests
```
POST 'questions'
Sample Request: 
`curl -X POST -H "Content-Type: application/json" -d '{"question":"Which subject studies living and non-living things?", "answer":"Biology", "category":"1", "difficulty":"1"}' http://127.0.0.1:5000/questions  |jq '.'`
* Sends a post request to create a new question

Sample Request Body
{
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
}

```

```
POST '/questions'
Sample Request: 
curl -X POST -H"Content-Type: application/json" -d '{"searchTerm":"american"}'  http://127.0.0.1:5000/questions/search |jq '.'
* Sends a post request in order to search for a specific question by search term 
* Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
* Returns: dictionary containing an array of questions, a number of totalQuestions that met the search term and the current category string 

Sample Request Body
{
    'questions': [
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
    ],
    'total_questions': 100,
    'current_category': 'Entertainment'
}

```

```
POST '/quizzes'
* Sends a post request in order to get the next question 
* Sample Request Body:

{
    'previous_questions':  an array of question id's such as [1, 4, 20, 15]
    'quiz_category': a string of the current category 
}
* Returns: a single new question object 

Sample Response
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}

```
#### DELETE Request
```
DELETE '/questions/${id}'
Sample Request: curl -X DELETE http://127.0.0.1:5000/questions/2 |jq '.'
* Deletes a specified question using the id of the question
* Request Arguments: id - integer
* Returns: specific id of question deleted and the total question remaining in the database 

Sample Response
{
    'total_questions': 20,
    'question_deleted': 2
}
```
### Deployment
N/A

## Author (s)
Njoku Nneka Sandra

### Acknowledgement
Specially thankful to God Almighty for this growth opportunity. To the ALX-T for this opportunity to improve my skillset. Also to the Udacity team for the well structured learning environment that helped me pull through with this project. I am thankful to my friends Livinus and Edidiong for helping out when I encountered blockers during the course of doing this project.

