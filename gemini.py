import streamlit as st
import dotenv
import google.generativeai as genai
import os

dotenv.load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_res(input: str, history):
    prompt = f"""You are a AI assistant. Here is the conversation so far: \n\n
    {"".join(f"{role}: {text}" for role, text in history)} \n\n
    Now here the user's new query {input} \n\n
    Please provide a comprehensive and informative response"""
    # print(prompt)
    response = chat.send_message(prompt, stream=False)
    # res_filter = response.candidates[0].content.parts
    # res_text = " ".join(part.text for part in res_filter)
    return response

st.set_page_config(page_title="Gemini App")
st.header("StreamLit application")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    
input = st.text_input("Input: ", key="input")
submit = st.button("Ask a question")

if submit and input:
    resp = get_gemini_res(input, st.session_state["chat_history"])
    st.session_state["chat_history"].append(("You", input))
    for chunk in resp:
        st.session_state["chat_history"].append(("Bot", chunk.text))
    
st.subheader("The Chat History")

for role, text in st.session_state["chat_history"]:
    st.write("!!!" + role + ": !!!")
    st.write(text)