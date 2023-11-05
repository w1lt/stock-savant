from flask import Flask, render_template, request
import calc_12_avg as calc
import news_sentiment as news
import social_media_trends as social

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']

        # Calculate the 12-month averages
        try:
            monthly_averages = calc.calc_12_avg(ticker_symbol)[0]
            company_name = calc.calc_12_avg(ticker_symbol)[1]
            news_sentiment = news.get_company_news_sentiment(ticker_symbol) #takes in company stock name as string
            social_data = social.analyze_social_media_data(ticker_symbol) #takes in company stock name as string
            social_sentiment = social_data[0]
            social_posts = social_data[1]
            

        except:
            return render_template('index.html', error=True)

        return render_template('result.html', ticker=ticker_symbol, company_name = company_name, averages=monthly_averages, news_sentiment=news_sentiment, social_sentiment=social_sentiment, social_posts = social_posts)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()