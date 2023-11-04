import requests
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Define the BERT model and tokenizer for sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Define the API endpoint to fetch news data
news_api_endpoint = "https://newsapi.org/v2/everything"
company_name = "AAPL"

# Fetch news data from News API
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

news_articles = fetch_news_data(company_name)

# Perform sentiment analysis on news articles using BERT
sentiments = []
logits_list = []
for article in news_articles:
    inputs = tokenizer(article, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item() + 1  # sentiment score from 1 to 5
    sentiments.append(predicted_class)  
    logits_list.append(logits.tolist())

# Create a DataFrame to store sentiment data
data = {"News Article": news_articles, "Sentiment": sentiments, "Logits": logits_list}
df = pd.DataFrame(data)

# Save the sentiment data to a CSV file
df.to_csv("news_sentiment_data.csv", index=False)

print("Sentiment analysis completed. Data saved to news_sentiment_data.csv.")
