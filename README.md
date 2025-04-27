# smart-banking-assistant

Welcome to the **Smart Banking Assistant** project!  
This is a simple yet smart banking chatbot developed with **Python** and **Streamlit**, supporting **text**, **voice recognition**, **learning new facts**, and providing instant answers to banking-related questions.

---

## ✨ Features
- 💬 **Text-based chatting** interface.
- 🎤 **Voice recognition** support (using SpeechRecognition library).
- 🧠 **Self-learning capability** – Teach the bot new questions and answers.
- 📚 **Knowledge persistence** via local JSON file storage.
- 🏦 **Quick FAQs** about account types, loan details, ATM and branch locations, and more.
- 🧹 **Clear chat history** option.
- ⚡ Built with **Streamlit** for an easy-to-use web UI.

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DehemiManchanayaka/smart-banking-assistant.git
   cd smart-banking-assistant
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
import nltk
nltk.download('punkt')
streamlit run app.py
