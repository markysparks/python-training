import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import serial.tools.list_ports

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Get list of available serial ports
ports = [p.device for p in serial.tools.list_ports.comports()]

app.layout = dbc.Container([
    html.Br(),

    dbc.Card([dbc.CardHeader(html.H5("Powertek MC361 - Temperature simulation")),

              # html.H1("Test Configuration"),

              dbc.Form([

                  dbc.CardGroup([
                      dbc.Checklist(style={"margin-left": "30px",
                                           "margin-top": "20px"},
                                    options=[{"label": "Include test", "value": 1, }],
                                    value=[1],
                                    id="include-test",
                                    switch=True,
                                    ),
                  ]),
                  html.Br(),

                  dbc.CardGroup([
                      dbc.Label("Interface :",
                                style={"margin-right": "30px", "margin-left": "30px"}),
                      dcc.Dropdown(style={"width": "50%", "margin-left": "5px"},
                                   id="interface",
                                   options=[
                                       {"label": "Ethernet", "value": "ethernet"},
                                       {"label": "Serial", "value": "serial"},
                                   ],
                                   value="ethernet",
                                   ),
                  ]),
                  html.Br(),

                  dbc.CardGroup([
                      dbc.Label("Serial Port:",
                                style={"margin-right": "30px", "margin-left": "30px", }),
                      dcc.Dropdown(id="serial-port",
                                   style={"width": "70%"},
                                   options=[{"label": p, "value": p} for p in ports]),
                  ]),
                  html.Br(),

                  dbc.CardGroup([
                      dbc.Label("IP Address:",
                                style={"margin-right": "30px", "margin-left": "30px"}),
                      dbc.Input(id="ip", type="text", value="192.168.1.10",
                                style={"margin-right": "30px", "margin-left": "5px", "width": "22%"}),
                  ]),
                  html.Br(),

                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Min Temp (C):",
                                                ), style={"margin-left": "30px"}, width=6),
                              dbc.Col(dbc.Input(id="min-temp", type="number", value="-30",
                                                ), width=3),
                          ],),
                      ]),

                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Max Temp (C):",
                                                ), width=6),
                              dbc.Col(dbc.Input(id="max-temp", type="number", value="70",
                                                ), width=3),
                          ]),
                      ]),
                  ]),
                  html.Br(),
                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Time interval (secs):",
                                                ), style={"margin-left": "30px"}, width=6),
                              dbc.Col(
                                  dbc.Input(id="time-interval", type="number", value="10",
                                            ), width=3),
                          ]),
                      ]),

                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Number of cycles :",
                                                ), width=6),
                              dbc.Col(dbc.Input(id="num-cycles", type="number", value="1",
                                                ), width=3),
                          ]),
                      ]),

                  ]),
                  html.Br(),
              ]),
    ]),

    html.Br(),
    dbc.Button("Start selected tests", color="primary", id="start-test",
               style={"width": "30%"}),

    html.Div(id="output",
             style={"margin-left": "30px", "margin-bottom": "20px", "margin-top": "10px",
                    "width": "20%"}),

],  style={"width": "700px"})


@app.callback(
    dash.dependencies.Output("serial-port", "disabled"),
    [dash.dependencies.Input("interface", "value")],
)
def disable_serial_port(interface):
    if interface == "serial":
        return False
    else:
        return True


@app.callback(
    dash.dependencies.Output("ip", "disabled"),
    [dash.dependencies.Input("interface", "value")],
)
def disable_ip(interface):
    if interface == "ethernet":
        return False
    else:
        return True


@app.callback(
    dash.dependencies.Output("output", "children"),
    [
        dash.dependencies.Input("start-test", "n_clicks"),
        dash.dependencies.Input("include-test", "value"),
        dash.dependencies.Input("interface", "value"),
        dash.dependencies.Input("serial-port", "value"),
        dash.dependencies.Input("ip", "value"),
        dash.dependencies.Input("min-temp", "value"),
        dash.dependencies.Input("max-temp", "value"),
        dash.dependencies.Input("time-interval", "value"),
        dash.dependencies.Input("num-cycles", "value"),
    ]
)
def run_test(n_clicks, include_test, interface, serial_port, ip, min_temp, max_temp,
             time_interval, num_cycles):
    if n_clicks and include_test:
        args = [interface, serial_port, ip, min_temp, max_temp, time_interval, num_cycles]
        print("Running test with arguments:", args)
        return html.Div(f"Running test with arguments: {args}")
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
