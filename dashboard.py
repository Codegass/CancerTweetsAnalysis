import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re
import plotly.plotly as py
import plotly.graph_objs as go

import nltk

### NLP Analyzer ###
class nltk_analyzer():

    def __init__(self, tweets):
        self.all_tweets = 


    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).lower().split())






app = dash.Dash('Cancer Tweets Analyzer Dashboard')

app.layout = html.Div(children)
if __name__ == "__main__":
    app.run_server(debug=True)