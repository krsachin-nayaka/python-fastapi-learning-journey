# FastAPI — Day 4&5

## Request Body, Pydantic Models, Validation & Response Models

Today I learned how FastAPI receives structured data from a client, validates that data using Pydantic, and controls the data returned to the client using Response Models.

---

# 1. Request Body

## What is a Request Body?

A **request body** is the data sent by the client to the server as part of an HTTP request.

It is commonly used with:

* `POST`
* `PUT`
* `PATCH`

For example, when creating a user, the client may need to send:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}
```

Instead of putting all this information into the URL, we send it as structured data in the request body.

---

## Why do we use a Request Body?

Suppose we want to create a user.

Putting everything in the URL would look like:

```text
/create?name=Sachin&age=20&mobile=9663089600
```

This becomes difficult to manage when there are many fields.

A request body allows us to send clean structured data:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663221220
}
```

This is easier to understand, validate, maintain, and extend.

---

# 2. JSON

FastAPI commonly receives request body data in **JSON format**.

JSON means **JavaScript Object Notation**.

Example:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}
```

Here:

```text
name   → string
age    → integer
mobile → integer
```

The JSON represents the data being sent from the client to the API.

---

# 3. Pydantic

FastAPI uses **Pydantic** for data parsing and validation.

We can create a Pydantic model using:

```python
from pydantic import BaseModel
```

Then define our expected data structure:

```python
class User(BaseModel):
    name: str
    age: int
    mobile: int
```

This model tells FastAPI:

> "I expect the request body to contain `name`, `age`, and `mobile`, and these fields should have the specified data types."

---

# 4. Pydantic BaseModel

`BaseModel` is the base class provided by Pydantic.

When we write:

```python
class User(BaseModel):
    name: str
    age: int
    mobile: int
```

`User` becomes a Pydantic model.

It gives us useful features such as:

* Data parsing
* Data validation
* Type checking
* Structured data handling
* Conversion/serialization support

---

# 5. Using a Pydantic Model in FastAPI

Example:

```python
from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    mobile: int


app = FastAPI()


@app.post("/create")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
    }
```

The important part is:

```python
def create_user(user: User):
```

Here:

```text
user
  ↓
instance containing the validated request data

User
  ↓
Pydantic model defining the expected structure
```

FastAPI understands that `user` should be created from the request body according to the `User` model.

---

# 6. Mental Model — Request Body

The easiest way to remember this is:

```text
CLIENT
   |
   | JSON Request Body
   ↓
Uvicorn
   |
   ↓
FastAPI
   |
   ↓
Pydantic Model
   |
   | Parse + Validate
   ↓
Endpoint Function
   |
   ↓
Response
```

For example:

```text
Client sends:

{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}

          ↓

Pydantic checks the structure and data types

          ↓

Endpoint receives validated data

          ↓

Application processes the data

          ↓

FastAPI sends a response
```

---

# 7. Data Validation

One of the biggest advantages of using Pydantic models is **automatic validation**.

Suppose our model says:

```python
class User(BaseModel):
    name: str
    age: int
    mobile: int
```

Then `age` is expected to be an integer.

Correct:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}
```

Incorrect:

```json
{
    "name": "Sachin",
    "age": "twenty one",
    "mobile": 9663089600
}
```

The second request fails because:

```text
age → expected integer
age → received "twenty one"
```

FastAPI/Pydantic returns a validation error instead of passing invalid data to the endpoint.

---

# 8. HTTP 422 — Validation Error

When the request reaches the correct endpoint but the submitted data doesn't satisfy the expected validation rules, FastAPI commonly returns:

```text
422 Unprocessable Content
```

Example:

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": [
                "body",
                "age"
            ],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "twenty one"
        }
    ]
}
```

Let's understand this response.

### `type`

```text
int_parsing
```

The problem occurred while trying to parse the value as an integer.

### `loc`

```text
["body", "age"]
```

This tells us where the problem occurred:

```text
body
  ↓
