📄 README.md

# 💬 MindMate – AI Mental Health Assistant

MindMate is a Streamlit-based mental health chatbot powered by Groq's LLaMA3 model. It listens to your voice or typed input and provides supportive, empathetic responses with personalized self-care suggestions.

---

## 🧠 Features

- 🎤 Voice input using your microphone
- 🤖 Responses generated using `LLaMA3-70B` via Groq API
- 🌱 Detects emotional tone and suggests self-care techniques
- 🧘 Includes mindfulness and breathing exercises
- 🔈 Speaks responses aloud using Windows speech synthesis

---

## 📸 UI Overview

- **Left panel**: Chat interface with voice and text input
- **Right panel**: Detected emotion + self-care suggestion
- Friendly, concise mental health support

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/mindmate-chatbot.git
cd mindmate-chatbot
2. Set Up Virtual Environment (Optional but Recommended)

python -m venv env
source env/bin/activate  # macOS/Linux
.\env\Scripts\activate   # Windows
3. Install Requirements

pip install -r requirements.txt
4. Set Environment Variables
Create a .env file in the root directory:

env

GROQ_API_KEY=your_groq_api_key_here
🧪 Run the App
bash
streamlit run main.py

⚙️ Tech Stack
Streamlit

Groq + Langchain

LLaMA3

SpeechRecognition

Python-dotenv

Windows TTS via pywin32

📝 Notes
Designed to avoid giving medical advice; it only provides light self-care suggestions.

Best run on Windows (due to text-to-speech via SAPI).

For voice input to work, ensure your microphone permissions are granted.

❤️ Credits
Built by me and my team[ALDRIN BINU,NAMITHA ANNA KOSHY,ALEX TITTO ZACHARIAS,HARISH PRASAD] using OpenAI ChatGPT, LangChain, Groq, and Streamlit.

