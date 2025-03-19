from flask import Flask, render_template, request
import google.generativeai as genai
from textblob import TextBlob

app = Flask(__name__)

# Configure the generative AI model
genai.configure(api_key="AIzaSyBsMUmdISsmSWDQK1gojqPXBIcLlBSFYJ0")
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summarize():
    url = request.form['url']
    response = model.generate_content("summarize the following text: " + url.strip(), stream=True)
    summary = ''.join(chunk.text for chunk in response)

    # Perform sentiment analysis on the summary
    analysis = TextBlob(summary)
    polarity = analysis.sentiment.polarity 

    if polarity > 0:
        sentiment = 'happy 😁'
    elif polarity < 0:
        sentiment = 'sad 😞'
    else:
        sentiment = 'neutral 🙂' 

    return render_template('summary.html', summary=summary, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
