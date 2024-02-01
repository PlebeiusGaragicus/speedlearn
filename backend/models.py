from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

# Pydantic models
class UserBase(BaseModel):
    name: str

class User(UserBase):
    id: str

class QuestionType(str, Enum):
    TrueFalse = "True/False"
    Checkbox = "Checkbox"
    Radio = "Radio"
    Freeform = "Freeform"

class QuestionBase(BaseModel):
    question_type: QuestionType
    question: str
    choices: Optional[List[str]] = None  # For "Checkbox" and "Radio" types, this is a list of choices
    correct_answer: str
    subject: str
    source_document: str

class Question(QuestionBase):
    id: str

class TestBase(BaseModel):
    name: str
    question_ids: List[str]

class Test(TestBase):
    id: str

class UserTestBase(BaseModel):
    user_id: str
    test_id: str
    answers: List[dict]

class UserTest(UserTestBase):
    id: str