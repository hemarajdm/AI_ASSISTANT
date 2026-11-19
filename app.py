import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered"
)

st.title("AI Interview Assistant")
st.caption("A platform for preparing for technical and HR interviews.")

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Streamlit secrets.")
    st.stop()

# Job role selection
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
    custom_role = st.text_input("Enter your job title", "XXXXXXX")
    if custom_role.strip():
        role = custom_role

# Model selection
gen_model = st.selectbox(
    "MODEL",
    ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]
)

# Difficulty selection
level = st.selectbox(
    "DIFFICULTY LEVEL",
    ["beginner", "intermediate", "advanced"]
)

# Activity selection
mode = st.radio(
    "Activity",
    [
        "generate questions",
        "generate code questions",
        "evaluate answer",
        "improve answers"
    ]
)

# Input fields based on selected activity
if mode == "generate questions":
    count = st.slider("Number of questions", 1, 10, 5)

elif mode == "generate code questions":
    topic = st.selectbox(
        "Topics",
        [
            "SQL",
            "AI/ML",
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

    
    if mode in ["evaluate answer", "improve answers"]:
        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid question and answer.")
            st.stop()

  
    background = (
        f"Job role: {role}\n"
        f"Difficulty level: {level}\n"
    )

    
    if mode == "generate questions":

        task = (
            f"Generate {count} frequently asked interview questions. "
            "Include 3 theoretical and 2 conceptual questions where possible. "
            "Do not provide answers. Give hints for each question."
        )

    elif mode == "generate code questions":

        task = (
            f"Generate {count} frequently asked coding interview questions "
            f"on {topic}. Questions should be appropriate for the selected "
            "job role and difficulty level."
        )

    elif mode == "evaluate answer":

        task = (
            f"Interview question: {question}\n"
            f"My answer: {answer}\n\n"
            "Evaluate this answer based on the following criteria:\n"
            "1. Conceptual understanding\n"
            "2. Relevance\n"
            "3. Communication\n"
            "4. Length of answer\n\n"
            "Give each criterion a rating out of 5. "
            "Provide an overall score and suggestions for improvement."
        )

    elif mode == "improve answers":

        task = (
            f"Interview question: {question}\n"
            f"My answer: {answer}\n\n"
            "Improve my answer based on word choice, clarity, and "
            "important keywords to include. "
            "Do not invent anything about the candidate. "
            "Keep the answer natural and professional."
        )

    
    with st.spinner("Generating your answer..."):

        try:
            response = client.chat.completions.create(
                model=gen_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Act as a senior interviewer with expertise "
                            "in both HR and technical interviews. "
                            "Provide accurate, clear, and helpful responses."
                        )
                    },
                    {
                        "role": "user",
                        "content": background + task
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            
            st.subheader("AI Interview Assistant Response")

            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")
