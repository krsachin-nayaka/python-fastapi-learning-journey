# FastAPI — Day 2

## Topics Covered

Today I learned:

1. Path Parameters
2. How Path Parameters work
3. Type Validation in Path Parameters
4. Query Parameters
5. Optional Query Parameters
6. Difference between Path Parameters and Query Parameters
7. Basic Request → FastAPI → Function → Response flow

---

# 1. Path Parameters

## What are Path Parameters?

A **Path Parameter** is a value that is included directly inside the URL path.

It is used when we want to identify a **specific resource**.

For example:

```text
/users/101
/users/102
/users/103
```

Here, `101`, `102`, and `103` can represent different user IDs.

Instead of creating a separate route for every user, we can create one dynamic route.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

---

# 2. How Path Parameters Work

The important part is:

```text
/users/{user_id}
```

The `{user_id}` inside the route means that this part of the URL is **dynamic**.

For example, if the client sends:

```text
GET /users/101
```

FastAPI takes:

```text
101
```

and passes it to the Python function:

```python
get_user(user_id=101)
```

The function returns:

```json
{
    "user_id": 101
}
```

If the client sends:

```text
GET /users/102
```

FastAPI passes:

```python
user_id = 102
```

and the response becomes:

```json
{
    "user_id": 102
}
```

So the same route can handle many different IDs.

---

# 3. Why Do We Use Path Parameters?

Path parameters are useful when the value identifies a particular resource.

For example:

### User

```text
/users/101
```

Means:

> Get the user whose ID is 101.

### Product

```text
/products/25
```

Means:

> Get product number 25.

### Student

```text
/students/45
```

Means:

> Get student number 45.

### Order

```text
/orders/5001
```

Means:

> Get order number 5001.

So the general idea is:

```text
Path Parameter → Identify a specific resource
```

---

# 4. Path Parameter with Database

In a real application, we normally do not just return the ID.

For example:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):

    # Find this user in the database
    user = database.find_user(user_id)

    return user
```

If the client requests:

```text
GET /users/101
```

the backend could search the database for user `101`.

The database might contain:

```text
ID    Name       Age
101   Sachin     21
102   Rahul      22
103   Anil       20
```

Then:

```text
GET /users/101
```

could return:

```json
{
    "id": 101,
    "name": "Sachin",
    "age": 21
}
```

This is how path parameters are commonly used in real backend applications.

---

# 5. Type Validation

We can specify the expected data type of a path parameter.

Example:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Here:

```python
user_id: int
```

means that `user_id` should be an integer.

### Valid request

```text
/users/101
```

FastAPI receives:

```text
101
```

and validates it as an integer.

### Invalid request

```text
/users/abc
```

`abc` cannot be converted into an integer.

FastAPI automatically returns a validation error instead of passing invalid data to the function.

This is one of the useful features of FastAPI.

---

# 6. Query Parameters

## What are Query Parameters?

A **Query Parameter** is additional information sent in the URL after a `?`.

Example:

```text
/users?name=sachin
```

Here:

```text
name=sachin
```

is a query parameter.

The general structure is:

```text
/path?key=value
```

For example:

```text
/users?name=sachin
```

* `/users` → path
* `?` → starts the query parameters
* `name` → parameter name
* `sachin` → parameter value

---

# 7. Creating a Query Parameter in FastAPI

Example:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users(name: str):
    return {"name": name}
```

Now we can send:

```text
GET /users?name=sachin
```

FastAPI receives:

```text
name = "sachin"
```

and calls the function:

```python
get_users(name="sachin")
```

The response will be:

```json
{
    "name": "sachin"
}
```

---

# 8. Multiple Query Parameters

We can have more than one query parameter.

Example:

```python
@app.get("/users")
def get_users(name: str, age: int):
    return {
        "name": name,
        "age": age
    }
```

The request can be:

```text
/users?name=sachin&age=21
```

Here:

```text
name = sachin
age = 21
```

The `&` is used to separate multiple query parameters.

FastAPI passes these values to the function:

```python
get_users(
    name="sachin",
    age=21
)
```

Response:

```json
{
    "name": "sachin",
    "age": 21
}
```

---

# 9. Optional Query Parameters

Sometimes a query parameter should not be mandatory.

We can make it optional.

Example:

```python
@app.get("/users")
def get_users(name: str | None = None):
    return {"name": name}
```

Here:

```python
name: str | None = None
```

means:

> `name` can contain a string, or it can be empty (`None`).

Now both requests are possible.

### With the parameter

```text
/users?name=sachin
```

Response:

```json
{
    "name": "sachin"
}
```

### Without the parameter

```text
/users
```

Response:

```json
{
    "name": null
}
```

This is useful when a parameter is optional.

---

# 10. Real-World Use of Query Parameters

Query parameters are commonly used for:

* Searching
* Filtering
* Sorting
* Pagination
* Optional settings

For example:

```text
/products?category=mobile
```

means:

> Get products from the mobile category.

Another example:

```text
/products?category=mobile&max_price=30000
```

means:

> Get mobile products with a maximum price of 30,000.

Another example:

```text
/products?sort=price
```

means:

> Sort the products based on price.

Pagination can also use query parameters:

```text
/products?page=2&limit=10
```

This could mean:

> Give me page 2 with 10 products.

---

# 11. Path Parameters vs Query Parameters

This is an important concept.

