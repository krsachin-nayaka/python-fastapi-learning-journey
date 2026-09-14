# FastAPI Dependency Injection

## 📌 Day- 6 — Dependency Injection

Dependency Injection is one of the important features of FastAPI. It helps us create reusable logic and allows FastAPI to automatically provide the required data or resources to an API endpoint.

---

# 1. What is Dependency Injection?

Before understanding Dependency Injection, we need to understand two things:

* Dependency
* Injection

### Dependency

A **dependency** is something that an endpoint function needs in order to perform its operation.

For example, an endpoint may need:

* Current user
* Database connection
* Authentication information
* Common query parameters
* Application settings
* Permission information

Instead of writing this supporting logic directly inside every endpoint, we can create separate reusable functions.

These functions are called **dependency functions**.

### Injection

**Injection** means providing the result of the dependency to the endpoint function that needs it.

FastAPI automatically:

1. Finds the dependency.
2. Executes the dependency.
3. Gets the result.
4. Provides/injects that result into the endpoint.
5. Executes the endpoint.
6. Sends the final response to the client.

### Simple Definition

> Dependency Injection in FastAPI is a mechanism where reusable dependency functions provide the required data or resources to an endpoint, and FastAPI automatically executes those dependencies and injects their results into the endpoint.

---

# 2. Simple Mental Model

Think about an endpoint as a person who needs some tools to perform a job.

For example:

```text
Endpoint
   ↓
"I need the current user"
   ↓
Dependency function
   ↓
Finds/provides the current user
   ↓
FastAPI injects the user
   ↓
Endpoint performs its main operation
   ↓
Final response
```

The endpoint does not need to manually perform every supporting task.

FastAPI manages the dependency process.

---

# 3. Why Do We Need Dependencies?

Imagine we have multiple endpoints:

```text
GET  /profile
GET  /orders
GET  /payments
GET  /dashboard
```

All of them need to know the current user.

Without dependencies, we might write authentication/user lookup logic inside every endpoint.

That creates duplicate code:

```text
/profile
    → authentication logic

/orders
    → authentication logic

/payments
    → authentication logic

/dashboard
    → authentication logic
```

Instead, we can create one reusable dependency:

```python
def get_current_user():
    ...
```

Then use it wherever required.

```text
get_current_user()
       ↓
 ┌─────┼─────┬──────────┐
 ↓     ↓     ↓          ↓
profile orders payments dashboard
```

The logic is written once and reused.

---

# 4. Creating a Dependency Function

A dependency function is usually a normal Python function.

Example:

```python
def get_user():
    return {
        "id": 101,
        "name": "Sachin"
    }
```

This function has one responsibility:

> Provide user information.

At this point, it is simply a normal Python function.

It becomes a FastAPI dependency when we use it with `Depends()`.

---

# 5. `Depends()`

FastAPI provides:

```python
Depends()
```

We import it from FastAPI:

```python
from fastapi import FastAPI, Depends
```

Then we can use our dependency:

```python
@app.get("/profile")
def profile(user=Depends(get_user)):
    return {
        "user": user
    }
```

The important part is:

```python
Depends(get_user)
```

This tells FastAPI:

> The `user` parameter should be obtained from the `get_user` dependency.

---

# 6. Complete Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()


def get_user():
    return {
        "id": 101,
        "name": "Sachin"
    }


@app.get("/profile")
def profile(user=Depends(get_user)):
    return {
        "message": "Profile accessed",
        "user": user
    }
```

---

# 7. How This Code Works

Let's understand it step by step.

## Step 1 — Client sends a request

The client sends:

```text
GET /profile
```

---

## Step 2 — FastAPI finds the endpoint

FastAPI finds:

```python
@app.get("/profile")
def profile(user=Depends(get_user)):
```

FastAPI notices that the endpoint has a dependency:

```python
Depends(get_user)
```

---

## Step 3 — FastAPI executes the dependency

FastAPI calls:

```python
get_user()
```

The dependency returns:

```python
{
    "id": 101,
    "name": "Sachin"
}
```

---

## Step 4 — FastAPI injects the result

FastAPI provides the dependency result to the endpoint.

Conceptually, it becomes:

```python
profile(
    user={
        "id": 101,
        "name": "Sachin"
    }
)
```

The endpoint can now use `user`.

---

## Step 5 — Endpoint performs its operation

The endpoint executes:

```python
return {
    "message": "Profile accessed",
    "user": user
}
```

---

## Step 6 — FastAPI sends the response

The final response is sent to the client:

```json
{
    "message": "Profile accessed",
    "user": {
        "id": 101,
        "name": "Sachin"
    }
}
```

---

# 8. Complete Request Flow

The complete flow can be remembered as:

```text
Client
  ↓
