from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import redis
import json

app = FastAPI()
rc = redis.Redis(host='localhost', port=6379, decode_responses=True)

class TestResults(BaseModel):
    username: str
    answers: dict
    test_started: bool  # Added "test_started" field



@app.post("/tests/")
async def create_test(test: TestResults):
    """
    Create a new test.

    Args:
        test (TestResults): The test object containing the test details.

    Returns:
        dict: A dictionary with a message indicating the success of the operation.
    """

    test.test_started = False  # Set "test_started" to False initially
    rc.set(test.username, json.dumps(test.dict()))
    return {'message': 'test added successfully'}




@app.get("/tests/")
async def get_all_tests():
    """
    Retrieve all tests from the Redis cache.

    Returns:
        dict: A dictionary containing all tests.
    """

    keys = rc.keys('*')
    tests = {key: json.loads(rc.get(key)) for key in keys}
    return tests



@app.get("/tests/{username}")
async def get_test(username: str):
    user_test = rc.get(username)
    if user_test:
        return {username: json.loads(user_test)}
    raise HTTPException(status_code=404, detail="Test not found")



@app.post("/tests/{username}/answers/")
async def submit_answer(username: str, answer: str):
    user_test = rc.get(username)
    if user_test:
        test = json.loads(user_test)
        test['answers'] = answer
        rc.set(username, json.dumps(test))
        return {'message': 'Answer submitted successfully'}
    raise HTTPException(status_code=404, detail="Test not found")
