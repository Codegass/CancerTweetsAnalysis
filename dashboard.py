import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re

import nltk
from nltk.corpus import stopwords


### NLP Analyzer ###
class nltk_analyzer():

    def __init__(self, dataframe):
        tweets_list = dataframe.tweets
        sentence = ''
        for tweets in tweets_list:
            sentence = sentence + ' ' + tweets

        self.all_tweets_tokens = self.clean_tweet(sentence).split()
        self.clean_tokens = list()
        self.project_specific_list = ['one','please', 'time', 'cancersucks', 'cancer'] 
        self.clean_tokens_without_sr(self.all_tweets_tokens)
        

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).lower().split())

    def clean_tokens_without_sr(self, token_list):
        sr = stopwords.words('english')
        for token in token_list:
            if token not in sr and token not in self.project_specific_list:
                self.clean_tokens.append(token)

    def Freq(self):
        fdist = nltk.FreqDist(self.clean_tokens)
        sorted_fdist = sorted(fdist.items(),key=lambda item:item[1],reverse=True)
        key = []
        value = []
        for k,v in sorted_fdist:
            key.append(k)
            value.append(v)

        return key[:20],value[:20]


### Graph Data ###
class graph():

    def __init__(self):
        pass

    def sentiment_data(self, df):
        Negtive = df.groupby(['sentiment']).size()[-1]
        Positive = df.groupby(['sentiment']).size()[-1]
        Neutrality = df.groupby(['sentiment']).size()[0]

        labels = ['Negtive','Positive','Neutrality']
        values = [Negtive,Positive,Neutrality]
        return labels, values



app = dash.Dash('Cancer Tweets Analyzer Dashboard')

tweets_dataframe = pd.read_csv("data.csv")
labels_sen, values_sen = graph().sentiment_data(tweets_dataframe)
labels_fre, values_fre = nltk_analyzer(tweets_dataframe).Freq()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(
        children='Cancer Tweets Analyzer Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        html.Div([dcc.Graph(
            id = 'sentiment',
            figure={
                'data':[{
                    'labels':labels_sen,
                    'values':values_sen,
                    'type':'pie',
                    'hoverinfo':'label+value+percent',
                    'hole':0.4,

                }],
                'layout': {
                    'title': 'Sentiment',
                    'margin': {'l':30,'r':30},
                }
            }
        )],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(
            id = 'Words Frequence',
            figure={
                'data':[{
                    'x':labels_fre,
                    'y':values_fre,
                    'type':'bar',
                }],
                'layout':{
                    'title': 'Words Frequence in Cancer Tweets',
                }
            }
        )],style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(
            id='teets_df',
            figure={
                'data': [{
                    'type': 'table',
                    'columnwidth': 0.3,
                    'header': {
                        'values': [['<b>{}</b>'.format(i)] for i in tweets_dataframe.columns],
                        'font': {'size': 13, 'color': 'white', },
                        'align': 'center',
                        'height': 30,
                        'fill': {'color': '#0076BA'},
                    },
                    'cells': {
                        'values': tweets_dataframe.values.T,
                        'line': {'color': 'rgb(50, 50, 50)'},
                        'align': 'center',
                        'height': 27,
                        'fill': {'color': ['#56C1FF', '#f5f5fa']},
                    },
                }],

                'layout': {
                    # 'height': 250,
                    'title': 'Tweets with Info',
                    'margin': {'l': 10, 'r': 10, 't': 50, 'b': 10},
                }
            },
        ),
    ])
])


if __name__ == "__main__":


    app.run_server(host='127.0.0.1', port='8050',debug=True)