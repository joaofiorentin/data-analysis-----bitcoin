import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar o dataset
file_path = r'C:/Users/João/Desktop/bitcoin/bd_bitcoin.csv'
bitcoin_data = pd.read_csv(file_path)

# Preparar os dados
bitcoin_data['Date'] = pd.to_datetime(bitcoin_data['Date'])
bitcoin_data['Daily Return'] = bitcoin_data['Close'].pct_change() * 100

# Iniciar o app Dash
app = dash.Dash(__name__)

# Layout com design mais limpo e organizado
app.layout = html.Div([
    html.H1("Análise Interativa do Bitcoin", style={'text-align': 'center', 'color': '#2e3d49', 'font-size': '36px', 'margin-top': '20px'}),
    
    # Dropdown para selecionar o tipo de preço
    html.Div([
        html.Label("Escolha o tipo de preço:", style={'font-size': '18px'}),
        dcc.Dropdown(
            id='price-type',
            options=[
                {'label': 'Abertura', 'value': 'Open'},
                {'label': 'Fechamento', 'value': 'Close'},
                {'label': 'Alta', 'value': 'High'},
                {'label': 'Baixa', 'value': 'Low'}
            ],
            value='Close',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'padding': '20px'}),

    # Gráfico de séries temporais
    html.Div([
        dcc.Graph(id='time-series-chart'),
    ], style={'margin-top': '30px'}),

    # Análise de Distribuição de Retornos Diários
    html.Div([
        html.H3("Distribuição de Retornos Diários (%)", style={'text-align': 'center', 'margin-top': '30px'}),
        dcc.Graph(id='return-distribution'),
    ], style={'margin-top': '30px'}),

    # Mapa de Correlação entre Variáveis
    html.Div([
        html.H3("Correlação entre Variáveis", style={'text-align': 'center', 'margin-top': '30px'}),
        dcc.Graph(id='correlation-heatmap'),
    ], style={'margin-top': '30px'}),

    # Resumo Estatístico
    html.Div([
        html.H3("Resumo Estatístico", style={'text-align': 'center', 'margin-top': '30px'}),
        html.Div(id='summary-stats', style={'width': '80%', 'margin': 'auto', 'text-align': 'center', 'font-size': '18px'})
    ], style={'margin-top': '30px'})
])

# Callback para atualizar o gráfico de séries temporais
@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('price-type', 'value')]
)
def update_time_series_chart(price_type):
    fig = px.line(
        bitcoin_data, 
        x='Date', y=price_type, 
        title=f"Preço do Bitcoin: {price_type}",
        labels={'Date': 'Data', price_type: 'Preço'},
        template="plotly_dark"
    )
    return fig

# Callback para atualizar o gráfico de distribuição de retornos diários
@app.callback(
    Output('return-distribution', 'figure'),
    Input('price-type', 'value')
)
def update_return_distribution(price_type):
    fig = px.histogram(
        bitcoin_data, 
        x='Daily Return', nbins=50,
        title='Distribuição de Retornos Diários (%)',
        labels={'Daily Return': 'Retorno Diário (%)'},
        template="plotly_dark"
    )
    return fig

# Callback para atualizar o heatmap de correlação
@app.callback(
    Output('correlation-heatmap', 'figure'),
    Input('price-type', 'value')
)
def update_correlation_heatmap(price_type):
    correlation = bitcoin_data[['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']].corr()
    fig = px.imshow(
        correlation, 
        text_auto=True,
        title='Mapa de Correlação entre Variáveis',
        template="plotly_dark"
    )
    return fig

# Callback para atualizar o resumo estatístico
@app.callback(
    Output('summary-stats', 'children'),
    Input('price-type', 'value')
)
def update_summary_stats(price_type):
    stats = bitcoin_data[price_type].describe().round(2)
    return html.Table([
        html.Tr([html.Th("Métrica"), html.Th("Valor")])] + 
        [html.Tr([html.Td(index), html.Td(value)]) for index, value in stats.items()],
        style={'width': '50%', 'margin': 'auto', 'border': '1px solid black'}
    )

# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
