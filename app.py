from flask import Flask, render_template, request
import calc_12_avg as calc
import news_sentiment as news
import social_media_trends as social
import monte_carlo_sim as msc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']


        months_12 = calc.calc_12_avg(ticker_symbol)
        monthly_avg_change = months_12[0]
        monthly_stdev = months_12[1] #takes in company stock name as string

        news_data = news.get_company_news_sentiment(ticker_symbol) #takes in company stock name as string
        news_sentiment = news_data[0]
        news_stdev = news_data[1]

        social_data = social.analyze_social_media_data(ticker_symbol) #takes in company stock name as string
        social_sentiment = social_data[0]
        social_stdev = social_data[1]

        social_reddit_post_mean = social_data[2]


        msc_results = msc.predict_earnings(stock_change_mean = monthly_avg_change,
                                            stock_change_std = monthly_stdev,
                                            news_sentiment_mean = news_sentiment,
                                            news_sentiment_std = news_stdev,
                                            social_sentiment_mean = social_sentiment,
                                            social_sentiment_std = social_stdev,
                                            reddit_mentions_mean = social_reddit_post_mean,
                                            )
        

        return render_template('result.html', stock_change_mean = monthly_avg_change,
                                            stock_change_std = monthly_stdev,
                                            news_sentiment_mean = news_sentiment,
                                            news_sentiment_std = news_stdev,
                                            social_sentiment_mean = social_sentiment,
                                            social_sentiment_std = social_stdev,
                                            reddit_mentions_mean = social_reddit_post_mean,
                                            msc_results = msc_results,)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()