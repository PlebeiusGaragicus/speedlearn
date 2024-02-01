import os
import time
import json
import requests

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from bson import ObjectId




# This should be on top of your script
cookies = EncryptedCookieManager(
    # prefix="masterful/streamlit-cookies-manager/",
    password=os.environ.get("COOKIES_PASSWORD", "alwayscheckthesourcecodeyoufool"),
)


# @app.post("/tests/{username}/answers/")
def submit_answer():
    user_answer = st.session_state.answer_selection
    if user_answer is None:
        st.warning('Please select an answer')
        return


    # user_test = requests.get(f'http://localhost:8000/tests/{st.session_state.username}')
    data = {
        "username": st.session_state.username,
        "answers": {
            "1": user_answer
        }
    }

    res = requests.post(f'http://localhost:8000/tests/{st.session_state.username}/answers/', json=data)
    if res.status_code == 200:
        return {'message': 'Answer submitted successfully'}
    else:
        raise requests.HTTPError(f"Failed to submit answer: {res.json()}")


def get_available_tests():
    res = requests.get('http://localhost:8000/tests/')
    if res.status_code == 200:
        if res.content:
            return res.json()
        else:
            return []
    else:
        raise requests.HTTPError(f"Failed to get available tests: {res.json()}")
    # return res.json()


class TestState:
    def __init__(self, username):
        self.username = username
        self.test_started = False
        self.answers = {}



def login_page():
    # st.write(st.session_state)
    if 'test_state' in st.session_state:
        return True

    st.write('# Hello, Learner!')
    username = st.text_input('Username', key='username')
    if username:
        st.session_state.test_state = TestState(username)
        cookies['tester_username'] = username
        cookies.save()
        st.rerun()



def logout():
    # cookies.clear()
    del cookies['tester_username']
    cookies.save()
    st.session_state.clear()
    st.rerun()



def main():
    while not cookies.ready():
        time.sleep(0.01)

    st.write("Current cookies:", cookies)

    if 'tester_username' in cookies:
        st.session_state.username = cookies['tester_username']
    else:
        login_page()
        st.stop()
    
    st.button("logout", on_click=logout)

    if st.session_state.username == "teacher":
        teacher_page()
    else:
        student_page()



def get_all_questions():
    res = requests.get('http://localhost:8000/questions/')
    if res.status_code == 200:
        print(res.json())
        try:
            return res.json()
        except json.JSONDecodeError:
            return []
    else:
        raise requests.HTTPError(f"Failed to get questions: {res.json()}")


def delete_question(question_id):
    # question_id = ObjectId(question_id)
    res = requests.delete(f'http://localhost:8000/questions/{question_id}')
    if res.status_code == 200:
        return {'message': 'Question deleted successfully'}
    else:
        raise requests.HTTPError(f"Failed to delete question: {res.json()}")
    

def teacher_page():
    # st.write("---")

    with st.expander('Create a new question', expanded=False):
        with st.form(key='new_question_form'):
            new_question = st.text_input('Question')
            new_options = []
            for i in range(5):
                option = st.text_input(f'Option {i+1}')
                new_options.append(option)
            new_answer = st.text_input('Answer')

            submit_button = st.form_submit_button('Submit')

            if submit_button:
                question_data = {
                    'question': new_question,
                    'options': new_options,
                    'correct_answer': new_answer,
                    'subject': 'math',
                    'source_document': 'test'
                }
                res = requests.post('http://localhost:8000/questions/', json=question_data)
                if res.status_code == 200:
                    st.write('Question submitted successfully')
                else:
                    st.write('Failed to submit question:', res.json())

    st.write("## All questions (teacher's view)")

    all_questions = get_all_questions()
    for q in all_questions:
        st.write(f"### {q['question']}")
        st.caption(f"id: {q['id']}")
        # st.write(q['options'])
        for i, option in enumerate(q['options']):
            # st.write(f"{i+1}. {option}")
            if q['correct_answer'] == option:
                st.write(f"`{chr(ord('A') + i)}:` :rainbow[{option}]")
            else:
                st.write(f"`{chr(ord('A') + i)}:` {option}")

        # st.write(f"answer: `{q['correct_answer']}`")
        st.write(f"source: {q['source_document']}")
        st.write(f"subject: {q['subject']}")
        st.button(f"Delete question {q['id']}", on_click=delete_question, args=(q['id'],))
        # st.write(q)
        st.write('---')


def student_page():
    # st.set_page_config(page_title='Quiz App', page_icon='🧠')
    st.caption(f"`{st.session_state.username}`")
    st.write(f'# Hello, {st.session_state.username}!')

    st.write('---')

    st.write("## Question 1: What's the capital of France?")
    st.radio('Answer', ['Paris', 'London', 'Berlin'], key="answer_selection")

    if submit := st.button('Submit'):
        response = submit_answer(st.session_state.username, st.session_state.answer_selection)
        st.write(response.json())







if __name__ == '__main__':
    main()
