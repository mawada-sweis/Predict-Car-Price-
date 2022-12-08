from http import HTTPStatus
from fastapi import FastAPI


# Define application
app = FastAPI()


# Check the connection is OK by initial path
@app.get("/")
def _health_check() -> dict:
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response
