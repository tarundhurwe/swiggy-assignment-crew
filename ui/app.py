import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.title("AI Evaluation Pipeline")

st.header("Upload Conversation")

input_json = st.text_area("Paste JSON here")

if st.button("Submit"):
    data = json.loads(input_json)
    res = requests.post(f"{API_URL}/ingest", json=data)
    st.write(res.json())

st.header("Get Results")

conv_id = st.text_input("Conversation ID")

if st.button("Fetch Results"):
    res = requests.get(f"{API_URL}/results/{conv_id}")
    st.json(res.json())

st.header("Suggestions")

if st.button("Load Suggestions"):
    res = requests.get(f"{API_URL}/suggestions")
    st.json(res.json())
