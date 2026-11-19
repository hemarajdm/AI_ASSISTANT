python
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered"
)

# Application Title
st.title("AI Interview Assistant")
st.caption("It is a platform for getting interview preparation information.")

# Groq API Connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Advanced Settings.")
    st.stop()

# Job Role Selection
role = st.selectbox(
    "JOB TITLE",
    [
        "software engineer",
        "senior software engineer",
        "data analyst",
        "prompt engineer",
        "DevOps engineer",
        "other"
    ]
)

if role == "other":
    role = st.text_input("Enter your job title", "XXXXXXX")

# Model Selection
gen_model = st.selectbox(
    "MODEL",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b"
    ]
)

# Difficulty Level
level = st.selectbox(
    "DIFFICULTY LEVEL",
    [
        "beginner",
        "intermediate",
        "advanced"
    ]
)

# Activity Selection
mode = st.radio(
    "ACTIVITY",
    [
        "generate questions",
        "generate code questions",
        "evaluate answer",
        "improve answers"
    ]
)

# Generate Questions
if mode == "generate questions":

    count = st.slider(
        "Number of questions",
        1, 10, 5
    )

# Generate Coding Questions
elif mode == "generate code questions":

    topic = st.selectbox(
        "Topics",
        [
            "SQL",
            "AIML",
            "Python",
            "DSA",
            "C++/C",
            "Java",
            "Cyber Security",
            "ML"
        ]
    )

    count = st.slider(
        "Number of questions",
        1, 10, 5
    )

# Evaluate or Improve Answers
else:

    question = st.text_area(
        "Enter interview question here"
    )

    answer = st.text_area(
        "Enter your answer",
        height=160
    )


# Generate AI Response
if st.button("Generate AI Response", type="primary"):

    # Validate User Input
    if mode in ["evaluate answer", "improve answers"]:

        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid question and answer.")
            st.stop()

    if role == "XXXXXXX" or not role.strip():
        st.warning("Please enter a valid job title.")
        st.stop()

    # Generate Task Based on Activity
    if mode == "generate questions":

        task = (
            "Generate " + str(count) +
            " frequently
