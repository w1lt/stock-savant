import praw
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Define the BERT model and tokenizer for sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id='clmYHjiEpgwCgVl40pn76Q',
    client_secret='n16VUaqBn0C6mivikDWiupZcULpaYw',
    user_agent='python:StockSavant:v1.0 (by /u/Aggravating-Gas-5659)'
)

company_name = "AAPL"
subreddit_name = "StockMarket"

def fetch_reddit_data(company_name, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for submission in subreddit.search(company_name, limit=10):  # Adjust the number of posts as needed
        posts.append(submission.title + ' ' + submission.selftext)
    return posts

reddit_posts = fetch_reddit_data(company_name, subreddit_name)

# Perform sentiment analysis on a subset of 10 Reddit posts using BERT
sentiments = []
for post in reddit_posts:
    inputs = tokenizer(post, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item() + 1  # sentiment score from 1 to 5
    sentiments.append(predicted_class)  

# Create a DataFrame to store sentiment data
data = {"Reddit Post": reddit_posts, "Sentiment": sentiments}
df = pd.DataFrame(data)

# Save the sentiment data to a CSV file
df.to_csv("reddit_sentiment_data.csv", index=False)

print(f"Sentiment analysis completed for {len(reddit_posts)} Reddit posts. Data saved to reddit_sentiment_data.csv.")
