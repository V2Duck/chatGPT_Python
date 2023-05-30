import openai
import streamlit as st
import logging
from collections import defaultdict
from typing import Dict, List

# Define a class to store session state
class SessionState:
    def __init__(self):
        self.history: List[str] = []
        self.results: Dict[str, str] = {}

# Load OpenAI API key
@st.cache_data(show_spinner=False)
def load_api_key():
    return "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"

# Get response from OpenAI API
@st.cache_data(show_spinner=False)
def get_response(question: str, language: str, model: str) -> str:
    try:
        openai.api_key = load_api_key() #API KEY
        response = openai.Completion.create(
            model=model,
            prompt=f"""{question} {language}""",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Get suggestions for input question
@st.cache_data(show_spinner=False)
def get_suggestions(history: List[str], results: Dict[str, str]) -> List[str]:
    counter = defaultdict(int)
    for item in history:
        if item in results:
            counter[results[item]] += 1
    suggestions = [k for k, v in counter.items() if v >= 2]
    return suggestions

# Main function
def main():
    state = SessionState()

    view = """
    Chào mừng tất cả các bạn đã ghé thăm website, hãy đặt câu hỏi....
    """

    st.markdown("<h1 style='text-align: center;'>Coding With Duck</h1>", unsafe_allow_html=True)
    st.markdown("---")

    with st.sidebar:
        st.image("duck.png")
        st.title("V- Duck Knight")
        st.caption(f'''{view}''', unsafe_allow_html=False)
        model = st.selectbox("Select a GPT model", ["text-davinci-002", "text-davinci-003", "text-curie-001"])

    language = st.selectbox("Choose a programming language:", ("Python", "C++", "Java", "Pascal"))
    question = st.text_input("Enter your question below", key="question")
    suggestions = get_suggestions(state.history, state.results)

    if len(suggestions) > 0:
        suggestion = st.selectbox("Or choose from popular questions:", suggestions)
        if suggestion:
            question = suggestion

    button = st.button("Send")

    if question and button:
        with st.spinner("Please wait..."):
            reply = get_response(question, language, model)
            if reply:
                state.history.append(question)
                state.results[question] = reply
                st.write("Here's your code:")
                st.markdown("\n")
                st.code(reply)
    elif st.button("Clear"):
        question = ""

    if len(state.history) > 0:
        st.markdown("---")
        st.write("Search history:")
        for item in state.history:
            st.write(f"- {item}")

logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    main()
