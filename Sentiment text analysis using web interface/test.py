from flask import Flask, request, render_template_string, send_file
import re
import pandas as pd
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import io

# Download NLTK data if not already downloaded
#nltk.download('punkt')
#nltk.download('stopwords')

# Load pre-trained model and vectorizer for prediction
def load_model(model_path='model.pkl', vectorizer_path='tfidf.pkl', scaler_path='scaler.pkl'):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    scaler = joblib.load(scaler_path)
    return model, vectorizer, scaler

# Function to preprocess and predict sentiment
def preprocess_text(text):
    text = re.sub('<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation and non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize the review
    
    processed_tokens = []
    negate = False

    for token in tokens:
        if token in {"not", "no", "never", "n't"}:
            negate = True
            processed_tokens.append(token)
        else:
            if negate:
                token = "not_" + token  # Append 'not_' to the token
                negate = False  # Reset negation
            if token not in set(stopwords.words('english')):
                processed_tokens.append(PorterStemmer().stem(token))  # Apply stemming

    return ' '.join(processed_tokens)

def predict_sentiment(model, vectorizer, scaler, review):
    cleaned_review = preprocess_text(review)  # Preprocess the review text
    tfidf_review = vectorizer.transform([cleaned_review])  # Transform the review using the tf-idf vectorizer
    tfidf_review = scaler.transform(tfidf_review)  # Scale the transformed review
    sentiment_prediction = model.predict(tfidf_review)  # Predict sentiment
    return sentiment_prediction[0]  # Return the sentiment label

app = Flask(__name__)

# Load the model, vectorizer, and scaler
model, vectorizer, scaler = load_model()

# Initialize a list to store previous submissions
submissions = []

# HTML template for the form and previous submissions with CSS styling
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Sentiment Analysis</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #282c34;
            margin: 0;
            padding: 40px;
            color: #f8f9fa;
        }
        h1 {
            color: #61dafb;
            border-bottom: 3px solid #21a1f1;
            padding-bottom: 15px;
            text-align: center;
            font-size: 2.5em;
        }
        form {
            background: #3c4043;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            max-width: 700px;
            margin: 20px auto;
            border: 1px solid #444;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 1px solid #555;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
            resize: none;
            background-color: #2c2f33;
            color: #f8f9fa;
        }
        button {
            background-color: #21a1f1;
            border: none;
            color: #fff;
            padding: 12px 25px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 18px;
            margin: 15px 0;
            cursor: pointer;
            border-radius: 6px;
            transition: background-color 0.3s, transform 0.2s;
        }
        button:hover {
            background-color: #1e90ff;
            transform: translateY(-2px);
        }
        h2 {
            color: #61dafb;
            font-size: 1.8em;
            margin-top: 20px;
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #3c4043;
            padding: 20px;
            border: 1px solid #444;
            border-radius: 6px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        strong {
            color: #f8f9fa;
        }
        .right, .left {
            width: 48%;
            padding: 10px;
            border: 1px solid #444;
            height: 60vh;
            box-sizing: border-box;
            overflow: auto;
            border-radius: 8px;
            margin: 20px 1%;
            background: #3c4043;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            float: left;
        }
        .right {
            float: right;
        }
        .container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
    </style>
</head>
<body>
    <h1>Enter a Review for Sentiment Analysis</h1>
    <form method="POST" action="/submit">
        <label for="review" style="color: #f8f9fa;">Review:</label>
        <textarea id="review" name="review" rows="4" required></textarea>
        <button type="submit">Submit</button>
    </form>
    {% if sentiment %}
        <h2>Predicted Sentiment: {{ sentiment }}</h2>
    {% endif %}
    <div class="container">
        <div class="left">
            <h2>Previous Submissions</h2>
            <ul>
                {% for item in submissions|reverse %}
                    <li><strong>Review:</strong> {{ item.review }} <br><strong>Sentiment:</strong> {{ item.sentiment }}</li>
                {% endfor %}
            </ul>
        </div>
        <div class="right">
            <h2>Sentiment Distribution</h2>
            <img src="/plot" alt="Sentiment Distribution" style="width: 100%; border-radius: 8px;">
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(html_template, submissions=submissions)

@app.route('/submit', methods=['POST'])
def submit():
    review = request.form.get('review')
    sentiment = predict_sentiment(model, vectorizer, scaler, review)
    submissions.append({'review': review, 'sentiment': sentiment})
    return render_template_string(html_template, sentiment=sentiment, submissions=submissions)

@app.route('/plot')
def plot():
    # Prepare data for plotting
    sentiment_counts = pd.Series([item['sentiment'] for item in submissions]).value_counts()
    
    # Create a plot
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', ax=ax, color=['#007bff', '#dc3545'])
    ax.set_title('Sentiment Distribution')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Frequency')
    plt.xticks(rotation=0)
    
    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
