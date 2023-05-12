
# To Do List

This project is a small Django based Rest API that will allow you to create lists and tasks, and will allow you to mark a task as completed.

## Run Locally

Clone the project

```bash
  git clone https://github.com/codeplatoon-devops/to-do-list-django.git
```

Go to the project directory

```bash
  cd to-do-list-django
```

Create and activate Virtual Environment

```bash
  python -m venv `name_of_env`
  source `name_of_env`/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Create your database

```bash
  createdb to_do
```

Create .env file

```bash
    touch .env
```

Generate secret key and add it to your .env file under `SECRET_KEY`

```bash
  # this will generate a secret key copy and paste it onto your .env file under the variable SECRET_KEY
  python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Migrate migrations

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

## API Reference

### Get all Lists

```http
  GET /api/v1/lists/
```

### Get a Lists

```http
  GET /api/v1/lists/<int:id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. ID/PK of desired list |

### Get a task from a list

```http
  GET /api/v1/list/<int:id>/todos/<int:item_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `int` | **Required**. ID/PK of desired list |
| `item_id` | `int` | **Required**. ID/PK of desired task |

### Create a list

```http
  POST /api/v1/lists/
```

#### Data (application/json)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `str` | **Required**. Title of the list to be created |

### Create a task

```http
  POST /api/v1/lists/<int:id>/todos/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `int` | **Required**. ID/PK of desired list |

#### Data (application/json)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `str` | **Required**. Title of the task to be created |

### Mark a task as complete

```http
  PUT /api/v1/list/<int:id>/todos/<int:item_id>/complete/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `int` | **Required**. ID/PK of desired list |
| `item_id` | `int` | **Required**. ID/PK of desired task |


## Using Postman

Download postman [here](https://www.postman.com/downloads/). It has an excellent free tier - do not worry about signing up for anything. [Insomnia](https://insomnia.rest/download) is a popular open-source alternative however postman is still more widely used in the industry and is the tool we will use most in this course. 

Use postman to make http requests to your web app once its running. Depending on the host (localhost vs an ec2 instance) you may have to modify the urls in the example here. You will also want to change the id values used to create new todo lists and items, etc.

Download [this json file with a postman collection for this app](todo-list-django-postman-collection.json). Then in postman go to "File > Import" and then import 
