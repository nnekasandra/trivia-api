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

    ```pip install -r requirements.txt```

Run the flask App and see the app is inside the flaskr folder in the backend folder. See [here](https://flask.palletsprojects.com/en/2.2.x/quickstart) for instructions on how to set up and run a flask app.

#### Database Set up
This project uses postgres database. Ensure you have postgres database set up and running. Check [here](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm) for instructions to set up postgres server.

From the backend terminal run:

    ```
    psql trivia < trivia.psql

    ```
This populates the questions into the database for api manipulations.

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
*Base URL*: This project has not been deployed but the base url locally is `localhost:3000`.
*API KEY* : This API does not use API key and authenthication.

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
*Sample Request* : curl http://127.0.0.1:5000/categories
* Fetches and retrieves all the endpoints available.
* Request arguments: None
* Returns: a dictionary with the id and type of the category arranged as key value pairs.

*Sample Response*
```
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

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.
