import json
import os
from textblob import TextBlob
from nltk.tokenize import word_tokenize
import nltk
import streamlit as st
import speech_recognition as sr

# Download NLTK tokenizer
nltk.download('punkt')

# JSON file to store knowledge
kb_file = 'knowledge_data.json'

# Default knowledge base with updated ATM and branch locations
default_knowledge = {
    "hello": "Hello! How may I assist you today?",
    "goodbye": "Goodbye! Wishing you a great day ahead!",
    "account types": "We offer Savings, Current, Fixed Deposit, and Business Accounts. Let me know if you need details about any specific type.",
    "loan types": "Available loans include Home, Personal, Auto, and Education Loans. Each loan has different eligibility and terms.",
    "interest rates": "Interest rates vary: Savings accounts (2%-5%), Loans depend on the type and tenure, contact support for exact loan rates.",
    "atm locations": {
        "Colombo": "ATM is located in Colombo 1, Colombo 2, and Colombo 7.",
        "Kandy": "ATM is located at Kandy Town and Peradeniya.",
        "Galle": "ATM is located at Galle Fort and Galle Town.",
        "Jaffna": "ATM is located in Jaffna City and Chunnakam."
    },
    "branch locations": {
        "Colombo": "We have branches in Colombo 1, Colombo 2, and Colombo 7.",
        "Kandy": "We have branches in Kandy Town and Peradeniya.",
        "Galle": "We have branches in Galle Fort and Galle Town.",
        "Jaffna": "We have branches in Jaffna City and Chunnakam."
    },
    "how to apply for a loan": "You can apply online via our website or visit any of our branches for assistance.",
    "banking hours": "Our banking hours are from 9 AM to 4 PM, Monday to Friday.",
    "contact support": "You can call us at 123-456-789 or email support@ourbank.com.",
    "fees": "Fees vary depending on your account type. Please contact customer support for full details.",
    "opening a savings account": "Visit any branch or apply online to open a savings account. A minimum deposit is required.",
    "fixed deposit": "A fixed deposit account earns higher interest. Terms range from 6 months to 5 years."
}


# Load or initialize knowledge base
def load_knowledge():
    if os.path.exists(kb_file):
        with open(kb_file, 'r') as file:
            return json.load(file)
    return default_knowledge

# Save updated knowledge
def save_knowledge(data):
    with open(kb_file, 'w') as file:
        json.dump(data, file, indent=4)

# Match user query
def match_query(user_input, knowledge_base):
    user_input = user_input.lower()
    tokens = word_tokenize(user_input)
    for key in knowledge_base:
        if key in user_input or key in tokens:
            return knowledge_base[key]
    return None

# Learn new fact
def learn_new_fact(user_input, knowledge_base):
    try:
        if ':' in user_input:
            content = user_input.lower().replace('learn', '', 1).strip()
            question, answer = map(str.strip, content.split(':', 1))
            knowledge_base[question] = answer
            save_knowledge(knowledge_base)
            return "Got it! I've saved that information."
        else:
            return "Please use the format: 'learn question: answer'."
    except Exception as e:
        return f"Sorry, I couldn't save that information due to: {e}"

# Get chatbot response
def fetch_response(user_input, knowledge_base):
    user_input = user_input.strip().lower()
    if user_input == "goodbye":
        return "goodbye", "Goodbye! Have a great day."
    if user_input.startswith("learn"):
        return "learn", learn_new_fact(user_input, knowledge_base)
    matched_response = match_query(user_input, knowledge_base)
    if matched_response:
        return "answer", matched_response
    return "unknown", "Sorry, I don't know the answer to that. Try rephrasing or use 'learn question: answer'."

# Voice recognition
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎙 Listening..."):
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand you."
            except sr.RequestError:
                return "Could not connect to the speech recognition service."

# Streamlit UI
st.set_page_config(page_title="Smart Banking Assistant", layout="centered")
st.title("🤖 Smart Banking Assistant")

# Session state
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = load_knowledge()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("🤖", "Hello! Type or speak your question. Use 'learn question: answer' to teach me something new.")]

# Chat display
for sender, msg in st.session_state.chat_history:
    with st.chat_message("assistant" if sender == "🤖" else "user"):
        st.markdown(msg)

# Clear chat
if st.button("🧹 Clear History"):
    st.session_state.chat_history = [("🤖", "Chat history cleared. How can I assist you now?")]
    st.rerun()

# Input columns
text_col, voice_col = st.columns([0.7, 0.3])
user_input = ""

with text_col:
    user_input = st.text_input("Type your message here:", key="text_input")

with voice_col:
    if st.button("🎤 Speak"):
        voice_input = recognize_voice()
        if voice_input:
            st.session_state.chat_history.append(("You", f"🗣️ {voice_input}"))
            intent, response = fetch_response(voice_input, st.session_state.knowledge_base)
            st.session_state.chat_history.append(("🤖", response))
            st.rerun()

# FAQ section (fixed)
st.markdown("### 🔍 Quick FAQs")
faq_items = [
    "account types", "loan types", "interest rates",
    "atm locations", "banking hours", "contact support",
    "fees", "branch locations"
]

faq_clicked = None
faq_cols = st.columns(4)
for idx, item in enumerate(faq_items):
    with faq_cols[idx % 4]:
        if st.button(item.title(), key=f"faq_button_{item}"):
            faq_clicked = item

if faq_clicked:
    st.session_state.chat_history.append(("You", faq_clicked))
    intent, response = fetch_response(faq_clicked, st.session_state.knowledge_base)
    st.session_state.chat_history.append(("🤖", response))
    st.rerun()

# Submit button
if st.button("➖ Enter"):
    if user_input.strip() != "":
        st.session_state.chat_history.append(("You", user_input))
        intent, response = fetch_response(user_input, st.session_state.knowledge_base)
        st.session_state.chat_history.append(("🤖", response))
        if intent == "goodbye":
            st.info("Session ended. Please refresh to start a new chat.")
        st.rerun()
