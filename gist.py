#gist.py
import os
import pyperclip
import streamlit as st
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class Summary(object):
    def __init__(self, title="AI Summarizer"):
        self.title = title

    @staticmethod
    def model():
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        return ChatGoogleGenerativeAI(model="gemini-pro")

    @staticmethod
    def getLLamaresponse(llm, input_text, tone, lang, gist_style, no_words, info=''):
        template = """
            Write a {tone} summary in {lang} as {gist_style} within {no_words} words.
            Text: {input_text} 
            {info}
                """.format(tone=tone, lang=lang, gist_style=gist_style, input_text=input_text,
                                        no_words=no_words, info=info)
        response = llm.invoke(template)
        return response.content
        # return formated_prompt

    @staticmethod
    def copy_text(answer, copy_button=False):
        pyperclip.copy(answer)
        if copy_button:
            st.toast("Text copied to clipboard!", icon="📋")

    @staticmethod
    def record_audio():
        r = sr.Recognizer()
        with st.spinner("Recording..."):
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                with st.spinner("Say Something..."):
                    audio = r.listen(source, timeout=5)
            with st.spinner("Processing..."):
                try:
                    text = r.recognize_google(audio)
                    st.session_state['input_text'] = text
                    return text
                except sr.UnknownValueError:
                    st.write("Sorry, I could not understand what you said. Please try again or write in text box.")
                    return ""
                except sr.RequestError as e:
                    st.write(f"Could not request results; {e}")
                    return ""

    @staticmethod
    def input_state(input_text):
        if isinstance(input_text, str):
            st.session_state['input_text'] = input_text

    

def run_gist(doc=''):
    load_dotenv()
    gist = Summary()

    st.header(gist.title + " 🤖", divider='rainbow')

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    button_disabled = False

    if button_disabled:
        st.toast("Mic Button is disabled in production. HF Don't have Audio Device")

    col1, col2 = st.columns([20, 3])

    with col1:
        text = st.empty()
        input_text = text.text_area("Enter Text")

    with col2:
        recorder = st.button("🎙️", help="Text by Voice", key="mic", disabled=button_disabled)

    if recorder:
        recorded_text = gist.record_audio()
        if recorded_text:
            input_text = text.text_area("Enter Text", value=recorded_text)
    
    if doc:
        input_text = text.text_area("Enter Text", value=doc)

    with st.sidebar:
        st.title(' :blue[_AI Generated Summary_] 🤖')
        st.subheader('Parameters')
        no_words = st.sidebar.slider('Maximum Characters', min_value=100, max_value=5000, value=1000, step=100)
        gist_style = st.selectbox('Writing the Summary for', ('Researchers', 'Data Scientist', 'Common People'), index=0)
        tone = st.selectbox('Desired Tone', ('Informative', 'Casual', 'Persuasive', 'Formal', 'Humorous'), index=0)
        lang = st.text_input('Language', 'English')
        info = st.text_area('Specific Instruction')
        with st.spinner("Loading Model..."):
            llm = gist.model()

    submit = st.button("Generate Summary", on_click=lambda: gist.input_state(input_text))
    print("Session: ", st.session_state)
    if submit:
        with st.spinner("Generating Summary..."):
            answer = gist.getLLamaresponse(llm, st.session_state['input_text'], tone, lang, gist_style, no_words, info)
            st.success('Summary Generated!', icon="✅")
            st.write(answer)
            st.markdown(''':orange[Run in your system to access Copy to Clipboard Feature]''')

if __name__ == "__main__":
    run_gist()