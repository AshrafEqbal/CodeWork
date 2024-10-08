from flask import Flask, render_template_string, request, redirect, url_for
from transformers import pipeline
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the sentiment analysis pipeline with the specified model
sentiment_analysis = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Mapping from the model's labels to more meaningful terms
label_mapping = {
    'LABEL_0': 'Negative',
    'LABEL_1': 'Neutral',
    'LABEL_2': 'Positive'
}

# To store previous submissions
submissions = []

def analyze_sentiment(text):
    # Get sentiment prediction
    result = sentiment_analysis(text)
    return result

def create_sentiment_distribution(submissions):
    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for item in submissions:
        sentiment_counts[item['sentiment']] += 1

    plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'blue', 'red'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment_term = None  # Initialize sentiment term
    if request.method == 'POST':
        review = request.form['review']
        result = analyze_sentiment(review)
        label = result[0]['label']
        sentiment_term = label_mapping.get(label, "Unknown")

        # Store submission
        submissions.append({'review': review, 'sentiment': sentiment_term})

    sentiment_plot = create_sentiment_distribution(submissions)
    return render_template_string(HTML_TEMPLATE, submissions=submissions, plot=sentiment_plot, sentiment=sentiment_term)

HTML_TEMPLATE = '''
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
    <form method="POST" action="/">
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
            <img src="data:image/png;base64,{{ plot }}" alt="Sentiment Distribution" style="width: 100%; border-radius: 8px;">
        </div>
    </div>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
