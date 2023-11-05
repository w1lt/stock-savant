import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import statistics  # Importing the statistics module for standard deviation

# Define the BERT model and tokenizer for sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Define the API endpoint to fetch news data
news_api_endpoint = "https://newsapi.org/v2/everything"

def fetch_news_data(company_name):
    params = {
        "q": company_name,
        "pageSize": 10,  # Max number of articles to retrieve
    }
    headers = {
        "x-api-key": "47d31e1d0e564f16815644e77a24f5d3"  # API key 
    }
    response = requests.get(news_api_endpoint, params=params, headers=headers)
    
    # Check if the response is successful (HTTP Status Code 200)
    if response.status_code != 200:
        print(f"Error: Unable to fetch news data. HTTP Status Code: {response.status_code}")
        return []
    
    news_data = response.json()

    # Check if response is successful (status code "ok")
    if news_data["status"] != "ok":
        print("Error fetching news data:", news_data.get("message", "Unknown error"))
        return []

    return [article["description"] for article in news_data["articles"]]

def get_company_news_sentiment(company_name): # company_name is a string
    news_articles = fetch_news_data(company_name)

    # Perform sentiment analysis on news articles using BERT
    sentiments = []
    for article in news_articles:
        inputs = tokenizer(article, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item() + 1  # sentiment score from 1 to 5
        sentiments.append(predicted_class)  

    if len(sentiments) == 0:
        return None  # or handle it differently, like returning a message or raising an exception
    
    avg_news_sentiment = (sum(sentiments) / len(sentiments)) # Average sentiment score of news articles
    news_sentiment_stdev = statistics.stdev(avg_news_sentiment)  # Standard deviation of sentiments

    news_sentiment_data = [avg_news_sentiment, news_sentiment_stdev]
    return news_sentiment_data