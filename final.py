import streamlit as st
import requests
from textblob import TextBlob
from urllib.parse import urlparse, parse_qs
import base64

# Function to decode the URL parameter and extract the complaint ID
def extract_complaint_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    encoded_param = query_params.get('complaint_id', [''])[0]
    decoded_param = base64.b64decode(encoded_param).decode('utf-8')
    complaint_id = decoded_param.split('=')[1]
    return complaint_id

# Read the complaint ID from URL query parameters
url = st.experimental_get_query_params().get('url', [''])[0]
complaint_id = extract_complaint_id(url)

# Rest of your code remains the same

# Style the feedback form
def style_feedback_form(complaint_id):
    # Add logo with increased size
    logo_image = "https://github.com/bunny2ritik/Utl-feedback/blob/main/newlogo.png?raw=true"  # Path to your logo image
    st.image(logo_image, use_column_width=True, width=400)
    
    # Display the title for the complaint ID without quotation marks
    st.markdown(f"<h3 style='text-align: center;'>Feedback for Complaint ID : {complaint_id}</h3>", unsafe_allow_html=True)

    # Set title for service engineer section
    st.header('Service Engineer ')

    # Add text area for engineer feedback
    engineer_review = st.text_area('Write your feedback for the Service Engineer here:')

    # Set title for service coordinator section
    st.header('Service Executive Coordinator' )

    # Add text area for coordinator feedback
    coordinator_review = st.text_area('Write your feedback for the Service Executive Coordinator here:')

    return engineer_review, coordinator_review

# Style the feedback form
engineer_review, coordinator_review = style_feedback_form(complaint_id)

# Add a submit button with custom style
submit_button_style = """
    <style>
        div.stButton > button:first-child {
            background-color: #4CAF50; /* Green */
            color: white;
        }
    </style>
"""

# Inject the submit button style into the Streamlit app
st.markdown(submit_button_style, unsafe_allow_html=True)

# Add a submit button
submit_button = st.button('Submit')

# Submit feedback and handle API request
if submit_button:
    # Submit feedback and handle API request
    if complaint_id:
        submit_feedback(complaint_id, engineer_review, coordinator_review)







