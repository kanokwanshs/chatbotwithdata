import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set page config
st.set_page_config(page_title="My Chatbot and Data Analysis App", layout="centered")

# Title and subtitle
sst.title("🧠 AI-Powered Chatbot & Data Analysis App 🖥️")
st.subheader("Upload your CSV and get AI insights!")

# Input Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize Gemini model
model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key configured successfully.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "data_dict" not in st.session_state:
    st.session_state.data_dict = None

# Section 1: Upload Main Dataset
st.markdown("### 📂 Section 1: Upload Main Dataset (CSV)")
uploaded_file = st.file_uploader("Choose your main data CSV file", type=["csv"], key="main_dataset")

# Section 2: Upload Data Dictionary (Optional)
st.markdown("### 📖 Section 2: Upload Data Dictionary (Optional)")
uploaded_dict_file = st.file_uploader("Upload a data dictionary CSV (optional)", type=["csv"], key="data_dict")

# Checkbox to trigger analysis
analyze_data_checkbox = st.checkbox("📊 Analyze CSV with AI")

# Read the uploaded files
if uploaded_file:
    try:
        st.session_state.uploaded_data = pd.read_csv(uploaded_file)
        st.success("Main dataset successfully uploaded.")
        st.write("#### Preview of Dataset")
        st.dataframe(st.session_state.uploaded_data.head())
    except Exception as e:
        st.error(f"Error loading main dataset: {e}")

if uploaded_dict_file:
    try:
        st.session_state.data_dict = pd.read_csv(uploaded_dict_file)
        st.success("Data dictionary uploaded.")
        st.write("#### Data Dictionary Preview")
        st.dataframe(st.session_state.data_dict.head())
    except Exception as e:
        st.error(f"Error loading data dictionary: {e}")

# Display chat history
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Chat input
if user_input := st.chat_input("Type your question here..."):
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    if not model:
        bot_response = "Please configure the Gemini API Key to start chatting."
    elif st.session_state.uploaded_data is None:
        bot_response = "Please upload a CSV file first, then ask me to analyze it."
    elif analyze_data_checkbox and ("analyze" in user_input.lower() or "insight" in user_input.lower()):
        try:
            data_summary = st.session_state.uploaded_data.describe().to_string()
            prompt = f"Analyze the following dataset and provide insights:\n\n{data_summary}"
            response = model.generate_content(prompt)
            bot_response = response.text
        except Exception as e:
            bot_response = f"Error during data analysis: {e}"
    else:
        try:
            response = model.generate_content(user_input)
            bot_response = response.text
        except Exception as e:
            bot_response = f"Error generating response: {e}"

    # Display bot response
    st.session_state.chat_history.append(("assistant", bot_response))
    st.chat_message("assistant").markdown(bot_response)
