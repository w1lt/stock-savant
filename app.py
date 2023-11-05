from flask import Flask, render_template, request
import calc_12_avg as calc
import news_sentiment as news
import social_media_trends as social
import llama as llm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']


        months_12 = calc.calc_12_avg(ticker_symbol)
        monthly_averages = months_12[0]
        monthly_averages_1_number = months_12[1] #takes in company stock name as string
        news_sentiment = news.get_company_news_sentiment(ticker_symbol) #takes in company stock name as string
        social_data = social.analyze_social_media_data(ticker_symbol) #takes in company stock name as string
        social_sentiment = social_data[0]
        social_posts = social_data[1]

        llm_response = llm.gen_output(ticker_symbol)
    

        return render_template('result.html', ticker=ticker_symbol, averages=monthly_averages, avg_number = monthly_averages_1_number, news_sentiment=news_sentiment, social_sentiment=social_sentiment, social_posts = social_posts, llm_response = llm_response)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()