age
```

### `msg`

Describes the validation problem.

### `input`

Shows the value that caused the problem:

```text
"twenty one"
```

---

# 9. Validation Happens Before the Endpoint

This is an important concept.

Suppose we have:

```python
@app.post("/create")
def create_user(user: User):
    print("Function executed")
    return user
```

If the request contains invalid data, Pydantic validation fails before the endpoint gets the validated `user` value.

Mental model:

```text
Request
   ↓
Route Matching
   ↓
Request Body Processing
   ↓
Pydantic Validation
   ↓
     ├── Invalid → 422 Response
     |
     └── Valid
           ↓
      Endpoint Function
           ↓
        Response
```

So validation protects the application from receiving incorrectly structured input.

---

# 10. Swagger UI

FastAPI automatically provides interactive API documentation.

We can open:

```text
http://127.0.0.1:8000/docs
```

This opens **Swagger UI**.

Swagger UI allows us to:

* See available API endpoints
* See HTTP methods
* See request body schemas
* Enter test data
* Send HTTP requests
* See responses
* Test validation errors

---

# 11. Swagger is a Client for Testing

Swagger UI is not our actual application frontend.

It acts as a convenient client for testing our API.

Mental model:

```text
Swagger UI
    |
    | HTTP Request
    ↓
Uvicorn
    |
    ↓
FastAPI
    |
    ↓
Endpoint
    |
    ↓
Response
    |
    ↓
Swagger UI
```

Later, a real frontend such as:

* React
* Angular
* Mobile application
* Another backend service

could send the same API requests.

---

# 12. Important HTTP Errors Learned

During request testing, we also understood different types of errors.

## 404 — Not Found

The requested path does not exist.

Example:

```text
GET /wrong-url
```

when `/wrong-url` has not been registered.

Mental model:

```text
URL does not match any route
        ↓
404 Not Found
```

---

## 405 — Method Not Allowed

The URL exists, but the HTTP method is not allowed for that route.

For example:

```python
@app.post("/create")
```

This route accepts:

```text
POST /create
```

But if we directly open:

```text
GET /create
```

the server can find `/create`, but that route does not accept GET.

Therefore:

```text
405 Method Not Allowed
```

Mental model:

```text
Path exists
    +
HTTP method is wrong
    ↓
405
```

---

## 422 — Validation Error

The path and method are correct, but the submitted data doesn't satisfy the expected validation rules.

Mental model:

```text
Path correct
    +
Method correct
    +
Data invalid
    ↓
422
```

---

# 13. Request Model

A **request model** defines the structure of data that the client is expected to send.

Example:

```python
class UserCreate(BaseModel):
    name: str
    age: int
    mobile: int
    password: str
```

This describes the incoming request.

Mental model:

```text
REQUEST MODEL

Client
  ↓
What data should I send?
```

---

# 14. Response Model

A **response model** defines the structure of data that the server should return to the client.

We use:

```python
response_model=UserResponse
```

Example:

```python
class UserResponse(BaseModel):
    name: str
    age: int
    mobile: int
```

Then:

```python
@app.post("/create", response_model=UserResponse)
def create_user(user: UserCreate):
    return user
```

Here:

```text
UserCreate
    ↓
Incoming data

UserResponse
    ↓
Outgoing data
```

---

# 15. Why Do We Need a Response Model?

Response models give us control over the data exposed by our API.

Imagine the client sends:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600,
    "password": "Sachin@123"
}
```

The password should not normally be returned to the client.

So we define:

```python
class UserResponse(BaseModel):
    name: str
    age: int
    mobile: int
```

Notice that `password` is not included.

Then:

```python
@app.post("/create", response_model=UserResponse)
def create_user(user: UserCreate):
    return user
```

The response is shaped according to `UserResponse`.

