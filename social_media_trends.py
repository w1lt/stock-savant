import praw
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
    
    sentiments = (sum(sentiments) / len(sentiments)) # Average sentiment score of Reddit posts
    all_social_media_data = [sentiments, len(reddit_posts)]
    return all_social_media_data

# Now you can call analyze_social_media_data with a company_name argument
# in the other file to get the all_social_media_data.
