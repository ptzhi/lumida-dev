####################################################################
# LUMIDA DASHBOARDS
# 2023/01/18
####################################################################

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

###############################################################################
# INITIALIZE BOOTSTRAP THEMES
###############################################################################
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"

app = Dash(__name__,external_stylesheets=[dbc.themes.LUX], use_pages=True)

# for pushing to Heroku with gunicorn:
server = app.server

###############################################################################
# APP LAYOUT
###############################################################################
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(dbc.NavLink("OVERVIEW", href="/", className='ms-4')),
        dbc.NavItem(dbc.NavLink("SPREAD", href="/spread", className='ms-4')),
        dbc.NavItem(dbc.NavLink("MULTICOIN", href="/multicoin", className='ms-4')),
        # dbc.NavItem(dbc.NavLink("test", href="/trend")),
    ],
    brand="LUMIDA - DEV",
    brand_href="#",
    links_left=True,
    color="light",
    # dark=True,
    fixed='top',
    fluid=True,
    style = {
        "height": '80px'
    }
)

app.title = 'Lumida Dashboard'

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                navbar,
            ],
            # style={'left':0},
            # className='m-4',

        ),
        dbc.Row(
            [
            	dash.page_container
            ],
            style={'padding-top':'65px'},
            className='m-4',
        ),
    ],
    fluid=True,
    # style={'background-color': 'rgb(252, 252, 252)'},
    # className='col-xl-8',
)

if __name__ == '__main__':
	app.run_server(debug=True)
