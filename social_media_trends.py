import praw
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import statistics  # Importing the statistics module for standard deviation

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

subreddit_name = "StockMarket"

def fetch_reddit_data(company_name, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for submission in subreddit.search(company_name, limit=10):  # Adjust the number of posts as needed
        posts.append(submission.title + ' ' + submission.selftext)
    return posts

def analyze_social_media_data(company_name): #takes in string func pararmeter
    reddit_posts = fetch_reddit_data(company_name, subreddit_name)
    
    # Perform sentiment analysis on a subset of 10 Reddit posts using BERT
    sentiments = []
    for post in reddit_posts[:10]:
        inputs = tokenizer(post, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item() + 1  # sentiment score from 1 to 5
        sentiments.append(predicted_class)
    
    avg_sentiments = (sum(sentiments) / len(sentiments)) # Average sentiment score of Reddit posts
    sentiment_stdev = statistics.stdev(sentiments)  # Standard deviation of sentiments
    
    avg_reddit_mentions = (len(reddit_posts) / 10)  # Average number of Reddit mentions
    reddit_mentions_stdev = statistics.stdev(avg_reddit_mentions)  # Standard deviation of Reddit mentions

    social_media_data = [avg_sentiments, sentiment_stdev, avg_reddit_mentions, reddit_mentions_stdev]
    return social_media_data
