import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
import datetime

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('https://gitcdn.xyz/repo/simon-mcmahon/nytimes-emotion/update/nytimes_dash_output.csv')

markdown_text_head= '''

## New York Times Trending Article Emotion and Bias

**Do different social media platforms have different "flavours" of content which people share on them?**  
    
    
'''
markdown_text_middle = '''
. 
.  
.  
.  

#### What is going on here?

The New York times publishes a list of the top 10 shared articles across Facebook, Twitter, Email and Most Viewed (on nytimes.com) [here](http://www.nytimes.com/most-popular.html). The page updates every 15 minutes.

A web crawling script was set up to check the top 10 articles every 15 minutes, extract the headline and the text, pass it through an NLP sentiment analysis neural net and plot the key attributes for you here, updated in real time.

#### Meaning of the scores
'''
markdown_text_below = '''
#### Controlling the Graph

* Hover over a place on the graph to see the headline of the most popular article for context. 
* Zoom to a region by clicking and dragging. 
* To zoom back out, double click on the graph.

###### Crafted by [Simon McMahon](https://www.linkedin.com/in/simon-mcmahon/)

'''

app.title='NY times Sentiment Analysis'

time_string = '%Y-%m-%d %H:%M:%S'

#Do the calculations required for the time slider

time_string = '%Y-%m-%d %H:%M:%S'

time_min = df['query_time'].min()
time_min = datetime.datetime.strptime(time_min, time_string)

time_max = df['query_time'].max()
time_max = datetime.datetime.strptime(time_max, time_string)

diff = time_max - time_min

days_recorded = diff.days


Radio_button_font_size = '120%'

app.layout = html.Div([
    dcc.Markdown(children=markdown_text_head),
    html.Div([
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Top 1', 'value': 'top1'},
                    {'label': 'Top 10', 'value': 'top10'},
                ],
                value='MTL',
                id = '1-or-10',
                labelStyle={'display': 'inline-block'}
            )],className = 'four columns',style={'display': 'inline-block','fontSize': Radio_button_font_size}),

        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Polarity', 'value': 'pol'},
                    {'label': 'Subjectivity', 'value': 'sub'},
                ],
                value='MTL',
                id='pol-or-sub',
                labelStyle={'display': 'inline-block'}
            )],className = 'four columns',style={'float': 'center', 'display': 'inline-block','fontSize': Radio_button_font_size}),

        dcc.Checklist(
            options=[
                {'label': 'fb', 'value': 'fb'},
                {'label': 'twitter', 'value': 'twitter'},
                {'label': 'email', 'value': 'email'},
                {'label': 'viewed', 'value': 'viewed'}
            ],
            values=['fb', 'twitter', 'email', 'viewed'], labelStyle={'display': 'inline-block'},
            className='four columns', id='series-plot', style={'float':'right','fontsize': Radio_button_font_size})
    ] ,className = 'row'),
    html.Div([

    ],className = 'row'),
    html.Div([
        dcc.Graph(id='test-top-1-polarity',className='u-full-width'),

    ],className = 'row'),

#Note here the slider value of 1 should correspond to days_recorded days displayed on the graph due to labelling weirdness
    dcc.Slider(
        id='time-slider',
        min=1,
        max=5,
        value=5,
        step=None,
        marks={5:'1 day', 4:'3 days', 3:'1 week', 2:'2 weeks', 1:'1 month'}
    ),

    dcc.Markdown(children=markdown_text_middle ),

    html.Table(children = [html.Tr([html.Th(string) for string in ['Score','Range','Low','High']]) ] +
                            [html.Tr([html.Th(string) for string in ['Polarity','-1 to 1','Negative emotion','Positive Emotion']]),
                            html.Tr([html.Th(string) for string in ['Subjectivity', '0 to 1', 'Objective', 'Subjective']])]
                           , className = 'u-full-width'),

    dcc.Markdown(children=markdown_text_below),
],className = 'container')

@app.callback(
    dash.dependencies.Output('test-top-1-polarity', 'figure'),
    [dash.dependencies.Input('1-or-10', 'value'), dash.dependencies.Input('pol-or-sub', 'value'),
     dash.dependencies.Input('time-slider','value'),
     dash.dependencies.Input('series-plot', 'values')])
def update_figure(oneORten,polORsub,timevalue,plottedseries):
    #dictionary to tranlate the value of the time slider to a number of days
    time_dict = { 5:1, 4:3, 3:7, 2:14, 1:30}
    days_display = time_dict[timevalue]

    if days_display > days_recorded:
        days_display = days_recorded

    cutoff_date = time_max - datetime.timedelta(days=days_display)

    binary_plot = lambda x: (datetime.datetime.strptime(x, time_string) >= cutoff_date)

    slider_plotted_df = df[df['query_time'].map(binary_plot)]

    #Generate the list to be used in the series plotting
    plot_list = [str(plottedseries[x]) + '_' for x in range(0,len(plottedseries))]

    if oneORten=='top1':
        number = 1
    else:
        number = 10
    if polORsub=='pol':
        pre = 'pol'
        full_word = 'Polarity'
    else:
        pre = 'sub'
        full_word = 'Subjectivity'
    iterated = [x + str(number) + '_' + pre for x in plot_list]
    traces = [
            go.Scatter(
                x=slider_plotted_df['query_time'],
                y=slider_plotted_df.ix[:,i ],
                text=slider_plotted_df[i.split('_')[0] + '_1_head'],
                mode='lines',
                opacity=0.7,
                name=i.split('_')[0]
            ) for i in iterated
        ]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': str(full_word)},
            title= str(full_word) + ' of Top ' + str(number) + ' article(s) by Social Media',
            hovermode='closest')
    }

app.css.append_css({
   'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    #TODO: Make the CSS Style sheet make the webpage have a maximum width so it doesnt look weird on really wide monitors.
})

if __name__ == '__main__':
    app.run_server(debug=True)