The client receives:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}
```

The password is not exposed in the response.

---

# 16. Request Model vs Response Model

This is one of the most important concepts from today.

| Model          | Purpose                         |
| -------------- | ------------------------------- |
| Request Model  | Defines what the client sends   |
| Response Model | Defines what the server returns |

Think of an API like a door:

```text
             API
              |
      ┌───────┴───────┐
      ↓               ↓
   INCOMING         OUTGOING
      ↓               ↓
Request Model     Response Model
      ↓               ↓
Client → Server   Server → Client
```

---

# 17. Complete Example

A more realistic example is:

```python
from fastapi import FastAPI
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    mobile: int
    password: str


class UserResponse(BaseModel):
    name: str
    age: int
    mobile: int


app = FastAPI()


@app.post("/create", response_model=UserResponse)
def create_user(user: UserCreate):
    return user
```

Request:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600,
    "password": "Sachin@123"
}
```

Response:

```json
{
    "name": "Sachin",
    "age": 20,
    "mobile": 9663089600
}
```

---

# 18. Complete Mental Model of Today's Learning

This is the most important mental model to remember:

```text
                    CLIENT
                       |
                       | HTTP Request
                       | JSON Body
                       ↓
                  ┌──────────┐
                  │ Uvicorn  │
                  └────┬─────┘
                       ↓
                  ┌──────────┐
                  │ FastAPI  │
                  └────┬─────┘
                       ↓
                 Route Matching
                       ↓
                Request Model
                       ↓
              Pydantic Validation
                       |
             ┌─────────┴─────────┐
             ↓                   ↓
          Invalid               Valid
             ↓                   ↓
            422              Endpoint
                                 ↓
                           Application Logic
                                 ↓
                         Response Model
                                 ↓
                            JSON Response
                                 ↓
                               CLIENT
```

In simple words:

> **The client sends JSON data → Uvicorn receives the HTTP request → FastAPI finds the correct route → Pydantic parses and validates the request data → the endpoint function processes the valid data → the response model controls the outgoing data → FastAPI sends the response back to the client.**

---

# 19. Key Points to Remember

### Request Body

Used to send structured data to the API.

### Pydantic

Used by FastAPI for parsing and validating structured data.

### `BaseModel`

Used to define the expected data structure.

### Request Model

Defines what the API expects from the client.

### Response Model

Defines what the API sends back to the client.

### Swagger UI

Provides an interactive interface for testing and documenting the API.

### 404

Route/path doesn't exist.

### 405

Path exists, but HTTP method is not allowed.

### 422

Request data failed validation.

---

# 20. Interview Questions

### Q1. What is a request body?

A request body contains data sent by the client to the server, commonly in JSON format for POST, PUT, and PATCH requests.

### Q2. What is Pydantic?

Pydantic is a Python library used for data parsing and validation. FastAPI uses it to validate request and response data.

### Q3. What is `BaseModel`?

`BaseModel` is the Pydantic base class used to define structured data models with fields and types.

### Q4. What is `response_model`?

`response_model` defines the expected structure of the response returned by an API endpoint. FastAPI uses it for response validation, serialization, documentation, and filtering.

### Q5. Difference between request and response models?

A request model defines the data accepted from the client, while a response model defines the data returned to the client.

### Q6. What happens when request data fails validation?

FastAPI returns a validation error, commonly with HTTP status code `422`, and the endpoint function is not executed with the invalid data.

### Q7. Is Swagger the actual frontend of the application?

No. Swagger UI is an automatically generated API documentation and testing interface. A real frontend or another client can communicate with the same API.

---

# 21. Today's Main Takeaway

The most important thing I learned today is:

```text
REQUEST
Client → JSON → FastAPI → Pydantic → Validation

PROCESSING
Validated Data → Endpoint Function → Application Logic

RESPONSE
Application Result → Response Model → JSON → Client
```

FastAPI is not just about creating routes.

It also provides a structured way to:

* Receive data
* Validate data
* Process data
* Control response data
* Document APIs
* Handle invalid requests

This forms the foundation for building reliable and production-style APIs.
