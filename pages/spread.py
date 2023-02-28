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
    path='/spread',
    title='Lumida - Spread',
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

# coin_list = [x for x in list(coins_dict.keys()) if x not in coin_del]

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
    'font-size':'15px'

}

datepicker_range = dbc.Row(
    [
        dbc.Label("Date Range:"),
        dcc.DatePickerRange(
            min_date_allowed=coins_dict['btc'].time.iloc[0],
            max_date_allowed=coins_dict['btc'].time.iloc[-1],
            initial_visible_month='2022-01-01',
            start_date='2011-01-01',
            end_date=coins_dict['btc'].time.iloc[-1],
            number_of_months_shown=1,
            id="date-picker-range",
            style={'font-size':'14px'}
        ),
    ],
)

dropdown_trailing = dbc.Row(
    [
        dbc.Label("Apply Trailing MA:"),
        dcc.Dropdown(
            trailing_dropdown,
            trailing_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="trailing",

        ),
    ],
    className='mt-4'
)

dropdown_rolling = dbc.Row(
    [
        dbc.Label("Apply Rolling ZScore:"),
        dcc.Dropdown(
            rolling_dropdown,
            rolling_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="rolling",

        ),
    ],
    className='mt-4'
)

dropdown_ob_threshold = dbc.Row(
    [
        dbc.Label("Apply OB Threshold:"),
        dcc.Dropdown(
            ob_threshold_dropdown,
            ob_threshold_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="obthreshold",

        ),
    ],
    className='mt-4'
)

dropdown_os_threshold = dbc.Row(
    [
        dbc.Label("Apply OS Threshold:"),
        dcc.Dropdown(
            os_threshold_dropdown,
            os_threshold_dropdown[1],
            clearable=False,
            maxHeight=400,
            id="osthreshold",

        ),
    ],
    className='mt-4'
)

dropdown_coins = html.Div(
    [
        dbc.Label("Search Coins:"),
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
        dropdown_trailing,
        dropdown_rolling,
        dropdown_ob_threshold,
        dropdown_os_threshold,
        dropdown_coins
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
                                    id='graph-log-price',
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
                                    id='graph-spread-price',
                                    # figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}

                                ),
                            ],
                            className='border border-light rounded-3',
                        ),
                    ],
                ),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             [
                #                 dcc.Graph(
                #                     id='graph-table-overbought-coin-summary',
                #                     # figure = blank_fig(),
                #                     style={'scroll-margin-top':'248px'},
                #                     config={'displayModeBar': False}
                                
                #                 ),
                #             ],
                #             className='border border-light rounded-3',
                #         ),
                #         dbc.Col(
                #             [
                #                 dcc.Graph(
                #                     id='graph-table-oversold-coin-summary',
                #                     figure = blank_fig(),
                #                     style={'scroll-margin-top':'248px'},
                #                     config={'displayModeBar': False}
                #                 ),
                #             ],
                #             className='border border-light rounded-3',
                #         ),
                #     ],
                # ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id='graph-table-overbought-coin',
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
                                    id='graph-table-oversold-coin',
                                    figure = blank_fig(),
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
    Output("graph-log-price", "figure"),
    Output("graph-spread-price", "figure"),
    Output("graph-table-overbought-coin", "figure"),
    Output("graph-table-oversold-coin", "figure"),
    # Output("graph-table-overbought-coin-summary", "figure"),
    # Output("graph-table-oversold-coin-summary", "figure"),
    Input('coins','value'),
    Input('trailing','value'),
    Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
    Input('rolling','value'),
    Input('obthreshold','value'),
    Input('osthreshold','value'),

)
def graph(coin, trailing, start_date, end_date, rolling, obthreshold, osthreshold):
    return (
        fig_plot.plot_log_price(coin,trailing, start_date, end_date),
        fig_plot.plot_spread_price(coin,trailing, start_date, end_date),
        fig_plot.plot_table_overbought_coin(coin,trailing, start_date, end_date, rolling, obthreshold),
        fig_plot.plot_table_oversold_coin(coin,trailing, start_date, end_date, rolling, osthreshold),
        # fig_plot.plot_table_overbought_coin_summary(coin,trailing, start_date, end_date, rolling, obthreshold),
        # fig_plot.plot_table_oversold_coin_summary(coin,trailing, start_date, end_date, rolling, obthreshold)
    )
