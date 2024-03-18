import streamlit as st
import requests
from textblob import TextBlob
import base64

# Function to submit feedback and handle API request
def submit_feedback(complaint_id, engineer_review, coordinator_review, additional_data):
    # Perform sentiment analysis for engineer review
    engineer_sentiment = perform_sentiment_analysis(engineer_review)

    # Perform sentiment analysis for coordinator review
    coordinator_sentiment = perform_sentiment_analysis(coordinator_review)

    # Derive ratings from sentiment analysis
    engineer_rating = derive_rating(engineer_sentiment)
    coordinator_rating = derive_rating(coordinator_sentiment)

    # Combine additional data with the feedback data
    feedback_payload = {
        'complaint_id': complaint_id,
        'engineer_feedback': {
            'feedback': engineer_review,
            'rating': engineer_rating,
            'sentiment': engineer_sentiment
        },
        'coordinator_feedback': {
            'feedback': coordinator_review,
            'rating': coordinator_rating,
            'sentiment': coordinator_sentiment
        },
        'additional_data': additional_data
    }

    # Save the feedback to the API database
    save_feedback_to_api(feedback_payload)

# Function to perform sentiment analysis using TextBlob
def perform_sentiment_analysis(review_text):
    sentiment_analysis = TextBlob(review_text).sentiment
    polarity_score = sentiment_analysis.polarity
    
    # Determine sentiment category based on polarity score
    if polarity_score <= -0.5:
        return 'Very Bad'
    elif polarity_score <= 0:
        return 'Bad'
    elif polarity_score <= 0.5:
        return 'Good'
    else:
        return 'Excellent'

# Function to derive ratings from sentiment polarity score
def derive_rating(sentiment_score):
    if sentiment_score == 'Very Bad':
        return 1.0
    elif sentiment_score == 'Bad':
        return 2.5
    elif sentiment_score == 'Good':
        return 4.0
    else:
        return 5.0

# Function to save feedback data to API
def save_feedback_to_api(feedback_payload):
    # API endpoint
    api_url = 'https://staging.utlsolar.net/tracker/production/public/utlmtlapis/getCustomerFeedback'

    # Make a POST request to the API endpoint with the feedback payload
    response = requests.post(api_url, json=feedback_payload)

    # Check if the request was successful
    if response.status_code == 200:
        st.success('Feedback submitted successfully!')
    else:
        st.error('Failed to submit feedback. Please try again later.')

# Read the complaint ID from URL query parameters and decode it
encoded_complaint_id = st.experimental_get_query_params().get('complaint_id', [''])[0]
complaint_id = base64.urlsafe_b64decode(encoded_complaint_id).decode('utf-8')

# Style the feedback form
def style_feedback_form():
    # Add logo with increased size
    logo_image = "https://github.com/bunny2ritik/Utl-feedback/blob/main/newlogo.png?raw=true"  # Path to your logo image
    st.image(logo_image, use_column_width=True, width=400)
    
    # Display the title for the complaint ID
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

# Additional data (you can customize this)
additional_data = {
    'customer_name': 'John Doe',
    'contact_number': '123-456-7890'
}

# Style the feedback form
engineer_review, coordinator_review = style_feedback_form()

# Add a submit button
submit_button = st.button('Submit')

# Submit feedback and handle API request
if submit_button:
    submit_feedback(complaint_id, engineer_review, coordinator_review, additional_data)
