from flask import Flask, render_template, request
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

# Sample DataFrame
data = pd.read_csv('Products.csv')

df = pd.DataFrame(data)

# Tokenize user input
def tokenize_input(user_input):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(user_input.lower())
    return [word for word in tokens if word.isalnum() and word not in stop_words]

# Find matching rows based on Brand column
def find_matching_rows(user_input):
    user_tokens = tokenize_input(user_input)
    matching_rows = df[df['Brand'].apply(lambda x: any(token in tokenize_input(x) for token in user_tokens))]
    return matching_rows

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    matching_rows = find_matching_rows(user_input)

    return render_template('index.html', user_input=user_input, matching_rows=matching_rows)

if __name__ == '__main__':
    app.run(debug=True)
