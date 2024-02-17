import dash
import ipaddress
from dash import dcc, Input, Output, State
from dash import html
from dash_bootstrap_components import Modal
import dash_bootstrap_components as dbc
import serial.tools.list_ports
import powertek_RTD_v3 as mc361_serial
import powertek_RTD_eth_v1 as mc361_eth

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Get list of available serial ports
ports = [p.device for p in serial.tools.list_ports.comports()]

app.layout = dbc.Container([
    html.Br(),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    ),

    # dbc.Modal(
    #     id="modal",
    #     is_open=False,
    #     children=["Test is already running..."]),

    dbc.Card([dbc.CardHeader(html.H5("Powertek MC361 - Temperature simulation")),
              dbc.Form([
                  dbc.CardGroup([
                      dbc.Checklist(style={"margin-left": "30px",
                                           "margin-top": "10px"},
                                    options=[{"label": "Include test", "value": 1, }],
                                    value=[1],
                                    id="include-test",
                                    switch=True,
                                    ),
                  ]),
                  html.Br(),

                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Interface :",
                                                style={"margin-left": "30px"}), width=4),
                              dbc.Col(
                                  dcc.Dropdown(
                                      id="interface", clearable=False,
                                      options=[
                                          {"label": "Ethernet", "value": "ethernet"},
                                          {"label": "Serial", "value": "serial"},
                                      ],
                                      value="ethernet",
                                  ), width=5)
                          ]),
                      ]),
                      dbc.Col([

                          dbc.CardGroup([
                              dbc.Col(dbc.Label("STATUS:", ), width=2),
                              dbc.Col(
                                  html.B("Waiting...", id='live-update-text',
                                         style={"margin-left": "10px", }), width=8)
                          ]),

                      ], ),
                  ], ),

                  html.Br(),

                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Serial Port:",
                                                style={"margin-left": "30px", }),
                                      width=4),
                              dbc.Col(dcc.Dropdown(id="serial-port", clearable=False,
                                                   options=[{"label": p, "value": p} for p
                                                            in ports], ), width=8)
                          ]),
                      ], ),
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(
                                  dbc.Label("Baud Rate:", style={"margin-left": "30px"}),
                                  width=7),
                              dbc.Col(dcc.Dropdown(id="baud-rate", value=9600,
                                                   clearable=False,
                                                   options=[
                                                       {"label": "4800", "value": 4800},
                                                       {"label": "9600", "value": 9600},
                                                       {"label": "19200", "value": 19200},
                                                       {"label": "38400", "value": 38400},
                                                       {"label": "57600", "value": 57600},
                                                       {"label": "115200",
                                                        "value": 115200}, ], ), width=3)
                          ]),
                      ], ),
                  ]),
                  html.Br(),

                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(
                                  dbc.Label("IP Address:", style={"margin-left": "30px"}),
                                  width=4),
                              dbc.Col(
                                  dbc.Input(id="ip", type="text", value="192.168.1.10", ),
                                  width=5),
                          ]),
                      ]),
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Test cycles:",
                                                style={"margin-left": "30px", }),
                                      width=7),
                              dbc.Col(
                                  dbc.Input(id="test-cycles", type="number", min=1,
                                            max=100, step=1, value="1", ),
                                  width=3),
                          ]),
                      ]),
                  ]),
                  html.Br(),

                  dbc.Row([
                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Min Temperature (C):", ),
                                      style={"margin-left": "30px", }, width=7),
                              dbc.Col(
                                  dbc.Input(id="min-temp", type="number", value="-30", ),
                                  width=3),
                          ]),
                      ]),

                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Max Temperature (C):",
                                                style={"margin-left": "30px", }
                                                ), width=7),
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
                                                ), style={"margin-left": "30px"},
                                      width=7),
                              dbc.Col(
                                  dbc.Input(id="time-interval", type="number", value="10",
                                            min=1
                                            ), width=3),
                          ]),
                      ]),

                      dbc.Col([
                          dbc.CardGroup([
                              dbc.Col(dbc.Label("Step interval (C):",
                                                style={"margin-left": "30px", }
                                                ), width=7),
                              dbc.Col(
                                  dbc.Input(id="step-interval", type="number", value="10",
                                            min=1
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

], style={"width": "755px"})


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
    Output("start-test", "disabled"),
    [Input("interface", "value"),
     Input("serial-port", "value"),
     Input("ip", "value"),
     Input("min-temp", "value"),
     Input("max-temp", "value"),
     Input("time-interval", "value"),
     Input("step-interval", "value"),
     Input("test-cycles", "value"),
     Input("live-update-text", "children"), ],
)
def disable_start(interface, serial_port, ip, min_temp, max_temp, time_interval,
                  step_interval, test_cycles, live_update_text):
    if interface == "serial" and not serial_port:
        return True
    if interface == "ethernet" and not ip:
        return True
    if interface == "ethernet" and not validate_ip(ip):
        return True
    if min_temp is None or max_temp is None or time_interval is None or step_interval is None or test_cycles is None:
        return True
    if int(time_interval) < 1 or int(step_interval) < 1 or int(test_cycles) < 1:
        return True
    if int(min_temp) > int(max_temp):
        return True
    if live_update_text != "Waiting...":
        return True
    return False


@app.callback(
    Output("output", "children"),
    [Input("include-test", "value"),
     Input("interface", "value"),
     Input("serial-port", "value"),
     Input("baud-rate", "value"),
     Input("ip", "value"),
     Input("min-temp", "value"),
     Input("max-temp", "value"),
     Input("time-interval", "value"),
     Input("step-interval", "value"),
     Input("test-cycles", "value"), ]
)
def set_vars(include_test, interface, serial_port, baud_rate, ip, min_temp,
             max_temp, time_interval, step_interval, test_cycles):
    global SER_PORT
    global SER_BAUD
    global IP
    global MIN_TEMP
    global MAX_TEMP
    global TIME_INTV
    global STEP_INTV
    global CYCLES
    global INCLUDE_TEST
    global INTERFACE
    SER_PORT = serial_port
    SER_BAUD = int(baud_rate)
    IP = ip
    INCLUDE_TEST = include_test
    INTERFACE = interface
    if min_temp is not None:
        MIN_TEMP = int(min_temp)
    if max_temp is not None:
        MAX_TEMP = int(max_temp)
    if time_interval is not None:
        TIME_INTV = int(time_interval)
    if step_interval is not None:
        STEP_INTV = int(step_interval)
    if test_cycles is not None:
        CYCLES = int(test_cycles)

    # args = [include_test, interface, serial_port, baud_rate, ip, min_temp, max_temp,
    #         time_interval, step_interval, test_cycles]
    # print("updating vars:", args)


@app.callback(
    Output("start-test", "value"),
    [dash.dependencies.Input("start-test", "n_clicks"), ]
)
def run_test(n_clicks, ):
    global CYCLES
    global STATUS
    if n_clicks and INCLUDE_TEST:
        while CYCLES >= 1:
            STATUS = f"Running - cycles remaining : {CYCLES}"
            if INTERFACE == "serial":
                print("serial")
                mc361_serial.run_temp_test(SER_PORT, SER_BAUD, MIN_TEMP, MAX_TEMP,
                                           TIME_INTV, STEP_INTV)
            elif INTERFACE == "ethernet":
                print("ethernet")
                mc361_eth.run_temp_test(IP, 23, MIN_TEMP, MAX_TEMP,
                                        TIME_INTV, STEP_INTV)
            CYCLES -= 1
        CYCLES = 1
        STATUS = "Waiting..."
        return "Waiting..."
    else:
        return dash.no_update


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_status(n):
    return STATUS


# @app.callback(
#     Output("modal", "is_open"),
#     [Input("start-test", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, is_open):
#     print(STATUS)
#     if STATUS != "Waiting...":
#         print("STATUS is waiting")
#         if n1:
#             return not is_open
#         return is_open


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


SER_PORT = ""
SER_BAUD = 9600
IP = "192.168.1.10"
MIN_TEMP = -30
MAX_TEMP = 70
TIME_INTV = 10
STEP_INTV = 10
CYCLES = 1
INTERFACE = "ethernet"
STATUS = "Waiting..."
INCLUDE_TEST = False

if __name__ == "__main__":
    app.run_server(debug=True)
