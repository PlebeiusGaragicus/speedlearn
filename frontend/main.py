import requests

import streamlit as st


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



class TestState:
    def __init__(self, username):
        self.username = username
        self.test_started = False
        self.answers = {}



def init():
    st.write(st.session_state)
    if 'test_state' in st.session_state:
        return True
    
    st.write('# Hello, Learner!')
    st.text_input('Username', key='username')
    # st.chat_input('Username', key='username')
    if st.session_state.username:
        st.session_state.test_state = TestState(st.session_state.username)
        st.rerun()


    return False





def main():
    st.set_page_config(page_title='Quiz App', page_icon='🧠')

    if not init():
        st.stop()

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