HTTP Request
  ↓
FastAPI
  ↓
Find Endpoint
  ↓
Check Dependencies
  ↓
Execute Dependency
  ↓
Dependency Returns Result
  ↓
FastAPI Injects Result
  ↓
Endpoint Executes
  ↓
Endpoint Returns Result
  ↓
FastAPI Creates HTTP Response
  ↓
Client
```

This is the most important mental model for Dependency Injection.

---

# 9. Important Difference: `get_user` vs `get_user()`

This is an important Python concept.

### We write:

```python
Depends(get_user)
```

and not:

```python
Depends(get_user())
```

Why?

Because:

```python
get_user
```

means:

> Here is the function. FastAPI can call it when needed.

While:

```python
get_user()
```

means:

> Execute the function now.

FastAPI needs the function itself so that it can control when and how the dependency is executed.

Therefore:

```python
Depends(get_user)
```

is the correct pattern.

---

# 10. `Depends()` Does Not Immediately Return the Dependency Result

This is another important mental model.

When we write:

```python
Depends(get_user)
```

we should not think:

```text
Depends() → immediately gives user
```

Instead think:

```text
Depends(get_user)
        ↓
Instruction to FastAPI
        ↓
"Use get_user as a dependency"
```

FastAPI later executes:

```python
get_user()
```

and injects the returned result into the endpoint.

---

# 11. Dependency Functions Can Receive Parameters

Dependency functions can also require data.

Example:

```python
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Sachin"
    }
```

We can use it as:

```python
@app.get("/profile")
def profile(user=Depends(get_user)):
    return user
```

Now a request such as:

```text
GET /profile?user_id=101
```

allows FastAPI to obtain:

```text
user_id = 101
```

and use it when resolving the dependency.

Conceptually:

```text
Request
   ↓
user_id = 101
   ↓
get_user(user_id=101)
   ↓
User object
   ↓
profile(user=User)
   ↓
Response
```

This shows that dependencies can participate in FastAPI's request parameter handling and validation system.

---

# 12. Dependency Chaining

A dependency can itself depend on another dependency.

Example:

```python
def get_db():
    return "Database connection"


def get_user(db=Depends(get_db)):
    return {
        "name": "Sachin",
        "database": db
    }


@app.get("/profile")
def profile(user=Depends(get_user)):
    return user
```

Here:

```text
profile
   ↓
get_user
   ↓
get_db
```

The endpoint depends on `get_user`.

`get_user` depends on `get_db`.

FastAPI resolves the dependencies in the required order.

### Execution flow

```text
Request
   ↓
profile()
   ↓
Needs get_user()
   ↓
get_user() needs get_db()
   ↓
get_db()
   ↓
Database connection
   ↓
get_user(db)
   ↓
User information
   ↓
profile(user)
   ↓
Response
```

This is called **dependency chaining** or **dependency graph resolution**.

---

# 13. Dependencies Do Not Always Need to Return Data

A dependency can also perform a check or validation.

For example:

```python
def verify_admin():
    # Check whether the user is an administrator
    ...
```

The purpose of this dependency may simply be:

```text
Allow the request
        OR
Reject the request
```

For example:

```python
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin=Depends(verify_admin)
):
    return {
        "message": "User deleted"
    }
```

Here the dependency can verify permissions before the endpoint performs the delete operation.

So a dependency can provide:

* Data
* Database resources
* Authentication
* Authorization
* Validation
* Configuration
* Other reusable supporting logic

---

# 14. Dependency with `yield`

Later, dependencies can also use `yield`.

A common database pattern looks like:

```python
def get_db():
    db = create_database_connection()

    try:
        yield db
    finally:
        db.close()
```

The basic idea is:

```text
Create resource
      ↓
Provide resource to endpoint
      ↓
Endpoint uses resource
      ↓
Request finishes
      ↓
