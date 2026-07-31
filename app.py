import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🎓",
    layout="wide"
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = []
if "doubts" not in st.session_state:
    st.session_state.doubts = 0
with st.sidebar:
    st.title("📚 LearnMate AI")
    st.write("Your Personal AI Tutor")
    st.divider()
    menu = st.radio(
        "Choose Feature",
        [
            "📖 Learn",
            "❓ Doubt Mode",
            "📅 Study Planner",
            "📈 Progress Tracking",
            "🕒 Session History"
        ]
    )
if menu == "📖 Learn":
    st.title("🎓 LearnMate AI")
    st.write("Learn the way you understand!")
    topic = st.text_input("Enter a topic")
    style = st.selectbox(
        "Choose Learning Style",
        [
            "Simple",
            "Step-by-step",
            "With Examples",
            "Exam Summary"
        ]
    )
    if st.button("Explain"):
        if topic:
            prompt = f"Explain '{topic}' in {style} style using simple English."
            try:
                with st.spinner("Generating explanation..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b:free",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                st.session_state.answer = response.choices[0].message.content
                if topic not in st.session_state.history:
                    st.session_state.history.append(topic)
            except Exception as e:
                st.error(e)
        else:
            st.warning("Please enter a topic.")
    if st.session_state.answer:
        st.success("✅ Explanation Generated!")
        st.markdown(st.session_state.answer)
        st.divider()
        quiz_level = st.selectbox(
            "Choose Quiz Difficulty",
            ["Basic", "Intermediate", "Advanced"]
        )
        if st.button("Generate Quiz"):
            quiz_prompt = f"""
Create exactly 5 {quiz_level} level multiple choice questions on '{topic}'.
Rules:
- Exactly 5 questions
- 4 options (A, B, C, D)
- Give answer key at the end
"""
            try:
                with st.spinner("Generating Quiz..."):
                    quiz = client.chat.completions.create(
                        model="openai/gpt-oss-20b:free",
                        messages=[
                            {"role": "user", "content": quiz_prompt}
                        ]
                    )
                st.success("🎉 Quiz Ready!")
                st.markdown(
                    quiz.choices[0].message.content
                )
                st.session_state.quiz_scores.append(5)
            except Exception as e:
                st.error(e)
elif menu == "❓ Doubt Mode":
    st.title("❓ Doubt Mode")
    doubt = st.text_area("Ask your doubt")
    if st.button("Solve Doubt"):
        if doubt:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b:free",
                    messages=[
                        {"role": "user", "content": doubt}
                    ]
                )
            st.session_state.doubts += 1
            st.markdown(
                response.choices[0].message.content
            )
        else:
            st.warning("Please enter your doubt.")
elif menu == "📅 Study Planner":
    st.title("📅 Smart Study Planner")
    goal = st.text_input("What do you want to learn?")
    level = st.selectbox(
        "Current Level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    days = st.number_input(
        "Days Left",
        min_value=1,
        max_value=365,
        value=30
    )
    hours = st.number_input(
        "Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=2
    )
    if st.button("Generate Study Plan"):
        prompt = f"""
Create a personalized study plan.
Goal: {goal}
Current Level: {level}
Days Left: {days}
Study Hours Per Day: {hours}
Generate a simple day-wise study schedule.
"""
        with st.spinner("Creating your study plan..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[
                    {"role":"user","content":prompt}
                ]
            )
        st.markdown(response.choices[0].message.content)
elif menu == "📈 Progress Tracking":
    st.title("📈 Your Progress")
    topics = len(st.session_state.history)
    quizzes = len(st.session_state.quiz_scores)
    doubts = st.session_state.doubts
    st.metric("📚 Topics Learned", topics)
    st.metric("📝 Quizzes Taken", quizzes)
    st.metric("❓ Doubts Solved", doubts)
    progress = min((topics * 10) + (quizzes * 5), 100)
    st.progress(progress / 100)
    st.write(f"Overall Progress: **{progress}%**")
elif menu == "🕒 Session History":
    st.title("🕒 Session History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history, 1):
            st.write(f"{i}. {item}")
    else:
        st.info("No topics studied yet.")
