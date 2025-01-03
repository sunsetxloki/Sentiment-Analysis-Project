from urllib.parse import quote as url_quote
from flask import Flask, render_template, request, redirect, url_for
import pickle
import re

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained model and vectorizer
try:
    model = pickle.load(open('sentiment_model.pkl', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    print("Model and vectorizer loaded successfully.")
except Exception as e:
    print(f"ERROR: Could not load model or vectorizer - {e}")

# Text preprocessing function
def clean_text(text):
    # Lowercase all text
    text = text.lower()
    # Remove any repetitive characters (e.g., "sooo good" -> "so good")
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    # Slang replacements
    slang_dict = {
        'peak': 'amazing',
        'banger': 'excellent',
        'lit': 'awesome',
        'meh': 'average',
        'tbh': 'to be honest',
        'fr': 'for real'
    }
    for slang, proper in slang_dict.items():
        text = text.replace(slang, proper)
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# Home route to render index page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route to handle review submission
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the review from the form
        review = request.form.get('review', '').strip()
        if not review:
            return render_template('index.html', error="Please enter a review to analyze.")
        
        # Clean the review text
        cleaned_review = clean_text(review)
        
        # Transform the cleaned review using the vectorizer
        transformed_review = vectorizer.transform([cleaned_review])
        
        # Predict sentiment using the model
        prediction = model.predict(transformed_review)[0]
        
        # Mapping the numerical prediction to a sentiment label and emoji
        sentiment_map = {
            0: ("Negative", "😞"),
            1: ("Positive", "😊")
        }
        
        # Get the sentiment label and emoji from the prediction
        sentiment_label, sentiment_emoji = sentiment_map.get(prediction, ("Unknown", "🤔"))
        
        # Redirect to result page with sentiment information
        return redirect(url_for('result', sentiment_label=sentiment_label, sentiment_emoji=sentiment_emoji))
    
    except Exception as e:
        print(f"ERROR: {e}")
        return render_template('index.html', error="Something went wrong during prediction.")

# Result page to display the sentiment
@app.route('/result')
def result():
    try:
        # Retrieve sentiment details from the URL parameters
        sentiment_label = request.args.get('sentiment_label', None)
        sentiment_emoji = request.args.get('sentiment_emoji', None)
        
        if not sentiment_label or not sentiment_emoji:
            return redirect(url_for('home'))  # Redirect to home if no sentiment info
        
        return render_template('result.html', sentiment_label=sentiment_label, sentiment_emoji=sentiment_emoji)
    
    except Exception as e:
        print(f"ERROR: {e}")
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
