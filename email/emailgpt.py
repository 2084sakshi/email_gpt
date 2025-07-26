import google.generativeai as genai

import streamlit as st
import os

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-pro")

def get_email( src , des, subject, tone, about):
   prompt = "write an email from {} to {} with the subject {} and the tone {} about {}".format(src, des, subject, tone, about)
   response = model.generate_content(prompt)
   return response.text 


#web part
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered", initial_sidebar_state="collapsed")
st.header("Email Generator")
st.subheader("Generate an email with the given details")
st.write("This is a simple web app to generate an email with the given details. You can use this to generate an email for your project, work, or any other purpose.")

col1,col2 = st.columns(2)
with col1:
    src = st.text_input("who is sending the email?")
    subject = st.text_input("Enter the subject of the email")

    
with col2:
    des = st.text_input("who is receiving the email?")
    tone = st.selectbox("Select the tone of the email", ["Formal", "Informal", "Neutral", "Request", "Complaint", "Apology", "Thank You", "Suggestion", "Advice", "Invitation", "Reminder", "Urgent"])

about = st.text_area("What is the email about?")
send = st.button("Generate Email")

if send:
    if src and des and subject and tone and about:
        email = get_email(src, des, subject, tone, about)
        st.write(email)
        print(email)
    else:
        st.error("Please fill in the details and click on the button to generate the email.")

