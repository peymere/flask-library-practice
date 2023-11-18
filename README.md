# Library - Flask Practice

For this assessment, you'll be working with a Library book loan domain.

In this repo:

- There is a Flask application with some features built out.

You can either check your API by:

- Using Postman to make requests
- Building out a React frontend

## Setup

To download the dependencies, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Models

You will implement an API for the following data model:

![Library ERD](./library-ERD.png)

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

- A `Member` has many `Book`s through `Loan`
- A `Book` has many `Member`s through `Loan`
- A `Loan` belongs to a `Member` and belongs to a `Book`

Update `server/models.py` to establish the model relationships. Since a
`Loan` belongs to a `Member` and a `Book`, configure the model
to cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
or 
flask db migrate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

## Validations

Add validations to the `Loan` model:

- must have a `number_of_pages` greater than or equal to 1

## Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using to_dict() (don't forget the comma if specifying a
single field).

NOTE: If you choose to implement a Flask-RESTful app, you need to add code to
instantiate the `Api` class in server/app.py.

### GET /books

Return JSON data in the format below:

```json
[
  {
    "author": "Gayle Laakmann McDowell",
    "id": 1,
    "title": "Cracking the Coding Interview"
  },
  {
    "author": "Marijn Haverbeke",
    "id": 2,
    "title": "Eloquent JavaScript"
  },
  {
    "author": "Allen B. Downey",
    "id": 3,
    "title": "Think Python: How to Think Like a Computer Scientist"
  }
]
```

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using `to_dict()` (don't forget the comma if specifying
a single field).

### GET /books/<int:id>

If the `Book` exists, return JSON data in the format below:

```json
{
  "author": "Allen B. Downey",
  "id": 3,
  "title": "Think Python: How to Think Like a Computer Scientist",
  "loans": [
    {
      "id": 1,
      "member": {
        "id": 1,
        "name": "Emma",
        "year_joined": 2023
      },
      "book_id": 3,
      "check_out_date": "2023-11-17 23:32:24",
      "due_date": "2023-11-24 23:32:24",
      "member_id": 1
    }
  ]
}
```

If the `Book` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Book not found"
}
```

### DELETE /books/<int:id>

If the `Book` exists, it should be removed from the database, along with
any `Loan`s that are associated with it (a `Loan` belongs
to a `Book`). If you did not set up your models to cascade deletes, you
need to delete associated `Loan`s before the `Book` can be
deleted.

After deleting the `Book`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Book` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Book not found"
}
```

### GET /members

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "name": "Emma",
    "year_joined": 2023
  },
  {
    "id": 2,
    "name": "Taylor",
    "year_joined": 2023
  },
  {
    "id": 3,
    "name": "Kiki",
    "year_joined": 2023
  }
]
```

### POST /loans

This route should create a new `Loan` that is associated with an
existing `Book` and `Member`. It should accept an object with the following
properties in the body of the request:

```json
{
  "book_id": 1,
  "member_id": 3
}
```

If the `Loan` is created successfully, send back a response with the
data related to the `Loan`:

```json
{
  "id": 1,
  "member": {
    "id": 1,
    "name": "Emma",
    "year_joined": 2023
  },
  "book_id": 3,
  "due_date": 1,
  "check_out_date": 1,
  "book": {
    "author": "Gayle Laakmann McDowell",
    "id": 1,
    "title": "Cracking the Coding Interview",
    "number_of_pages": 100
  },
  "member_id": 1
}
```

If the `Loan` is **not** created successfully due to a validation
error, return the following JSON data, along with the appropriate HTTP status
code:

```json
{
  "errors": ["validation errors"]
}
```
