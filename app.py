import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered"
)import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Interview Assistant", page_icon='🫡', layout='centered')

st.title("AI Interview Asssitant")
st.caption("It is a platform for getting information")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Advanced settings")
    st.stop()

role = st.selectbox("JOB TITLE", [
    'software engineer',
    'senior software engineer',
    'data analyst',
    'prompt engineer',
    'Devops engineer',
    'other'
])

if role == "other":
    st.text_input("Enter your job title", "XXXXXXX")

gen_model = st.selectbox("model", [
    'openai/gpt-oss-20b',
    'openai/gpt-oss-120b'
])

role = st.selectbox("difficult level", [
    'bigginner',
    'intermidiate',
    'advance'
])

mode = st.radio('Activity', [
    'generate questions',
    'generate code questions',
    'evaluate answer',
    'improve answers'
])

if mode == 'generate questions':
    count = st.slider("Number of questions", 1, 10, 5)

elif mode == 'generate code questions':
    topic = st.selectbox('Topics', [
        'SQL', 'AIML', 'Python', 'DSA',
        'c++/c', 'Java', 'cyber security', 'ML'
    ])
    count = st.slider("Number of question", 1, 10, 5)

else:
    question = st.text_area('Enter interview question here')
    answer = st.text_area('enter your answer', height=160)

if st.button("Generate AI Response", type="primary"):

    if mode in ['evaluate answer', 'improve answers'] and (not question.strip() or not answer.strip()):
        st.warning("please enter valid question and answer")
        st.stop()

    topics = "Topics is " + (topic if mode == 'generate code questions' else "") + " difficulty is " + role

    if mode == "generate questions":
        task = "generate " + str(count) + " Frequently asked Interview questions 3 theory and 2 conceptual. do not give answers. give hints"

    elif mode == "generate code questions":
        task = "generate " + str(count) + " Frequently asked coding questions on " + topic + " anything can be related to topic"

    elif mode == "evaluate answer":
        task = "question :" + question + " MY Answer : " + answer + " Evaluate this answer based on concept, relevance, communication, length of answer. give each rating out of 5 in a list."

    elif mode == "improve answers":
        task = "question :" + question + " MY Answer : " + answer + " improve the answer based on choice of words and keywords to include. do not invent anything about candidate"

    background = "job role :" + role + " difficulty level " + role

    with st.spinner("generating your answer ...."):
        try:
            response = client.chat.completions.create(
                model=gen_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Act as a senior interviewer, both HR and technical expert"
                    },
                    {
                        "role": "user",
                        "content": background + task
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")

st.title("AI Interview Assistant")
st.caption("It is a platform for getting information.")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Advanced Settings.")
    st.stop()

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

gen_model = st.selectbox(
    "Model",
    ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]
)

level = st.selectbox(
    "Difficulty Level",
    ["beginner", "intermediate", "advanced"]
)

mode = st.radio(
    "Activity",
    [
        "generate questions",
        "generate code questions",
        "evaluate answer",
        "improve answers"
    ]
)

if mode == "generate questions":
    count = st.slider("Number of questions", 1, 10, 5)

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
    count = st.slider("Number of questions", 1, 10, 5)

else:
    question = st.text_area("Enter interview question here")
    answer = st.text_area("Enter your answer", height=160)


if st.button("Generate AI Response", type="primary"):

    if mode in ["evaluate answer", "improve answers"] and (
        not question.strip() or not answer.strip()
    ):
        st.warning("Please enter a valid question and answer.")
        st.stop()

    if mode == "generate questions":
        task = (
            "Generate " + str(count) +
            " frequently asked interview questions. "
            "Include 3 theory and 2 conceptual questions. "
            "Do not give answers. Give hints."
        )

    elif mode == "generate code questions":
        task = (
            "Generate " + str(count) +
            " frequently asked coding questions on " + topic +
            ". Anything can be related to this topic."
        )

    elif mode == "evaluate answer":
        task = (
            "Question: " + question +
            "\nMy Answer: " + answer +
            "\nEvaluate this answer based on concept, relevance, "
            "communication, and length of answer. "
            "Give each rating out of 5 in a list."
        )

    elif mode == "improve answers":
        task = (
            "Question: " + question +
            "\nMy Answer: " + answer +
            "\nImprove the answer based on choice of words "
            "and keywords to include. "
            "Do not invent anything about the candidate."
        )

    background = (
        "Job role: " + role +
        "\nDifficulty level: " + level
    )

    with st.spinner("Generating your answer..."):

        try:
            response = client.chat.completions.create(
                model=gen_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Act as a senior interviewer, both HR and technical expert."
                    },
                    {
                        "role": "user",
                        "content": background + "\n" + task
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            output = response.choices[0].message.content

            st.subheader("AI Response")
            st.markdown(output)

            st.download_button(
                "Download response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API connection was unsuccessful: {e}")
            st.info("Please check your API key and rate limits.")

st.caption("Powered by Streamlit and GitHub using LLM API.")
