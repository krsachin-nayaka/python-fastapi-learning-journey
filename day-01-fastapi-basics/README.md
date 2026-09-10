# Day 1 — UV and FastAPI Fundamentals

## 1. What is UV?

**UV** is a fast Python tool used for **Python project management, package management, and virtual environment management**.

Instead of using different tools for different tasks, UV can handle many common Python project tasks from one place.

I used UV to:

* Create a Python project
* Create and manage a virtual environment
* Install Python packages
* Manage project dependencies
* Run Python commands inside the project environment
* Run the FastAPI application

---

# 2. Creating a Python Project with UV

First, I created a project using:

```bash
uv init fastAPI_project
```

This creates a Python project with files used to manage the project.

The basic structure is:

```text
fastAPI_project/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
```

### What are these files?

### `.gitignore`

Tells Git which files and folders should not be uploaded to GitHub.

For example:

```text
.venv/
__pycache__/
```

The virtual environment should not be uploaded because it contains installed packages and can become very large.

---

### `.python-version`

Stores the Python version used by the project.

This helps keep the Python version consistent for the project.

---

### `README.md`

This file contains information and documentation about the project.

I use it to record:

* What I learned
* Commands I used
* Concepts I understood
* Project information

---

### `pyproject.toml`

This is an important Python project configuration file.

It contains information about the project and its dependencies.

For example, when I install FastAPI using UV, the dependency is recorded in `pyproject.toml`.

---

### `uv.lock`

This file records the exact dependency versions used by the project.

This helps make the project environment more consistent when the project is installed or developed on another machine.

---

# 3. Virtual Environment with UV

A **virtual environment** is an isolated environment for a Python project.

It allows each project to have its own packages and dependencies.

UV can create the virtual environment for the project.

The environment is created as:

```text
.venv/
```

I should **not upload `.venv/` to GitHub**.

Instead, `.gitignore` contains:

```text
.venv/
```

So Git ignores it.

---

# 4. Installing FastAPI Using UV

After creating the project, I installed FastAPI using:

```bash
uv add fastapi
```

This does more than simply downloading FastAPI.

UV:

1. Finds the FastAPI package
2. Installs it into the project environment
3. Records FastAPI as a project dependency
4. Updates `pyproject.toml`
5. Updates `uv.lock`

This makes dependency management easier.

---

# 5. Installing Uvicorn

To run the FastAPI application, I installed Uvicorn:

```bash
uv add uvicorn
```

### Important

**Uvicorn** and **Unicorn** are different.

I need **Uvicorn** for running the FastAPI application.

```text
Uvicorn → ASGI server
```

---

# 6. Running Python Through UV

UV can run Python inside the project's environment.

For example:

```bash
uv run python
```

This means UV runs Python using the project's environment.

I can also check whether FastAPI is installed:

```bash
uv run python -c "import fastapi; print(fastapi.__version__)"
```

If FastAPI is installed correctly, it prints the installed version.

---

# 7. Creating the FastAPI Application

Inside the project, I created:

```text
app/
└── main.py
```

The `app` folder contains my application code.

Inside `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()
```

### Understanding this code

```python
from fastapi import FastAPI
```

This imports the `FastAPI` class from the FastAPI framework.

FastAPI already provides many features required for building APIs.

For example:

* Request handling
* Routing
* Validation
* Response handling

Instead of building these things from scratch, I can use the features provided by FastAPI.

---

### `app = FastAPI()`

This creates a **FastAPI application object**.

The variable name `app` is just a normal Python variable.

It represents my FastAPI application.

---

# 8. What is Uvicorn?

**Uvicorn is an ASGI server.**

Its job is to run the FastAPI application and communicate with clients through HTTP.

I start my application using:

```bash
uv run uvicorn app.main:app --reload
```

Let's understand this command:

```text
app.main:app
│   │     │
│   │     └── FastAPI application object
│   └──────── main.py
└──────────── app folder
```

So:

```text
app.main:app
```

means:

> Go to the `app` folder → open `main.py` → find the FastAPI object named `app`.

### `--reload`

```bash
--reload
```

