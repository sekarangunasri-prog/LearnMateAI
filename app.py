import streamlit as st
st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🎓",
    layout="wide"
)
with st.sidebar:
    st.title("📚 LearnMate AI")
    st.write("Your Personal AI Tutor")
    st.divider()
    st.info("Choose a topic and your learning style.")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(page_title="LearnMate AI", page_icon="🎓")

st.title("🎓 LearnMate AI")
st.write("Learn the way you understand!")

topic = st.text_input("Enter a topic")

style = st.selectbox(
    "Choose Learning Style",
    ["Simple", "Step-by-step", "With Examples", "Exam Summary"]
)

if st.button("Explain"):
    if topic:
        prompt = f"Explain '{topic}' in {style} style using simple English."

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a topic.")
