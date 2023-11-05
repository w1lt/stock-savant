import numpy as np

# Function to ensure that values like sentiment don't go outside their defined range.
def bound_value(value, lower_bound, upper_bound):
    return max(min(value, upper_bound), lower_bound)

def predict_earnings(
    stock_change_mean,
    stock_change_std,
    news_sentiment_mean,
    news_sentiment_std,
    social_sentiment_mean,
    social_sentiment_std,
    reddit_mentions_mean,
    n_simulations=20
):
    # Define hypothetical coefficients for the model. These are the weights we assign to each factor 
    # when predicting earnings. In a real-world scenario, these would be determined using regression analysis 
    # on past data.
    beta1 = 1000
    beta2 = 50
    beta3 = 100
    beta4 = 30

    # Initialize a list to store results of each simulation.
    earnings_results = []

    # Run the Monte Carlo simulation for the defined number of times.
    for _ in range(n_simulations):
        
        # Randomly sample from a normal distribution for stock change.
        stock_change = np.random.normal(stock_change_mean, stock_change_std)
        
        # Randomly sample for news and social sentiment, considering a small correlation between them.
        news_sentiment, social_sentiment = np.random.multivariate_normal(
            [news_sentiment_mean, social_sentiment_mean],
            [[news_sentiment_std**2, 0.1], [0.1, social_sentiment_std**2]]
        )
        
        # Ensure the sentiment values are bound between 1 and 5.
        news_sentiment = bound_value(news_sentiment, 1, 5)
        social_sentiment = bound_value(social_sentiment, 1, 5)
        
        # Calculate predicted earnings based on the hypothetical model and include the reddit_mentions_mean.
        predicted_earnings = (beta1 * stock_change) + (beta2 * news_sentiment**3) + (beta3 * social_sentiment**2) + (beta4 * np.log(reddit_mentions_mean + 1))
        
        # Append the result to our list.
        earnings_results.append(predicted_earnings)
    
    average_earning_results = np.mean(earnings_results) # Calculate the average of all the results.

    return average_earning_results