| Path Parameter                         | Query Parameter                             |
| -------------------------------------- | ------------------------------------------- |
| Part of the URL path                   | Comes after `?`                             |
| Uses `{}` in the route                 | Usually declared in the function            |
| Usually identifies a specific resource | Usually filters/searches/customizes results |
| Commonly required                      | Can be optional                             |
| Example: `/users/101`                  | Example: `/users?name=sachin`               |

### Simple way to remember

```text
Path Parameter
→ Which resource?

Query Parameter
→ What filter or option?
```

Example:

```text
/products/25
```

means:

> Give me product 25.

While:

```text
/products?category=mobile
```

means:

> Give me products filtered by mobile category.

---

# 12. How FastAPI Handles a Request

The request-response flow I learned is:

```text
Client
   ↓
HTTP Request
   ↓
Uvicorn
   ↓
FastAPI Application
   ↓
Routing
   ↓
Endpoint Function
   ↓
Business Logic / Database
   ↓
Response
   ↓
FastAPI
   ↓
Uvicorn
   ↓
Client
```

Let's understand this step by step.

### Step 1 — Client sends a request

For example:

```text
GET /users/101
```

The client could be:

* Browser
* Frontend application
* Mobile application
* Postman
* Another backend service

---

### Step 2 — Uvicorn receives the request

Uvicorn is the **ASGI server** that runs the FastAPI application.

It receives the incoming HTTP request and passes it to FastAPI.

---

### Step 3 — FastAPI checks the route

FastAPI checks the registered path operations.

For example:

```python
@app.get("/users/{user_id}")
```

FastAPI understands that this route handles:

```text
GET /users/<some value>
```

---

### Step 4 — FastAPI extracts the path parameter

If the request is:

```text
/users/101
```

FastAPI extracts:

```text
user_id = 101
```

Then it passes that value to the function.

---

### Step 5 — FastAPI executes the function

FastAPI calls:

```python
get_user(user_id=101)
```

The function can perform business logic or communicate with a database.

---

### Step 6 — Function returns the result

For example:

```python
return {"user_id": user_id}
```

FastAPI converts the returned Python data into an appropriate HTTP response.

JSON is very commonly used for API responses.

---

### Step 7 — Response goes back to the client

The response travels back through the server to the client.

Example:

```json
{
    "user_id": 101
}
```

---

# 13. Important Understanding About `@app`

Example:

```python
@app.get("/users")
def get_users():
    return {"message": "All users"}
```

Here:

```python
app = FastAPI()
```

creates the FastAPI application object.

The decorator:

```python
@app.get("/users")
```

registers the combination of:

```text
HTTP Method → GET
Path        → /users
Function    → get_users
```

So when the client sends:

```text
GET /users
```

FastAPI knows that it should execute:

```python
get_users()
```

The function name does **not** decide the URL.

For example:

```python
@app.get("/students")
def get_users():
    return {"message": "Students"}
```

The URL is still:

```text
/students
```

because the route was registered as:

```python
@app.get("/students")
```

The function name is simply a Python function name.

---

# 14. Day 2 Complete Example

Here is a small example combining path and query parameters:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }


@app.get("/users")
def get_users(
    name: str | None = None,
    age: int | None = None
):
    return {
        "name": name,
        "age": age
    }
```

### Path parameter request

```text
GET /users/101
```

Response:

```json
{
    "user_id": 101
}
```

### Query parameter request

```text
GET /users?name=sachin&age=21
```

Response:

```json
{
    "name": "sachin",
    "age": 21
}
```

Notice that these are two different routes:

```text
/users/{user_id}
```

and

```text
/users
```

The first uses a **path parameter**.

The second uses **query parameters**.

---

# 15. Key Points Learned Today

### Path Parameters

```text
/users/101
```

* Value is part of the URL path.
* Defined using `{}`.
* Commonly used to identify a specific resource.
* Can have type validation.

### Query Parameters

```text
/users?name=sachin
```

* Value comes after `?`.
* Commonly used for filtering, searching, sorting, and pagination.
* Can be required or optional.
* Multiple query parameters use `&`.

### FastAPI Routing

```python
@app.get("/users")
```

registers:

```text
GET + /users → endpoint function
```

### Request Flow

```text
Client
 ↓
Uvicorn
 ↓
FastAPI
 ↓
Routing
 ↓
Endpoint
 ↓
Business Logic / Database
 ↓
Response
 ↓
Client
```

---

# Day 2 Mental Model

The easiest way I remember today's concepts:

```text
Path Parameter
/users/101
       ↑
   Which user?
```

```text
Query Parameter
/users?name=sachin
       ↑
   What filter?
```

And for FastAPI:

```text
Request
   ↓
Route Matching
   ↓
Parameter Extraction
   ↓
Function Execution
   ↓
Business Logic / Database
   ↓
Response
```

---

# Day 2 Summary

Today I learned how FastAPI handles dynamic values in URLs using **Path Parameters** and additional filtering or optional information using **Query Parameters**.

I also understood how Uvicorn, FastAPI routing, endpoint functions, business logic, databases, and HTTP responses work together to process an API request.

The most important understanding from Day 2 is:

> **Path parameters usually identify the resource, while query parameters usually filter, search, sort, paginate, or customize the result.**

I also understood that:

> `@app.get()` registers an HTTP GET method and a URL path with the FastAPI application object. When a matching request arrives, FastAPI executes the associated endpoint function.