automatically reloads the server when I make code changes.

This is useful during development.

---

# 9. Creating the First API Route

I created my first route:

```python
@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```

Let's understand each part.

---

## `@app.get("/")`

This is a FastAPI decorator.

It tells FastAPI:

> When a client sends a GET request to `/`, execute the function below this decorator.

So FastAPI creates this connection:

```text
GET /  →  home()
```

---

## `def home():`

This is a normal Python function.

FastAPI calls this function when the matching request arrives.

---

## `return`

The function returns:

```python
{"message": "Hello FastAPI"}
```

FastAPI converts this into a JSON response.

The client receives:

```json
{
    "message": "Hello FastAPI"
}
```

---

# 10. Creating Another Route

I also created an `/about` route:

```python
@app.get("/about")
def about():
    return {"message": "This is About page"}
```

Now my application has two routes:

```text
GET /       → home()
GET /about  → about()
```

I can access the second route using:

```text
http://127.0.0.1:8000/about
```

---

# 11. What is a Route?

A **route** connects an HTTP method and URL path to a Python function.

For example:

```python
@app.get("/about")
def about():
    return {"message": "This is About page"}
```

creates:

```text
HTTP Method + Path
       ↓
GET + /about
       ↓
about()
       ↓
Response
```

The path `/about` is written in the decorator.

It does not need to be written inside the function.

---

# 12. What is GET?

**GET** is an HTTP method.

It is generally used when the client wants to **retrieve or request data** from the server.

For example:

```text
GET /students
```

could mean:

> "Give me the student data."

In my current example:

```text
GET /
```

means the client is requesting the resource available at `/`.

---

# 13. Basic Client → Server Flow

The complete flow I learned is:

```text
Client
   │
   │ HTTP GET Request
   ↓
Uvicorn
   │
   │ passes the request to the application
   ↓
FastAPI
   │
   │ finds the matching route
   ↓
Python Function
   │
   │ executes the logic
   ↓
Response
   │
   ↓
Client
```

For example:

```text
Browser
   ↓
GET /
   ↓
Uvicorn
   ↓
FastAPI
   ↓
home()
   ↓
{"message": "Hello FastAPI"}
   ↓
Browser
```

---

# 14. Difference Between UV, Uvicorn and FastAPI

This was one of the important things I understood today.

| Tool        | Main Purpose                                       |
| ----------- | -------------------------------------------------- |
| **UV**      | Python project, package and environment management |
| **Uvicorn** | Runs the FastAPI application as an ASGI server     |
| **FastAPI** | Python web framework used to build APIs            |
| **My Code** | Defines routes and application/business logic      |

A simple way to remember:

```text
UV
↓
Manages my Python project

Uvicorn
↓
Runs my application

FastAPI
↓
Provides the framework for building APIs

My Python code
↓
Defines what my API should do
```

---

# 15. My Day 1 Code

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/about")
def about():
    return {"message": "This is About page"}
```

---

# 16. Commands I Learned Today

### Create project

```bash
uv init fastAPI_project
```

### Install FastAPI

```bash
uv add fastapi
```

### Install Uvicorn

```bash
uv add uvicorn
```

### Run Python

```bash
uv run python
```

### Run FastAPI application

```bash
uv run uvicorn app.main:app --reload
```

### Check installed FastAPI version

```bash
uv run python -c "import fastapi; print(fastapi.__version__)"
```

---

# 17. Key Learning

Today I understood the basic architecture of a FastAPI application.

The important concepts are:

* UV manages the Python project and dependencies.
* A virtual environment keeps project dependencies isolated.
* FastAPI is a Python web framework for building APIs.
* Uvicorn runs the FastAPI application as an ASGI server.
* `FastAPI()` creates the application object.
* Routes connect HTTP methods and URL paths to Python functions.
* `GET` is used to request/retrieve resources.
* FastAPI converts Python return values into HTTP responses such as JSON.
* A client sends a request, FastAPI processes it through the matching route, and the server sends a response back to the client.

## Day 1 Completed ✅

Next: **FastAPI Path Parameters**
