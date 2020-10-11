
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

################
# Logo
################
SKYWEATHER2_LOGO = "https://www.switchdoc.com/SkyWeatherNoAlpha.png"



################
# Navbar
################
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SkyWeather Status", href="/status_page")),
            dbc.NavItem(dbc.NavLink("Weather", href="/weather_page")),
            dbc.NavItem(dbc.NavLink("Indoor T/H", href="/indoorth")),
            dbc.NavItem(dbc.NavLink("Logs", href="/log_page")),
            dbc.NavItem(dbc.NavLink("Documentation", href="https://shop.switchdoc.com/products/skyweather2-raspberry-pi-based-weather-station-kit-for-the-cloud")),
                ],
                id='navbar',
                brand="SkyWeather2",
                brand_href="#",
                color="primary",
                dark=True,

    )
    return navbar

def Logo():
    logo = html.Img(src=SKYWEATHER2_LOGO, height=100, style={'margin' :'20px'})
    return logo



