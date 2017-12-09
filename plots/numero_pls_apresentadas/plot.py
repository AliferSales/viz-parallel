import pandas as pd
import plotly.graph_objs as go
from plots.numero_pls_apresentadas.get_raw_data import output
import imp



def draw_plot_1(input):

    periodo = input['tempo-numero']

    raw_data = imp.load_source('info', 'plots/numero_pls_apresentadas/get_raw_data.py').output['raw_data']

    raw_data['dataInicio'] = pd.to_datetime(raw_data['dataInicio'])

    df = raw_data[raw_data['dataInicio'] >= str(periodo[0])]
    df = df[df['dataInicio'] <= str(periodo[1])]

    print(raw_data.columns)

    anos = df['dataInicio'].dt.year
    qtde = df['numero_pls']

    trace = [go.Bar(
        y=qtde,
        x=anos,
        opacity=0.75,
        text=['Qtde: {}<br>Ano: {}'.format(i, j) for i, j in zip(qtde, anos)],
        hoverinfo='text',
        name='Ano',
        marker=dict(
            color='#2DA37D'
        ),
        showlegend=False
    )
    ]

    layout = go.Layout(
        xaxis=dict(title='Anos'),
        yaxis=dict(title='Número de PLs')
    )

    figure = dict(data=trace, layout=layout)

    return figure

output = {"plot": draw_plot_1}