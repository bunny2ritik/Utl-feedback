import streamlit as st
import requests
from textblob import TextBlob
import base64

# Function to decode the complaint ID from the URL query parameters
def decode_complaint_id_from_url(url_query):
    if url_query:
        complaint_id_encoded = url_query.get('q', [''])[0]
        if complaint_id_encoded:
            try:
                # Remove leading/trailing spaces from the encoded string
                complaint_id_encoded = complaint_id_encoded.strip()
                
                # Add padding to the base64-encoded string, if necessary
                padding_needed = len(complaint_id_encoded) % 4
                if padding_needed != 0:
                    complaint_id_encoded += '=' * (4 - padding_needed)
                
                # Decode the base64-encoded complaint ID
                complaint_id_decoded = base64.b64decode(complaint_id_encoded).decode('utf-8')
                return complaint_id_decoded
            except Exception as e:
                st.error(f"Error decoding complaint ID: {e}")
                st.stop()
    st.error("Complaint ID not found in URL query parameters.")
    st.stop()

# Function to submit feedback and handle API request
def submit_feedback(complaint_id, engineer_review, coordinator_review):
    # Perform sentiment analysis for engineer review
    engineer_sentiment = perform_sentiment_analysis(engineer_review)

    # Perform sentiment analysis for coordinator review
    coordinator_sentiment = perform_sentiment_analysis(coordinator_review)

    # Derive ratings from sentiment analysis
    engineer_rating = derive_rating(engineer_sentiment)
    coordinator_rating = derive_rating(coordinator_sentiment)

    # Save the feedback to the API database
    save_feedback_to_api(complaint_id, engineer_review, engineer_rating, coordinator_review, coordinator_rating, engineer_sentiment, coordinator_sentiment)
    
    # Display sentiment analysis results
    st.header('Sentiment Analysis Results:')
    st.write('Service Engineer Review Sentiment:', engineer_sentiment)
    st.write('Service Executive Coordinator Review Sentiment:', coordinator_sentiment)

# Function to perform sentiment analysis using TextBlob
def perform_sentiment_analysis(review_text):
    sentiment = TextBlob(review_text).sentiment
    polarity = sentiment.polarity
    
    # Determine sentiment category based on polarity score
    if polarity <= -0.5:
        return 'Very Bad'
    elif polarity <= 0:
        return 'Bad'
    elif polarity <= 0.5:
        return 'Good'
    else:
        return 'Excellent'

# Function to derive ratings from sentiment category
def derive_rating(sentiment_category):
    if sentiment_category == 'Very Bad':
        return 1.0
    elif sentiment_category == 'Bad':
        return 2.5
    elif sentiment_category == 'Good':
        return 4.0
    else:
        return 5.0

# Function to save feedback data to API
def save_feedback_to_api(complaint_id, engineer_review, engineer_rating, coordinator_review, coordinator_rating, engineer_sentiment, coordinator_sentiment):
    # Feedback data including complaint ID
    feedback_data = {
        'apiKey': 'RnVqaXlhbWEgUG93ZXIgU3lzdGVtcyBQdnQuIEx0ZC4=.$2y$10$sd9eji2d1mc8i1nd1xsalefYiroiLa46/X0U9ihoGeOU7FaWDg30a.',  # Replace with your actual API key
        'complaint_id': complaint_id,
        'engineer_feedback': {
            'feedback': engineer_review,
            'rating': engineer_rating,
            'output': engineer_sentiment
        },
        'coordinator_feedback': {
            'feedback': coordinator_review,
            'rating': coordinator_rating,
            'output': coordinator_sentiment
        }
    }

    # API endpoint
    api_url = 'https://staging.utlsolar.net/tracker/production/public/utlmtlapis/getCustomerFeedback'  # Replace with your actual API endpoint

    # Make a POST request to the API endpoint
    response = requests.post(api_url, json=feedback_data)

    # Check if the request was successful
    if response.status_code == 200:
        st.success('Feedback submitted successfully!')
    else:
        st.error('Failed to submit feedback. Please try again later.')

# Main function to render the feedback form and handle user input
def main():
    # Read the URL query parameters using st.query_params
    url_query = st.query_params

    # Decode the complaint ID from the URL query parameters
    complaint_id_decoded = decode_complaint_id_from_url(url_query)

    # Style the feedback form
    def style_feedback_form(complaint_id):
        # Add logo with increased size
        logo_image = "https://github.com/bunny2ritik/Utl-feedback/blob/main/newlogo.png?raw=true"  # Path to your logo image
        st.image(logo_image, use_column_width=True, width=400)
        
        # Display the title for the complaint ID without quotation marks
        st.markdown(f"<h3 style='text-align: center;'>Feedback for Complaint ID: {complaint_id}</h3>", unsafe_allow_html=True)

        # Set title for service engineer section
        st.header('Service Engineer Feedback')

        # Add text area for engineer feedback
        engineer_review = st.text_area('Write your feedback for the Service Engineer here:')

        # Set title for service executive coordinator section
        st.header('Service Executive Coordinator Feedback')

        # Add text area for coordinator feedback
        coordinator_review = st.text_area('Write your feedback for the Service Executive Coordinator here:')

        return engineer_review, coordinator_review

    # Style the feedback form and collect user input
    engineer_review, coordinator_review = style_feedback_form(complaint_id_decoded)

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
        if complaint_id_decoded:
            submit_feedback(complaint_id_decoded, engineer_review, coordinator_review)

# Run the application
if __name__ == '__main__':
    main()
