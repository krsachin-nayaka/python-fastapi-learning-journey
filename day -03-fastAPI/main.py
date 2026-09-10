```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users():
    return {"message": "Retrieve users"}


@app.post("/users")
def create_user():
    return {"message": "Create user"}


@app.put("/users/{user_id}")
def replace_user(user_id: int):
    return {"message": f"Replace user {user_id}"}


@app.patch("/users/{user_id}")
def update_user(user_id: int):
    return {"message": f"Partially update user {user_id}"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"Delete user {user_id}"}
```