Cleanup resource
```

This is especially useful for resources such as database sessions.

We will study `yield` dependencies separately because they are important for production-level FastAPI applications.

---

# 15. Real-World Uses of Dependency Injection

Dependency Injection is commonly used for:

### Authentication

```python
Depends(get_current_user)
```

Used to identify the logged-in user.

### Authorization

```python
Depends(require_admin)
```

Used to check whether a user has permission.

### Database

```python
Depends(get_db)
```

Used to provide a database session/connection.

### Common Parameters

```python
Depends(common_parameters)
```

Used to reuse common query parameters.

### Application Settings

```python
Depends(get_settings)
```

Used to provide configuration.

### Reusable Business Logic

```python
Depends(some_service)
```

Used when multiple endpoints need the same supporting logic.

---

# 16. Benefits of Dependency Injection

Now that we understand the actual mechanism, we can understand why it is useful.

## 1. Reusability

Create logic once and use it in multiple endpoints.

```text
get_current_user()
       ↓
Profile
Orders
Payments
Dashboard
```

---

## 2. Less Duplicate Code

Instead of repeating authentication, database, or validation logic in every endpoint, we can centralize it in reusable dependencies.

---

## 3. Separation of Responsibilities

The endpoint can focus on its main business operation.

For example:

```text
Dependency
→ "Who is the user?"

Endpoint
→ "What should I do for this user?"
```

This makes the code easier to understand and maintain.

---

## 4. Easier Testing

Dependencies can be replaced during testing.

Conceptually:

```text
Production
API → Real Database

Testing
API → Test Database
```

This makes testing easier without changing the main endpoint logic.

---

## 5. Centralized Authentication and Authorization

Authentication and permission logic can be implemented once and reused across many endpoints.

---

## 6. Resource Management

Dependencies can manage resources such as database sessions and perform cleanup after the request.

---

# 17. Dependency Injection vs Normal Function Call

### Normal function call

```python
def get_user():
    return "Sachin"


@app.get("/")
def home():
    user = get_user()
    return {"user": user}
```

Here **we manually call** the function.

### Dependency Injection

```python
def get_user():
    return "Sachin"


@app.get("/")
def home(user=Depends(get_user)):
    return {"user": user}
```

Here **FastAPI manages the dependency**.

The key difference is:

```text
Normal function call
→ Developer controls the call

Dependency Injection
→ FastAPI manages dependency resolution and injection
```

---

# 18. Final Mental Model

Remember this flow:

```text
             CLIENT
                ↓
             REQUEST
                ↓
             FASTAPI
                ↓
        Check Endpoint
                ↓
       Check Dependencies
                ↓
        Execute Dependency
                ↓
       Dependency Result
                ↓
       Inject the Result
                ↓
        Endpoint Executes
                ↓
        Main Business Logic
                ↓
          Final Result
                ↓
       HTTP Response
                ↓
             CLIENT
```

### One-line memory trick

> **Dependency does the supporting work → FastAPI injects its result → Endpoint performs the main work → FastAPI sends the response.**

---

# 19. Key Terms to Remember

| Term                  | Meaning                                                          |
| --------------------- | ---------------------------------------------------------------- |
| Dependency            | Something an endpoint needs                                      |
| Dependency Function   | Reusable function that provides/handles that requirement         |
| `Depends()`           | Tells FastAPI to use a dependency                                |
| Injection             | FastAPI providing the dependency result to the endpoint          |
| Dependency Chaining   | One dependency depending on another                              |
| Dependency Resolution | FastAPI finding and executing dependencies in the required order |

---

# 20. What I Learned Today

I learned that a FastAPI dependency is a reusable function that handles some supporting requirement needed by an endpoint.

FastAPI can execute that dependency automatically using `Depends()` and inject the result into the endpoint function.

The endpoint then receives the required data or resource, performs its main business operation, and returns the final result to FastAPI, which sends the HTTP response back to the client.

The basic pattern is:

```python
def dependency():
    # supporting logic
    return result


@app.get("/")
def endpoint(data=Depends(dependency)):
    # main business logic
    return data
```

The overall concept is:

```text
Dependency
    ↓
Provides required thing
    ↓
FastAPI injects it
    ↓
Endpoint uses it
    ↓
Final response
```

---

# 📚 Next Concepts

After understanding basic Dependency Injection, the next concepts to learn are:

1. Dependency with Query Parameters
2. Dependency with Path Parameters
3. Dependency with Headers
4. Dependency Chaining
5. `yield` Dependencies
6. Database Dependency
7. Authentication using Dependencies
8. Authorization using Dependencies
9. Dependency Overrides for Testing
10. Router-level Dependencies

These concepts will take Dependency Injection from a basic idea to **production-level FastAPI usage**.
