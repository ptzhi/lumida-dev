###############################################################################
# App Page
###############################################################################

import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# local
from data_master import*
import fig_format
import fig_plot


##############################################################################
# INITIALIZE DASH PAGE
##############################################################################
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
# # app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE, dbc_css],use_pages=True)
# load_figure_template('SLATE')

dash.register_page(
    __name__,
    path='/',
    title='Lumida - Crypto Index',
)

##############################################################################
# SET UP - REQUIRED VARIABLES
##############################################################################
# for buttons
trailing_dropdown = ['30d', '60d' ,'90d', '180d', '360d']
rolling_dropdown = ['1d', '3d' ,'5d', '7d', '10d']
ob_threshold_dropdown = ['1','2', '3', '4']
os_threshold_dropdown = ['-1', '-2', '-3', '-4']

coins_list = list(coin_price.columns)


# blank figure for initial load - temporary workaround
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', )
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig

##############################################################################
# DBC Components
##############################################################################

_FIXED = {
    "position": "fixed",
    "top":  '11em',
    "left": '1em',
    "bottom": 0,
    'font-size':'13px'

}

datepicker_range = dbc.Row(
    [
        dbc.Label("Date Range:"),
        dcc.DatePickerRange(
            min_date_allowed=coins_dict['btc'].time.iloc[0],
            max_date_allowed=coins_dict['btc'].time.iloc[-1],
            initial_visible_month=coins_dict['btc'].time.iloc[-1],
            start_date=coins_dict['btc'].time.iloc[-730],
            end_date=coins_dict['btc'].time.iloc[-1],
            number_of_months_shown=3,
            id="date-picker-range",
            with_portal=True,
            style={'font-size':'13px'}
        ),
    ],
)

dropdown_trailing = dbc.Row(
    [
        dbc.Label("Spread Trailing:"),
        dcc.Dropdown(
            trailing_dropdown,
            trailing_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="trailing",
            style={'font-size':'13px'}
        ),
    ],
    className='mt-4'
)

cap_input = html.Div(
    [
        html.P("Min cap (bn)"),
        dbc.Input(
        	id="min-cap",
         	type="number", 
          	placeholder='input number',
           	value=5,
            debounce=True,
            style={'font-size':'13px'}
        ),
        html.P("Max cap (bn)"),
        dbc.Input(
        	id="max-cap",
         	type="number", 
         	placeholder='input number',
         	value=500,
          	debounce=True,
           	style={'font-size':'13px'}
        ),
    ],
    className='mt-4'
)

dropdown_rolling = dbc.Row(
    [
        dbc.Label("Rolling ZScore:"),
        dcc.Dropdown(
            rolling_dropdown,
            rolling_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="rolling",
            style={'font-size':'13px'}
        ),
    ],
    className='mt-4'
)

zscore_input = html.Div(
    [
        html.P("OB threshold"),
        dbc.Input(
        	id="obthreshold",
         	type="number", 
          	placeholder='input number',
           	value=2,
            debounce=True,
            style={'font-size':'13px'}
        ),
        html.P("OS threshold"),
        dbc.Input(
        	id="osthreshold",
         	type="number", 
         	placeholder='input number',
         	value=-2,
          	debounce=True,
           style={'font-size':'13px'}
        ),
    ],
    className='mt-4'
)

# dropdown_ob_threshold = dbc.Row(
#     [
#         dbc.Label("Apply OB Threshold:"),
#         dcc.Dropdown(
#             ob_threshold_dropdown,
#             ob_threshold_dropdown[1],
#             clearable=False,
#             maxHeight=400,
#             id="obthreshold",

#         ),
#     ],
#     className='mt-4'
# )

# dropdown_os_threshold = dbc.Row(
#     [
#         dbc.Label("Apply OS Threshold:"),
#         dcc.Dropdown(
#             os_threshold_dropdown,
#             os_threshold_dropdown[1],
#             clearable=False,
#             maxHeight=400,
#             id="osthreshold",

#         ),
#     ],
#     className='mt-4'
# )

dropdown_coins = html.Div(
    [
        dbc.Label("Select Coin:"),
        dcc.Dropdown(
        	coins_list,
            'btc',
            placeholder="Select coin",
            maxHeight=500,
            multi=False,
            id="coins",
            clearable=False,
        ),
    ],
    className='mt-4'

)

