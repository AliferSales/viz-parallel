
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
from dash.dependencies import Input, Output
import yaml


from main_options.fluxo_tramitacao.callback import fluxo_tramitacao
from main_options.perfil_tempo_tramitacao.callback import perfil_tempo_tramitacao
from main_options.numero_pls_apresentadas.callback import numero_pls_apresentadas
from main_options.acumulado_pls_apresentadas.callback import acumulado_pls_apresentadas

from components import components

#  CONFIG APP

server = flask.Flask(__name__)
app = dash.Dash(name='app1', sharing=True, server=server, csrf_protect=False)


# CONSTANTS
options_properties = yaml.load(open('main_options/options_properties.yaml', 'r'))
options_functions = {'fluxo_tramitacao': fluxo_tramitacao,
                     'perfil_tempo_tramitacao': perfil_tempo_tramitacao,
                     'numero_pls_apresentadas': numero_pls_apresentadas,
                     'acumulado_pls_apresentadas': acumulado_pls_apresentadas
                     }
columns = 2

app.config.supress_callback_exceptions = True

#  ESTRUTURA APP

app.layout = html.Div([

# (1) Título
   html.Div([

               html.H1('Estrutura de tramitações',
                       style={'margin-top': '10',
                              'margin-bottom': '-5'})

       ],
       className='row'
   ),

   html.Hr(),

    html.Div([

        html.Div([

            html.P('Selecione o gráfico a ser mostrado:'),
            dcc.RadioItems(
                id='graph-selector',
                options=[{'label': option['full_name'],
                          'value': option['back_name']}
                         for option in options_properties],
                value=options_properties[0]['back_name'],
                labelStyle={'display': 'inline-block'}
            )
        ],
            className='six columns'
        ),
        ]
    ),

    html.Div(id='menu',
        className='ten columns offset-by-one'
    ),

    html.Div(
        id='output-container',
        className='ten columns offset-by-one'
    ),
    ]
)

def generate_ids(value, column):
    return "{value}-{column}".format(value=value, column=column)

@app.callback(Output('menu', 'children'),
              [Input('graph-selector', 'value')])
def update_menu(back_name):

    menus = []

    for opt in options_properties:
        if opt['back_name'] == back_name:
            for variables in opt['variables']:
                for column in range(columns):

                    kwargs = dict(id=generate_ids(variables['data_title'], column),
                                  className='five columns',
                                  raw_data=options_functions[back_name]['raw_data'],
                                  column_name=variables['column_name'],
                                  back_name=back_name,
                                  data_title=variables['data_title'],
                                  extra_options=variables['options'])

                    menus.append(components[variables['type']](kwargs=kwargs))
    print(menus)
    return menus


@app.callback(
    Output('output-container', 'children'),
    [Input('graph-selector', 'value')])
def display_controls(back_name):
    # Create a unique output container for each pair of dynamic controls
    return html.Div(
        [dcc.Graph(id=generate_ids(back_name, column),
                   className='six columns',
                   style={'text-align': 'center'}) for column in range(columns)])


def generate_output_callback(back_name):
    def print_exit(*values):

        print(values)

        return options_functions[back_name]['draw_plot_1'](values[0], values[1])

    return print_exit

for back_name in [o['value'] for o in app.layout['graph-selector'].options]:

    for column in range(columns):
        callback_input = []
        for opt in options_properties:
            if opt['back_name'] == back_name:
                for variables in opt['variables']:
                    callback_input.append(Input(generate_ids(variables['data_title'], column),
                                                'value'))

        app.callback(
            Output(generate_ids(back_name, column), 'figure'),
            callback_input)(
            generate_output_callback(back_name)
        )

#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def draw_plot_1(input1, input2, input3):
#
#    func = options_functions[input3]['draw_plot_1']
#    return func(input1, input2)



#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def draw_plot_1(input1, input2, input3):
#
#    func = options_functions[input3]['draw_plot_1']
#    return func(input1, input2)
#
#
#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def draw_plot_2(input1, input2, input3):
#
#    func = options_functions[input3]['draw_plot_1']
#    return func(input1, input2)
#
#
#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def draw_plot_diff(input1, input2, input3):
#
#    func = options_functions[input3]['draw_plot_diff']
#    return func(input1, input2)
#
#
#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def big_numbers_1(input1, input2, input3):
#
#    func = options_functions[input3]['big_numbers_1']
#    return func(input1, input2)
#
#
#@app.callback(Output('output', 'children'),
#              [Input('input-1', 'value'),
#               Input('input-2', 'value'),
#               Input('xaxis-type', 'value')])
#def big_numbers_2(input1, input2, input3):
#
#    func = options_functions[input3]['big_numbers_2']
#    return func(input1, input2)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server()

