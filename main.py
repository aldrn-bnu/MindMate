import streamlit as st
import speech_recognition as sr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

# Prompt for mental health assistant
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a kind, supportive mental health assistant. and if you cant understand what is being said,just say that you dont understand and dont try to calm the user
Respond empathetically and calmly. Suggest simple self-care actions and other exercises try not to be too repetitive
Keep replies short (~30 words). Avoid assuming distress from casual greetings.
some self care suggestions,"Try deep breathing exercises before your meeting. Practicing mindfulness or grounding techniques like the 5-4-3-2-1 method can also help reduce anxiety symptoms.
Maintain a consistent sleep schedule and avoid screen time an hour before bed. Consider writing a 'worry list' before sleeping to help clear your mind.
Break tasks into very small steps and reward yourself for each one. Also, ensure you're getting proper nutrition and hydration to support energy levels.
Schedule 10 minutes of quiet time daily for yourself. Breathing techniques or progressive muscle relaxation can reduce tension significantly.
Try writing about your feelings each morning. Mindful stretching or yoga can help calm the body and reduce physical symptoms of anxiety.
Make time for small enjoyable activities daily, even if they don’t feel fun right now. Talking to someone about your feelings can also help.
Reach out to one person you trust and have a short chat. Even brief human connection can help reduce feelings of isolation.
Use the Pomodoro technique—work in 25-minute focused sessions followed by short breaks. Also, keep your work environment distraction-free.
Next time you feel the urge to eat, try journaling what you're feeling. Substitute emotional eating with a short walk or calming activity.
Write down three small things you did well today. Practicing self-compassion and limiting comparisons with others is key.
Challenge negative thoughts with positive self-talk. Consider gradual exposure to social settings that feel safe.
Try practicing daily diaphragmatic breathing and limit caffeine intake. Talking to a professional can also provide long-term support.
Make a small list of avoided tasks and tackle one at a time with short breaks in between. Reward yourself for each completed item.
Create a simple morning routine with small wins. Try writing one thing you’re looking forward to, even if it’s minor.
Set a 10-minute timer for ‘worry time’, then consciously shift to an engaging activity. Use cognitive reframing to view situations more realistically.
Focus on one small decision you can make today. Regaining control over small choices helps build confidence.
Track your mood daily using a journal or app. Ensure you're getting enough sleep and reducing sugar/caffeine intake.
Remind yourself that rest is productive too. Schedule short breaks as part of your workday and treat them as essential.
Try a 1-hour digital detox daily. Replace screen time with an offline activity like reading or walking.
Write a list of your recent accomplishments, no matter how small. Talk to a mentor or trusted friend for perspective.
" generate suggestions similiar to these according to the users prompts
try to detect "Performance Anxiety
Sleep Disturbance / Insomnia
Burnout
Chronic Stress
Somatic Symptoms of Anxiety
Early Signs of Depression
Social Isolation
Attention Difficulties / Mental Fatigue
Emotional Eating
Low Self-Esteem
Social Anxiety
Generalized Anxiety
Avoidant Coping
Depressive Symptoms
Rumination / Overthinking
Loss of Agency / Helplessness
Mood Swings
Workaholism / Perfectionism
Digital Addiction / Anxiety
Imposter Syndrome
"
If suggesting breathing: say "Inhale...", count, then "Hold...", then "Exhale..."."""),
    ("user", "{input}")
])
chain: Runnable = prompt | llm

# 🎤 Voice recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="en-in")
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech recognition failed."

# 🤖 Get AI response + voice reply
def get_response(user_input):
    from win32com.client import Dispatch  
    speaker = Dispatch("SAPI.SpVoice")    

    response = chain.invoke({"input": user_input})
    content = response.content.strip()
    speaker.Speak(content)

    issue = "Wellness"
    suggestion = "Take 3 deep breaths."
    lowered = user_input.lower()

    if any(w in lowered for w in ["sad", "anxious", "angry", "tired"]):
        issue = "Emotional distress"
    elif any(w in lowered for w in ["happy", "relaxed", "peaceful"]):
        issue = "Positive mood"

    if "anxious" in lowered:
        suggestion = "Try the 4-7-8 breathing technique."
    elif "tired" in lowered:
        suggestion = "Take a short walk and hydrate."

    return content, issue, suggestion

# 🧠 Streamlit UI setup
st.set_page_config(page_title="MindMate Chat", layout="wide")
st.title("💬 MindMate - Chat with a Caring AI")

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "issue" not in st.session_state:
    st.session_state.issue = ""
if "suggestion" not in st.session_state:
    st.session_state.suggestion = ""

# Layout: chat and sidebar
col1, col2 = st.columns([3, 1])

with col1:
    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.messages:
            role, text = msg["role"], msg["text"]
            if role == "user":
                st.chat_message("🧍 You").markdown(text)
            else:
                st.chat_message("🤖 MindMate").markdown(text)

    # Input section at bottom
    col_input, col_mic = st.columns([4, 1])
    with col_input:
        user_input = st.text_input("Type a message...", key="chat_input")
        if st.button("Send") and user_input.strip():
            st.session_state.messages.append({"role": "user", "text": user_input})
            reply, issue, suggestion = get_response(user_input)
            st.session_state.messages.append({"role": "bot", "text": reply})
            st.session_state.issue = issue
            st.session_state.suggestion = suggestion
            st.rerun()

    with col_mic:
        if st.button("🎙️ Speak"):
            voice_input = recognize_speech()
            st.session_state.messages.append({"role": "user", "text": voice_input})
            reply, issue, suggestion = get_response(voice_input)
            st.session_state.messages.append({"role": "bot", "text": reply})
            st.session_state.issue = issue
            st.session_state.suggestion = suggestion
            st.rerun()

with col2:
    st.subheader("🧠 Detected Emotion")
    st.info(st.session_state.issue)

    st.subheader("🌿 Self-Care Suggestion")
    st.success(st.session_state.suggestion)

st.markdown("---")
st.caption("Made with ❤️ using LLaMA3 + Groq + Streamlit")
