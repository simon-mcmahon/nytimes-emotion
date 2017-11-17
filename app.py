import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_csv('nytimes_dash_output.csv')

markdown_text_head= '''

## New York Times Article Sentiment Analysis by Social Media

###### Do different social media platforms have different "flavours" of content which people share on them?  


'''
markdown_text_below = '''

#### What is going on here?

The New York times publishes a list of the top 10 shared articles across Facebook, Twitter, Email and Most Viewed (on nytimes.com) [here](http://www.nytimes.com/most-popular.html). The page updates every 15 minutes.

A web crawling script was set up to check the top 10 articles every 15 minutes, extract the headline and the text, pass it through an NLP sentiment analysis neural net and plot the key attributes for you here, updated in real time.

#### Meaning of the scores

##### Polarity 

**A number from -1.0 to 1.0 where negative values are associated with negative emotions and positive scores with positive emotions.**

##### Subjectivity

**A number from 0.0 to 1.0 where 0.0 is very objective and 1.0 is very subjective.**

#### Controlling the graph

##### Radio Buttons

* Clicking on each set of buttons changes the graph parameters.
    * **Top 1** displays the score of only the top headline
    * **Top 10** displays the averaged score of the top 10 popular headlines
    * **Polarity** changes the y-axis to display the polarity value.
    * **Subjectivity** changed the y-axis to display the subjectivity value.  
  
##### Graph Manipulation

* Hover over a place on the graph to see the headline of the most popular article for context. 
* Zoom to a region by clicking and dragging. 
* To zoom back out, double click on the graph.  

##### Crafted by [Simon McMahon](https://www.linkedin.com/in/simon-mcmahon/)

'''

app.title='NY times Sentiment Analysis'

Radio_button_font_size = '150%'

app.layout = html.Div([
    dcc.Markdown(children=markdown_text_head),
    html.Div([
        dcc.RadioItems(
            options=[
                {'label': 'Top 1', 'value': 'top1'},
                {'label': 'Top 10 Average', 'value': 'top10'},
            ],
            value='MTL',
            id = '1-or-10',
            labelStyle={'display': 'inline-block'}
        )],style={'width': '48%','display': 'inline-block','fontSize': Radio_button_font_size}),

    html.Div([
        dcc.RadioItems(
            options=[
                {'label': 'Polarity', 'value': 'pol'},
                {'label': 'Subjectivity', 'value': 'sub'},
            ],
            value='MTL',
            id='pol-or-sub',
            labelStyle={'display': 'inline-block'}
        )],style={'width': '48%','float': 'center', 'display': 'inline-block','fontSize': Radio_button_font_size}),
    dcc.Graph(id='test-top-1-polarity'),
    dcc.Markdown(children=markdown_text_below),
])

@app.callback(
    dash.dependencies.Output('test-top-1-polarity', 'figure'),
    [dash.dependencies.Input('1-or-10', 'value'), dash.dependencies.Input('pol-or-sub', 'value')])
def update_figure(oneORten,polORsub):
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
    iterated = [x + str(number) + '_' + pre for x in ['fb_','twitter_','email_','viewed_']]
    traces = [
            go.Scatter(
                x=df['query_time'],
                y=df.ix[:,i ],
                text=df[i.split('_')[0] + '_1_head'],
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