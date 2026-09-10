from fastapi import FastAPI

app = FastAPI()


# -------------------------
# Path Parameter
# -------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }


# -------------------------
# Query Parameters
# -------------------------

@app.get("/users")
def get_users(
    name: str | None = None,
    age: int | None = None
):
    return {
        "name": name,
        "age": age
    }
