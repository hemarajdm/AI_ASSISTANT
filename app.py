import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    layout="centered"
)

st.title("🤖 AI Interview")
st.caption("Practice and Prepare for Your Placement")

# Groq API Configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")

# Job Role
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "Data Analyst",
        "Cyber Security Engineer",
        "Software Developer",
        "Others"
    ]
)

if role == "Others":
    role = st.text_input("Enter your Job Title")

# Model Selection
model = st.selectbox(
    "Choose Your Model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)

# Difficulty Level
level = st.selectbox(
    "Choose Your Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Activity Selection
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Activity Inputs
if mode == "Generate Questions":

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"]
    )

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

else:

    question = st.text_area(
        "Enter Interview Question Here"
    )

    answer = st.text_area(
        "Enter Your Answer",
        height=160
    )

# Generate AI Response
if st.button("Generate AI Response", type="primary"):

    if not role.strip():
        st.warning("Please enter a valid job title.")
        st.stop()

    if mode in ["Evaluate Answers", "Improve Answers"]:

        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid Question and Answer.")
            st.stop()

    # Prompt Creation
    if mode == "Generate Questions":

        task = f"""
        Generate {count} frequently asked interview questions
        for the role of {role}.

        Difficulty Level: {level}

        Include:
        - Theory-based questions
        - Practical questions
        - Situation-based questions

        Provide clear and structured questions.
        """

    elif mode == "Generate Code Questions":

        task = f"""
        Generate {count} frequently asked coding and technical
        interview questions.

        Job Role: {role}
        Topic: {topic}
        Difficulty: {level}

        Include:
        - Coding questions
        - Hints for solving each question
        - Expected time complexity
        - Expected space complexity
        """

    elif mode == "Evaluate Answers":

        task = f"""
        Evaluate the following interview answer.

        Job Role: {role}
        Difficulty: {level}

        Interview Question:
        {question}

        Candidate Answer:
        {answer}

        Evaluate based on:
        1. Technical correctness
        2. Clarity
        3. Completeness
        4. Communication skills

        Identify drawbacks and provide a score out of 10.
        Suggest improvements.
        """

    elif mode == "Improve Answers":

        task = f"""
        Improve the following interview answer.

        Job Role: {role}
        Difficulty: {level}

        Interview Question:
        {question}

        Candidate import streamlit as st
from groq import Groq
st.set_page_config(page_title = "AI Interview Assistant", page_icon = '🫡', layout= 'centered')
st.title("AI Interview Asssitant ")
st.caption(" it is a platform for getting information")
try:
  client = Groq(api_key = st.secrets["GROQ_API_KEY"])
except (KeyError, FileNorFound):
                st.error("API Key is missing . Add it in Advance setting")
                st.stop()
role = st.selectbox("JOB TITLE", ['software engineer','senior software engineer', 'data analyst','prompt engineer', 'Devops engineer', 'other'])
if role == "other":
  st.text_input("Enter your job title ","XXXXXXX")
gen_model = st.selectbox("model", ['openai/gpt-oss-20b', 'openai/gpt-oss-120b'])
role = st.selectbox("difficult level", ['bigginer','intermidiate','advance'])
mode = st.radio('Activity', ['generate questions', 'generate code questions', 'evaluate answer','improve answers'])
if mode == 'generate questions':
  count = st.slider(1,10,5)
elif mode == 'generate code questions':
  topic = st.selectbox('Topics', ['SQL','AIML','Python','DSA','c++/c','Java','cyber security','ML'])
  count = st.slider("Number od question",1,10,5)
else:
  question = st.text_area('Enter interview question here ')
  answer = st.text_area('enter your answer ', height = 160)

if st.button("Generate AI Response", type = "primary"):
  if mode in ['Evaluate Answers', 'Imporve Answer'] and (not question.strip()) or (not answer.strip()):
    st.warning("please enter valid question and answer")
    st.stop()
  topics = "Topics is " + topic + "difficlty is " + level 
  if mode == "generate questions":
    task = "generate" + str(count) + "Frequenrtly asked Interview question 3 theory and 2 conceptual. do not give answers. give hints"
  elif mode == "generate code questions":
    task = "generate" + str(count) + "Frequenrtly askedcodeing question on " + topic + " anything can be related to topic "
  elif mode == "evaluate answer":
    task = "question :" + question + "MY Answer : " + answer + "Evalute this answer based on concept, relevence , communication, length of answe. give each rating out of 5 in a list. "
   elif mode == "improve answers":
     task = "question :" + question + "MY Answer : " + answer + "imporve the answern based oon choice on words key words to include. do not invent anything about candidate " 
   background = "job role :" + role + "difficult levet " + level
   with st.spinner(" generating your answer .... "):
     try:
       response = client.chat.completions.create(
         model = gen_model,
         messages = [{"role":"system","content":"Act as a senoir interviewer , both HR and technicall expert"},
                     {"role" : "user",
                     "content" : backgroound + task }],
         temprature = 0.7,
         max_tokens = 2000Answer:
        {answer}

        Provide:
        1. An improved professional answer
        2. Important points to remember
        3. Technical keywords
        4. Suggestions for improvement
        """

    # Groq API Call
    try:

        with st.spinner("AI is generating your response..."):

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are an experienced technical interviewer
                        and career mentor.

                        Provide accurate, clear, structured,
                        and beginner-friendly responses.
                        """
                    },
                    {
                        "role": "user",
                        "content": task
                    }
                ],
                temperature=0.7,
                max_completion_tokens=3000
            )

            result = response.choices[0].message.content

        # Display Result
        st.subheader("🎯 AI Interview Result")

        st.markdown(result)

    except Exception as e:

        st.error(f"Something went wrong: {e}")
