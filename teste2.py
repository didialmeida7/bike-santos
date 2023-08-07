from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

file_paths = ["BikeSantos_2022_Simp.csv", "BikeSantos_2018_Simp.csv", "BikeSantos_2019_Simp.csv", "BikeSantos_2020_Simp.csv", "BikeSantos_2021_Simp.csv"]
dfs = [pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path) for file_path in file_paths]
df = pd.concat(dfs, ignore_index=True)

df.drop(['Nascimento', 'País', 'Cidade', 'UF', 'Data de Cadastro', 'IdJornada',
         'Projeto', 'AreaEstacaoRetirada', 'EnderecoEstacaoRetirada', 'Meio de Retirada',
         'AreaEstacaoDevolucao', 'EnderecoEstacaoDevolucao'], axis=1, inplace=True)

df.rename(columns={'EstacaoRetirada': 'Pontos', 'QuantidadeRetirada': 'Retiradas'}, inplace=True)

df_aggregated = df.groupby('Pontos', as_index=False)['Retiradas'].sum()

fig = go.Figure(data=[
    go.Bar(x=df_aggregated['Pontos'], y=df_aggregated['Retiradas'],
           marker=dict(color='rgba(0, 128, 0, 0.6)'))
])

fig.update_traces(textposition='inside', textfont_size=14)
fig.update_layout(
    title='Quantidade de Retiradas de Bicicletas nos Pontos',
    xaxis_title='Estação de Retirada',
    yaxis_title='Total de Retiradas',
    hovermode='x',
    paper_bgcolor='white',
    plot_bgcolor='white'
)

df_aggregated = df.groupby('DiaSemana', as_index=False)['Retiradas'].sum()
df_aggregated['DiaSemana'] = pd.Categorical(df_aggregated['DiaSemana'],
                                            categories=['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
                                            ordered=True)
df_aggregated.sort_values('DiaSemana', inplace=True)

fig2 = px.line(df_aggregated, x='DiaSemana', y='Retiradas', color='DiaSemana',
               line_shape='linear', labels={'DiaSemana': 'Dia da Semana', 'Retiradas': 'Quantidade de Retiradas'},
               color_discrete_sequence=px.colors.sequential.algae)

fig2.update_traces(mode='lines+markers', hovertemplate=None)


estacoes_options = [{'label': estacao, 'value': estacao} for estacao in df['Pontos'].unique()]
menu_estacoes = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Selecione a estação:", html_for="dropdown_estacoes"),
            dcc.Dropdown(
                id="dropdown_estacoes",
                options=estacoes_options,
                value=df['Pontos'].iloc[0],  # Valor inicial
            ),
        ]
    )
)

app.layout = html.Div(
    children=[
        html.H1(children='Quantidade de Retiradas', style={'color': '#000000', 'text-align': 'center'}),
        html.H2(children='Gráfico com a Quantidade de Retiradas de Bicicletas nos Pontos',
                style={'color': '#000000'}),
        dcc.Graph(
            id='retirada-estacoes',
            figure=fig
        ),
        html.H2(children='Gráfico com a Quantidade de Retiradas de Bicicletas por Dia da Semana',
                style={'color': '#000000'}),
        dcc.Graph(
            id='retirada-dias',
            figure=fig2
        ),
        html.H2(children='Gráfico com a Quantidade de Viagens por Estação',
                style={'color': '#000000'}),
        menu_estacoes,
        dcc.Graph(id='viagens-estacao'),
    ],
    style={
        'background-color': '#f0f0f0',
        'padding': '50px',
        'font-family': 'Arial, sans-serif',
        'max-width': '800px',
        'margin': '0 auto'
    }
)

# Callback para atualizar o gráfico com base na estação selecionada no menu
@app.callback(
    Output('viagens-estacao', 'figure'),
    [Input('dropdown_estacoes', 'value')]
)
def update_station_graph(selected_station):
    df_filtered = df[df['Pontos'] == selected_station]
    if not df_filtered.empty and "BikeSantos_2022_Simp.csv" in file_paths:
        fig_station = go.Figure(data=[
        go.Bar(x=df_filtered['DiaSemana'], y=df_filtered['Retiradas'],
               marker=dict(color='rgba(0, 128, 0, 0.6)'))
    ])
    fig_station.update_traces(textposition='inside', textfont_size=14)
    fig_station.update_layout(
        title=f'Quantidade de Viagens na Estação "{selected_station}"',
        xaxis_title='Dia da Semana',
        yaxis_title='Total de Viagens',
        hovermode='x',
        paper_bgcolor='white',
        plot_bgcolor='white'
    )



    return fig_station


if __name__ == '__main__':
    app.run_server(debug=True)
