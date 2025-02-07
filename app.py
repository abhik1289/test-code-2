import streamlit as st
import pandas as pd
import re
import google.generativeai as genai
# import easyocr  # If needed
from PIL import Image
import io
import time
import random
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB connection (REPLACE with your connection string)
client = MongoClient("mongodb+srv://theabhik2020:hoAxx927XbF0Yp3c@cluster0.ko8v5.mongodb.net/pythonTest")
db = client["user_db"]
users = db["users"]

# Set Streamlit page config
st.set_page_config(page_title="Decentralized Fraud Detection System", layout="wide")

# Set up Gemini API key
genai.configure(api_key="AIzaSyDZfMZN51fqIhxjtSkkAM6eMDBvYdcCuvk")  # Replace with your actual key

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_id' not in st.session_state:  # Store user ID
    st.session_state.user_id = None  # Initialize to None
if 'users' not in st.session_state:
    st.session_state.users = {} # this line is not required

# User Registration
def register_user():
    st.subheader("📝 Register")
    username = st.text_input("Enter a username:")
    email = st.text_input("Enter your email:") # Add email input
    password = st.text_input("Enter a password:", type="password")

    if st.button("Register"):
        if users.find_one({'email': email}): # Check if email exists
            st.error("Email already exists. Choose a different one.")
            return

        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': hashed_password
        }

        try:
            result = users.insert_one(user_data)
            st.success("✅ Registration successful! Please log in.")
        except Exception as e:
            st.error(f"An error occurred during registration: {e}")

# User Login
def login_user():
    st.subheader("🔑 Login")
    email = st.text_input("Enter your email:") # Login with email
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        user = users.find_one({'email': email})
        if user and check_password_hash(user['password_hash'], password):
            st.session_state.logged_in = True
            st.session_state.username = user['username']
            st.session_state.user_id = str(user['_id']) # Store the user's ID
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid email or password. Try again.")

# Logout
def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None # Clear user ID
    st.rerun()

# Show login/register page if not logged in
if not st.session_state.logged_in:
    st.sidebar.title("🔐 User Authentication")
    auth_option = st.sidebar.radio("Choose an option:", ["Login", "Register"])
    if auth_option == "Login":
        login_user()
    else:
        register_user()
    st.stop()

#... (rest of your Streamlit code: PAN/GST verification, transactions, etc.)

st.title(f"🚀 Welcome, {st.session_state.username}!")
st.sidebar.button("Logout", on_click=logout_user)

#... (rest of your Streamlit code)