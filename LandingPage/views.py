from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime as dt
import traceback
import requests
import os


# Create your views here.

def landing(request):
    news_data = news(request)

    return render(request, 'landing.html', {'news_data': news_data})

def graph(request):
    if request.method == 'POST':
        ticker = request.POST.get('ticker', '')

        if not ticker:
            return HttpResponse("Ticker not provided", status=400)

        try:
            now = dt.datetime.now()
            five_years_ago = now - dt.timedelta(days=5*365)
            
            data = yf.download(ticker, start=five_years_ago, end=now, )['Adj Close']
            data = data.to_frame()
            data.reset_index(inplace=True)

            # Plot
            fig = px.line(data, x='Date', y='Adj Close', title=ticker, labels={'y': 'Stock Price'})
            fig.update_xaxes(rangeslider_visible=True)
            graph_json = fig.to_json()

            return HttpResponse(graph_json, content_type='application/json')
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_message = f"Error: {str(e)}\n\nTraceback:\n{traceback_str}"
            return HttpResponse(error_message, status=500)


    return HttpResponse("Invalid request method", status=400)

load_dotenv()
api_key = os.getenv('RAPIDAPI_KEY')
def news(request):
    try:
        url = "https://seekingalpha.p.rapidapi.com/news/v2/list-trending"
        querystring = {"size":"20"}
        headers = {
            "X-RapidAPI-Key": os.environ.get('RAPIDAPI_KEY'),
            "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
        }

        # rest of the code

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Parse the response to get the news articles
        news_data = []
        for item in data['data']:  # 'data' field is a list of news items
            title = item['attributes']['title']
            url = "https://seekingalpha.com/news/" + item['id']  # Construct the URL from the 'id'
            date = item['attributes']['publishOn']
            news_data.append({'title': title, 'url': url, 'date': date})

        return news_data
    except Exception as e:
        print(e)
        return []