table_of_contents = dbc.Row(
    [
        dbc.Label("Jump To Chart:", className='lead'),
        dbc.Nav(
            [
                dbc.NavLink("Test", href="#graph-spread-index",  external_link=True, active="exact"),
                # dbc.NavLink("Transactions", href="#graph-tx", external_link=True, active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='mt-4'
)


sidebar = dbc.Col(
    [
        datepicker_range,
        cap_input,
        dropdown_trailing,
        dropdown_rolling,
        zscore_input,
        # dropdown_ob_threshold,
        # dropdown_os_threshold,
        dropdown_coins,
        # table_of_contents,
        # options_checklist,
    ],
    style=_FIXED,
    width=1,
)

###############################################################################
# DASH APP LAYOUT
###############################################################################

layout = dbc.Container(
    [
        dbc.Col(
            [
                sidebar,
            ],
            className='d-none d-lg-block',
            width=1,
        ),
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # dbc.Label(
                                #     [
                                #         'Crypto Cap-weighted Index 60dma Spread'
                                #     ],
                                #     className='mt-4'
                                # ),
                                dcc.Graph(
                                    id='graph-spread-index',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}

                                ),
                            ],
                            className='border border-light rounded-3 mt-4',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-index-overbought',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 mt-4',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-index-oversold',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 mt-4',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-coin-spy-price',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}

                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-ma-coin',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-drawdown-coin',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-obos-coin',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-ob-coin-summary',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-os-coin-summary',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-macd-sma',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-macd-sma-eqv-shorting',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-macd-sma-over',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-macd-sma-under',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
            ],
            # className='flex-fill',
            # width=12,
        ),
    ],
    # fluid=True,
    className='dbc d-flex',
)


###############################################################################
# CALLBACKS - PLOTS
###############################################################################
@callback(
    Output("graph-spread-index", "figure"),
    Output("graph-table-index-overbought", "figure"),
    Output("graph-table-index-oversold", "figure"),
    Output("graph-coin-spy-price", "figure"),
    Output("graph-ma-coin", "figure"),
    Output("graph-drawdown-coin", "figure"),
    Output("graph-obos-coin", "figure"),
    Output("graph-table-ob-coin-summary", "figure"),
    Output("graph-table-os-coin-summary", "figure"),
    Output("graph-macd-sma", "figure"),
    Output("graph-macd-sma-eqv-shorting", "figure"),
    Output("graph-table-macd-sma-over", "figure"),
    Output("graph-table-macd-sma-under", "figure"),
    Input('coins','value'),
    Input('trailing','value'),
    Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
    Input('min-cap','value'),
    Input('max-cap','value'),
    Input('rolling','value'),
    Input('obthreshold','value'),
    Input('osthreshold','value'),
)
def graph(coin, trailing, start_date, end_date, min_cap, max_cap, rolling, obthreshold, osthreshold):
    return (
        fig_plot.plot_spread_index(trailing, start_date, end_date,min_cap, max_cap),
        fig_plot.plot_table_index_overbought(trailing, start_date, end_date, min_cap, max_cap),
        fig_plot.plot_table_index_oversold(trailing, start_date, end_date, min_cap, max_cap),
        fig_plot.plot_coin_spy_price(coin,trailing, start_date, end_date),
        fig_plot.plot_ma_coin(coin, trailing, start_date, end_date),
        fig_plot.plot_drawdown_coin(coin, trailing, start_date, end_date),
        fig_plot.plot_spread_coin_index(coin,trailing, start_date, end_date),
        fig_plot.plot_table_overbought_coin_summary(coin,trailing, start_date, end_date, rolling, obthreshold),
        fig_plot.plot_table_oversold_coin_summary(coin,trailing, start_date, end_date, rolling, osthreshold),
        fig_plot.plot_macd_sma(coin, start_date, end_date),
        fig_plot.plot_macd_sma_eqv(coin, start_date, end_date),
        fig_plot.plot_table_macd_sma_over_summary(coin, start_date, end_date),
        fig_plot.plot_table_macd_sma_under_summary(coin, start_date, end_date)
    )
