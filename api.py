from http import HTTPStatus
from fastapi import FastAPI
from src.data_handler import Sample


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


@app.post("/predict_car_price/")
async def _get_sample(sample: Sample) -> dict:
    """Receive a sample as dataclass and convert it to dictionary.
        ** The sample saved in a file in this commit. **

    Args:
        sample (Sample): contains the features value.

    Returns:
        dict: response information contains the sample as string type.
    """
    response:dict = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "price": sample.price
    }
    return response
