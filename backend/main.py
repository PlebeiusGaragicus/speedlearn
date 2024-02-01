from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

from models import *
from bson import ObjectId


app = FastAPI()

MONGO_DB_URI = "mongodb://localhost:27017"
client = MongoClient( MONGO_DB_URI )
db = client["speedlearn"]


# User endpoints
@app.get("/users", response_model=List[User])
async def read_users():
    users = list(db.users.find())
    return users

@app.post("/users", response_model=User)
async def create_user(user: UserBase):
    user_id = db.users.insert_one(user.dict()).inserted_id
    return {**user.dict(), "id": str(user_id)}


# Question endpoints
@app.get("/questions", response_model=List[Question])
async def read_questions():
    questions = list(db.questions.find())
    for q in questions:
        print(q)
    
    # return questions
    return [{**question, "id": str(question["_id"])} for question in questions]



# @app.get("/questions/{question_id}", response_model=Question)
# async def read_question(question_id: str):
#     question = db.questions.find_one({"_id": ObjectId(question_id)})
#     if question is None:
#         raise HTTPException(status_code=404, detail="Question not found")
#     return {**question, "id": str(question["_id"])}
#     # return question

@app.delete("/questions/{question_id}", response_model=Question)
async def delete_question(question_id: str):
    question = db.questions.find_one({"_id": ObjectId(question_id)})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db.questions.delete_one({"_id": ObjectId(question_id)})
    return {**question, "id": str(question["_id"])}


@app.post("/questions", response_model=Question)
def create_question(question: QuestionBase):
    question_id = db.questions.insert_one(question.dict()).inserted_id
    return {**question.dict(), "id": str(question_id)}


# Test endpoints
@app.get("/tests", response_model=List[Test])
async def read_tests():
    tests = list(db.tests.find())
    return tests

@app.post("/tests", response_model=Test)
async def create_test(test: TestBase):
    test_id = db.tests.insert_one(test.dict()).inserted_id
    return {**test.dict(), "id": str(test_id)}


# UserTest endpoints
@app.get("/usertests", response_model=List[UserTest])
async def read_user_tests():
    user_tests = list(db.usertests.find())
    return user_tests

@app.post("/usertests", response_model=UserTest)
async def create_user_test(user_test: UserTestBase):
    user_test_id = db.usertests.insert_one(user_test.dict()).inserted_id
    return {**user_test.dict(), "id": str(user_test_id)}
