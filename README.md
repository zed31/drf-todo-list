# TODO List API

[![Build Status](https://travis-ci.com/zed31/drf-todo-list.svg?branch=master)](https://travis-ci.com/zed31/drf-todo-list)
![David](https://img.shields.io/david/expressjs/express.svg)

This project consist of creating an API using Django Rest Framework technology. The goal of this API is to provide a business logic related to a
todo list.

# How it works

Todolist API have 2 main objects:
- TODO: Which is represented by a title and a description and an owner
- User: Which is represented by an email and a password which can be either a normal user and an administrator

## User side

An user can do the following things
- Perform CRUD operation on its own profile
- Perform CRUD operation on todo

## Administrator side

An administrator can do the following things:
- Perform CRUD operation on user
- Perform CRUD operation on todo
- Ban an user by updating its pofile

## Todo

Todo are objects without logic on it, basically a todo contains just the following fields:

| Field       | Description                  | Type       |
| ----------- | ---------------------------- | ---------- |
| title       | The title of the todo        | CharField  |
| description | The description of the todo  | TextField  |
| owner       | The owner (User) of the task | ForeignKey |
| status      | Status of the todo           | Choice     |

The following value applies to the Todo status:

| Status | Value       |
| ------ | ----------- |
| C      | Created     |
| P      | In progress |
| D      | Done        |

## User

User are objects that allows you to authenticate through session authentication or even register
and access to your todo, the following fields compose the user:

| Field        | Description                                                                  | Type         |
| ------------ | ---------------------------------------------------------------------------- | ------------ |
| email        | The email used by the user to register or authenticate, must be unique       | EmailField   |
| password     | The password used by the user to register or authenticate                    | CharField    |
| is_superuser | Boolean used to detect if the user is an administrator or a regular user     | BooleanField |
| is_ban       | Boolean used to detect if the user is ban or not                             | BooleanField |

# Install the API

## Install manually

To install it, just clone the repository and run the following command:

`pip install -r <TODOLIST_REPOSITORY>/requirements.txt`

Or you can create a virtualenv like this:

```sh
virtualenv -p python3 venv
source venv/bin/activate
cd <TODOLIST_REPOSITORY>
pip install -r <TODOLIST_REPOSITORY>/requirements.txt

#Make sure everything worked:
cd <TODOLIST_REPOSITORY>
python3 manage.py test
```

Just replace the `TODOLIST_REPOSITORY` by the actual repository

**Make sure you have python3 installed**

## With docker

You can simply use docker-compose by running the following command:
```sh
git clonet <REPO>
docker-compose build
docker-compose up
```

# Run the server

To run the server simply use: `python3 manage.py runserver`

# Routes

In all paths containing a `PK`, replace the `PK` by the primary key

| Path                  | Description                                                             | Methods            |
| --------------------- | ----------------------------------------------------------------------- | ------------------ |
| /api/v1/              | List all the routes you can access from the API with your current state | GET                |
| /api/v1/auth/login    | Used by the user to logged in and create a session                      | POST               |
| /api/v1/auth/register | Used by a new user to register and be able to log in                    | POST               |
| /api/v1/auth/logout   | Logout the user                                                         | GET                |
| /api/v1/todo          | List all todos and allows you to create some                            | GET / POST         |
| /api/v1/todo/PK       | Allows a basic RUD on a specific todo                                   | GET / PUT / DELETE |
| /api/v1/users/        | List all users and allows administrator to create some                  | GET / POST         |
| /api/v1/users/PK      | Allows a basic RUD on a specific user                                   | GET / PUT / DELETE |

### User permission

The following permission tab applies for each normal user profiles

| Route                  | Method | Allowed        |
| ---------------------- | ------ | -------------- |
| /api/v1/               | GET    | Y              |
| /api/v1/auth/login/    | POST   | Y              |
| /api/v1/auth/register/ | POST   | Y              |
| /api/v1/auth/logout/   | GET    | Y              |
| /api/v1/todo/          | GET    | Y              |
| /api/v1/todo/          | POST   | Y              |
| /api/v1/todo/PK/       | GET    | Y (owner only) |
| /api/v1/todo/PK/       | PUT    | Y (owner only) |
| /api/v1/todo/PK/       | DELETE | Y (owner only) |
| /api/v1/users/         | GET    | N              |
| /api/v1/users/PK/      | GET    | Y (owner only) |
| /api/v1/users/PK/      | PUT    | Y (owner only) |
| /api/v1/users/PK/      | DELETE | Y (owner only) |

### Admin permission

The following permission tab applies to each administrator profiles

| Route                  | Method | Allowed |
| ---------------------- | ------ | ------- |
| /api/v1/               | GET    | Y       |
| /api/v1/auth/login/    | POST   | Y       |
| /api/v1/auth/register/ | POST   | Y       |
| /api/v1/auth/logout/   | GET    | Y       |
| /api/v1/todo/          | GET    | Y       |
| /api/v1/todo/          | POST   | Y       |
| /api/v1/todo/PK/       | GET    | Y       |
| /api/v1/todo/PK/       | PUT    | Y       |
| /api/v1/todo/PK/       | DELETE | Y       |
| /api/v1/users/         | GET    | Y       |
| /api/v1/users/PK/      | GET    | Y       |
| /api/v1/users/PK/      | PUT    | Y       |
| /api/v1/users/PK/      | DELETE | Y       |

# Request examples

## Registration example

To register a new user just do the following request to the api:

Make a `post` request on the route `/api/<api_version>/auth/register/`

Header:
```
Content-Type: application/json
```

Body:
```json
{
    "email": "foo.bar@gmail.com",
    "password": "secret_password"
}
```
## Login example

The login (if succeed) will return you the things you can do once you are logged in (i.e: All the route you can access). Login will also provides 2 things inside the cookies:
- The session id used to determine your session
- The CSRF token to prevent Cross Site Request Forgery

Make a `post` request on the route `/api/<api_version>/auth/login/`

Header:
```
Content-Type: application/json
```

Body:
```json
{
    "email": "foo.bar@gmail.com",
    "password": "secret_password"
}
```

## Create a todo

To create a todo you first need to create a session by login to the API, then execute a `post` request on the following route: `/api/<api_version>/todo/`

Header
```
Content-Type: application/json
X-CSRFToken: <generated_token>
```
The generated CSRFT token will be found in the same place as the sessionid, which is inside the cookies.

Body
```json
{
    "title": "title of the todo",
    "description" : "description of the todo"
}
```
