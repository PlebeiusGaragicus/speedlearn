from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import redis
import json

app = FastAPI()
rc = redis.Redis(host='localhost', port=6379, decode_responses=True)

class Quiz(BaseModel):
    username: str
    answers: dict

@app.post("/quizzes/")
async def create_quiz(quiz: Quiz):
    rc.set(quiz.username, json.dumps(quiz.answers))
    return {'message': 'Quiz added successfully'}

@app.get("/quizzes/")
async def get_all_quizzes():
    keys = rc.keys('*')
    quizzes = {key: json.loads(rc.get(key)) for key in keys}
    return quizzes

@app.get("/quizzes/{username}")
async def get_quiz(username: str):
    user_quiz = rc.get(username)
    if user_quiz:
        return {username: json.loads(user_quiz)}
    raise HTTPException(status_code=404, detail="Quiz not found")
