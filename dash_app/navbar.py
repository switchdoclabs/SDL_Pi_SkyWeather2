
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc



################
# Navbar
################
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SkyWeather Status", href="/status_page")),
            dbc.NavItem(dbc.NavLink("Weather", href="/weather_page")),
            dbc.NavItem(dbc.NavLink("Indoor T/H", href="/indoorth")),
            dbc.NavItem(dbc.NavLink("SkyCam", href="/skycam_page")),
            dbc.NavItem(dbc.NavLink("WS Air Quality", href="/aqi_page")),
            dbc.NavItem(dbc.NavLink("WS Lightning", href="/lightning_page")),
            dbc.NavItem(dbc.NavLink("WS AfterShock", href="/aftershock_page")),
            dbc.NavItem(dbc.NavLink("WS Radiation", href="/radiation_page")),
            dbc.NavItem(dbc.NavLink("WS SolarMAX2", href="/solarmax_page")),
            dbc.NavItem(dbc.NavLink("Logs", href="/log_page")),
                ],
                id='navbar',
                brand="SkyWeather2",
                brand_href="#",
                color="primary",
                dark=True,

    )
    return navbar

def Logo(app):
    logo = html.Img(src=app.get_asset_url('SkyWeather2Logo.png'), height=100, style={'margin' :'20px'})
    return logo



