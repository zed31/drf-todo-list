# TODO List API

This project consist of creating an API using Django Rest Framework technology. The goal of this API is to provide a business logic related to a
todo list.

## How it works

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


