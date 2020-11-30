import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import no_update
import pandas as pd

from loan_analytics import main
from loan_analytics import LoanImpacts
# setup app with stylesheets
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])

# Number of maximum loans
loan_num = 3

loanNum = dbc.FormGroup(
    [
        dbc.Label("Please choose the number of loans in your loan portfolio", size='lg', color='black-50'),
        dbc.RadioItems(
            options=[
                {"label": "1", "value": 1},
                {"label": "2", "value": 2},
                {"label": "3", "value": 3},
            ],
            value=1,
            id="loanNum-input",
            inline=True,
            style={'margin-left': '2px'},
        )
    ]
)

# Create loan table 
loan_table_df = main.compute_schedule(1.0, 1.0, 1.0, 1.0)
initial_table = pd.DataFrame(columns=loan_table_df.columns)
initial_table.loc[0] = '-'
loan_table = dash_table.DataTable(
    id='loan-table',
    columns=[{"name": i, "id": i} for i in loan_table_df.columns],
    data=initial_table.to_dict('records'),
    style_as_list_view=True
)

table_card = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        f"Click to show the amortization schedule",
                        color="link",
                        id=f"tableToggle-button",
                        style={"font-size":"20px"},
                        block=True
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(loan_table),
                id=f"collapse-table",
            ),
        ]
    )


# Create contribution table 
loan_impacts = LoanImpacts.LoanImpacts(principal=1, rate=1, payment=1, extra_payment=0, contributions=[0])
con_table_df = loan_impacts.compute_impacts()
con_table = dash_table.DataTable(
    id='con-table',
    columns=[{"name": i, "id": i} for i in con_table_df.columns],
    data=con_table_df.to_dict('records'),
    style_as_list_view=True
)

# con_table_card = dbc.Card(
#      [
#         dbc.FormGroup(
#             [
#                 con_table,
#             ]
#         )
#      ],
#      className="w-100 mb-3",
#      body=True
# )

con_table_card = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        f"Click to show the Contribution Table",
                        color="link",
                        id=f"conTableToggle-button",
                        style={"font-size":"20px"},
                        block=True
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(con_table),
                id=f"collapse-conTable",
            ),
        ]
    )

# Create loans portfolio
def make_item(i, d=False):
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H1(
                    dbc.Button(
                        f"Loan #{i}",
                        color="link",
                        id=f"loan-{i}-toggle",
                        disabled=d,
                        style={"font-size":"20px"}
                    )
                )
            ),
            dbc.Collapse(
                html.P(
                    [
                        html.Br(),
                        dbc.FormGroup(
                            [
                                dbc.Label("Please Enter the loan amount", size="md"),
                                dbc.InputGroup(
                                [   
                                    dbc.InputGroupAddon("$", addon_type="prepend"),
                                    dbc.Input(placeholder="Please Enter the loan amount", type="number", min=0, bs_size="md", inputMode="numeric", id=f'loan-input{i}'),
                                ]
                            ),
                            ],
                            className="mx-2"
                        ),
                        dbc.FormGroup(
                            [
                                dbc.Label("Please Enter the interest rate:", size="md"),
                                dbc.InputGroup(
                                [   
                                    dbc.Input(placeholder="Please Enter the interest rate", type="number", min=0, bs_size="md", inputMode="numeric", id=f'rate-input{i}'),
                                    dbc.InputGroupAddon("%", addon_type="append")
                                ]
                            ),
                            ],
                            className="mx-2"
                        ),
                        dbc.FormGroup(
                            [
                                dbc.Label("Please Enter the payment:", size="md"),
                                dbc.InputGroup(
                                [   
                                    dbc.InputGroupAddon("$", addon_type="prepend"),
                                    dbc.Input(placeholder="Please Enter the payment", type="number", min=0, bs_size="md", inputMode="numeric", id=f'payment-input{i}'),
                                ]
                            ),
                            ],
                            className="mx-2"
                        ),
                        dbc.FormGroup(
                            [
                                dbc.Label("Please Enter the extra payment:", size="md"),
                                dbc.InputGroup(
                                [   
                                    dbc.InputGroupAddon("$", addon_type="prepend"),
                                    dbc.Input(placeholder="Please Enter the extra payment", type="number", min=0, bs_size="md", inputMode="numeric", id=f'expayment-input{i}'),
                                ]
                            ),
                            ],
                            className="mx-2"
                        ),
                        dbc.ButtonGroup(
                            [
                            dbc.Button("Submit", outline=True, id=f"button-submit{i}", color="success", className="mr-1", n_clicks=0),
                            dbc.Button("Clear", outline=True, id=f"button-clear{i}", color="warning", className="mr-1", n_clicks=0)
                            ],
                            className="mx-2 mb-2"
                        )
                    ],
                    className="w-100 mb-3"
                ),
                id=f"collapse-{i}",
            ),
        ]
    )


# Create loan input options
loan_port = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Div(
                    [make_item(i) for i in range(1, loan_num+1)], className="accordion"
                    )
            ],
            className="mx-2"
        )
    ],
    className="w-100 mb-3",
    id='loanNum-card'
)

# Tab 1
loan  = dbc.Container(
    [
        dbc.Row(
            dbc.Col(loanNum)
            ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Please enter your Loans Portfolio", size='lg', color='black-50'),
                        loan_port
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Label("Your Result (Display after your submission)", size='lg', color='black-50'),
                        dbc.Card(
                            dbc.Jumbotron(
                                [
                                    html.P('Your Regular Payment', style={'textAlign': 'center', 'margin-top':'0px', "font-size":"18px", "color":'#A9A9A9', "font-weight":"bold"}),
                                    html.P('-', id="result-display4", style={"font-size":"30px", 'textAlign': 'center', "font-weight":"bold"}),
                                    html.Hr(className="my-1"),
                                    html.P('Estimated Time to Loan Term Termination', style={'textAlign': 'center', 'margin-top':'5px', "font-size":"18px", "color":'#A9A9A9', "font-weight":"bold"}),
                                    html.Div('-', id="result-display3", style={"font-size":"30px", 'textAlign': 'center', "font-weight":"bold"}),
                                    html.Hr(className="my-2"),
                                    html.P('Total Principal Paid', style={'textAlign': 'center', 'margin-top':'5px', "font-size":"18px", "color":'#A9A9A9', "font-weight":"bold"}),
                                    html.Div('-', id="result-display1", style={"font-size":"30px", 'textAlign': 'center', "font-weight":"bold"}),
                                    html.Hr(className="my-1"),
                                    html.P('Total Interest Paid', style={'textAlign': 'center', 'margin-top':'5px', "font-size":"18px", "color":'#A9A9A9', "font-weight":"bold"}),
                                    html.Div('-', id="result-display2", style={"font-size":"30px", 'textAlign': 'center', "font-weight":"bold"})
                                ],
                                style={'margin-bottom':'0px'}
                                ), 
                            )
                    ],
                )
            ]
            ),
        html.Br(),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                [
                    # dbc.Label("Below is the amortization schedule!", id='table-label', size='lg', color='black-50'),
                    table_card
                ]
             ),
        )
        
    ],
    id="tab1-container",
    style={"height": "100vh"}, 
    fluid=True
)

tab1_content = loan

# Tab 2
## sub tabs for number of contributors
ppltab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Person 1", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input1_1'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            dbc.ButtonGroup(
            [
                dbc.Button("Submit", outline=True, id=f"ppl-submit1", color="success", className="mr-1", n_clicks=0),
                dbc.Button("Clear", outline=True, id=f"ppl-clear1", color="warning", className="mr-1", n_clicks=0)
                ],
                className="mx-0 mb-2"
            ),
        ]
    ),
    className="mt-3",
)

ppltab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Person 1", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input2_1'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            html.Hr(),
            dbc.Label("Person 2", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input2_2'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            dbc.ButtonGroup(
            [
                dbc.Button("Submit", outline=True, id=f"ppl-submit2", color="success", className="mr-1", n_clicks=0),
                dbc.Button("Clear", outline=True, id=f"ppl-clear2", color="warning", className="mr-1", n_clicks=0)
                ],
                className="mx-0 mb-2"
            ),
        ]
    ),
    className="mt-3",
)

ppltab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("Person 1", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input3_1'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            html.Hr(),
            dbc.Label("Person 2", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input3_2'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            html.Hr(),
            dbc.Label("Person 3", className="card-text", color="warning"),
            dbc.FormGroup(
                [
                    dbc.Label("Please enter the contribution of this person", size="md"),
                    dbc.InputGroup(
                    [   
                        dbc.InputGroupAddon("$", addon_type="prepend"),
                        dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='pplloan-input3_3'),
                    ]
                    ),
                ],
                className="mx-0"
            ),
            dbc.ButtonGroup(
            [
                dbc.Button("Submit", outline=True, id=f"ppl-submit3", color="success", className="mr-1", n_clicks=0),
                dbc.Button("Clear", outline=True, id=f"ppl-clear3", color="warning", className="mr-1", n_clicks=0)
                ],
                className="mx-0 mb-2"
            ),
        ]
    ),
    className="mt-3",
)

ppl_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(ppltab1_content, label="1", tab_id="ppltab-1"),
                dbc.Tab(ppltab2_content, label="2", tab_id="ppltab-2"),
                dbc.Tab(ppltab3_content, label="3", tab_id="ppltab-3"),
            ],
            id="ppltabs-input",
            active_tab="ppltab-1",
            style={'width': '100%'},
            className="mx-1",
        ),
        html.Div(id="pplcontent-tab"),
    ]
)

## layout of tab 2
tab2_content = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Label("Please enter the loan information", size='lg', color='black-50')
                )
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Step 1. Please enter the loan amount", size='md', style={'font-weight': 'bold'}),
                            dbc.InputGroup(
                            [   
                                dbc.InputGroupAddon("$", addon_type="prepend"),
                                dbc.Input(placeholder="e.g. 10000", type="number", min=0, bs_size="md", inputMode="numeric", id='loan-input4'),
                            ]
                            ),
                        ],
                        className="mx-0"
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Step 2. Please enter the interest rate", size="md", style={'font-weight': 'bold'}),
                            dbc.InputGroup(
                            [   
                                dbc.Input(placeholder="e.g. 4", type="number", min=0, bs_size="md", inputMode="numeric", id='rate-input4'),
                                dbc.InputGroupAddon("%", addon_type="append")
                        ]
                        ),
                        ],
                        className="mx-0"
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Step 3. Please enter the payment", size="md", style={'font-weight': 'bold'}),
                            dbc.InputGroup(
                            [   
                                dbc.InputGroupAddon("$", addon_type="prepend"),
                                dbc.Input(placeholder="e.g. 15", type="number", min=0, bs_size="md", inputMode="numeric", id='payment-input4'),
                            ]
                        ),
                        ],
                        className="mx-0"
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Step 4. Please enter the extra payment", size="md", style={'font-weight': 'bold'}),
                            dbc.InputGroup(
                            [   
                                dbc.InputGroupAddon("$", addon_type="prepend"),
                                dbc.Input(placeholder="e.g. 10", type="number", min=0, bs_size="md", inputMode="numeric", id='expayment-input4'),
                            ]
                        ),
                        ],
                        className="mx-0"
                    ),
                    dbc.Label("Step 5. How many people contributes to this loan?", size="md", style={'font-weight': 'bold'}),
                    ppl_tabs,
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Br(),
                    html.Hr(),
                    con_table_card
                ]
             ),
        )
    ],
    className="w-100 mb-3",
    id="tab2-container",
    style={"height": "100vh"}, 
    fluid=True
)

tab0_content = dbc.Container(
    [
        html.Br(), 
        html.Hr(), 
        dbc.Jumbotron(
        [
            html.H1("Loan Caculator Application", className="display-3"),
            html.P(
                "By "
                "Roger Hung  ",
                className="lead",
            ),
            html.Hr(className="my-1"),
            html.P(
                "This is a calculator that can process multiple loans at the same time and "
                "is capable of evaluating several contributions"
            )
        ]
        ),
        html.Hr()
    ]
)

# Layout
tabs = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(tab0_content, label="Introduction", tab_id="tab-0", label_style={'font-size': 15, 'font-weight': 'bold'}),
                dbc.Tab(tab1_content, label="Loan Portfolio Calculator", tab_id="tab-1", label_style={'font-size': 15, 'font-weight': 'bold'}),
                dbc.Tab(tab2_content, label="Loan with multiple contributions", tab_id="tab-2", label_style={'font-size': 15, 'font-weight': 'bold'}),
            ],
            id="tabs-input",
            active_tab="tab-0",
            style={'width': '100%'},
        ),
        html.Div(id="content-tab"),
    ],
    id="second-container",
    style={"height": "100vh"}, 
    fluid=True
)


app.layout = tabs

# Callback
## Loan amount & Display Result
@app.callback(
    [Output('loan-table', 'data'),
    Output('result-display1', 'children'),
    Output('result-display2', 'children'),
    Output('result-display3', 'children'),
    Output('result-display4', 'children')],
    [Input("loan-input1", "value"),
    Input("rate-input1", "value"),
    Input("payment-input1", "value"),
    Input("expayment-input1", "value"),
    Input("button-submit1", "n_clicks"),
    Input("loan-input2", "value"),
    Input("rate-input2", "value"),
    Input("payment-input2", "value"),
    Input("expayment-input2", "value"),
    Input("button-submit2", "n_clicks"),
    Input("loan-input3", "value"),
    Input("rate-input3", "value"),
    Input("payment-input3", "value"),
    Input("expayment-input3", "value"),
    Input("button-submit3", "n_clicks")]
)
def display_result(loan_amount, rate, payment, expayment, click, loan_amount2=0, rate2=0, payment2=0, expayment2=0, click2=0,loan_amount3=0, rate3=0, payment3=0, expayment3=0, click3=0):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if (button_id == "button-submit1"):
        df = main.compute_schedule(loan_amount, rate, payment, expayment)
        updated_data = df.to_dict('records')
        interest_sum = round(df['Applied Interest'].sum(), 2)
        principal_sum = round(df['Applied Principal'].sum(), 2)
        loan_term = df.shape[0]
        reg_payment = df['Payment'].iloc[0] + df['Extra Payment'].iloc[0]
        return updated_data, html.P([f'{principal_sum}']), html.P([f'{interest_sum}']), html.P([f'{loan_term}']), f'{reg_payment}'

    elif (button_id == "button-submit2"):
        df = main.compute_schedule(loan_amount2, rate2, payment2, expayment2)
        updated_data=df.to_dict('records')
        interest_sum = round(df['Applied Interest'].sum(), 2)
        principal_sum = round(df['Applied Principal'].sum(), 2)
        loan_term = df.shape[0]
        reg_payment = df['Payment'].iloc[0] + df['Extra Payment'].iloc[0]
        return updated_data, html.P([f'{principal_sum}']), html.P([f'{interest_sum}']), html.P([f'{loan_term}']), f'{reg_payment}'

    elif (button_id == "button-submit3"):
        df = main.compute_schedule(loan_amount3, rate3, payment3, expayment3)
        updated_data=df.to_dict('records')
        interest_sum = round(df['Applied Interest'].sum(), 2)
        principal_sum = round(df['Applied Principal'].sum(), 2)
        loan_term = df.shape[0]
        reg_payment = df['Payment'].iloc[0] + df['Extra Payment'].iloc[0]
        return updated_data, html.P([f'{principal_sum}']), html.P([f'{interest_sum}']), html.P([f'{loan_term}']), f'{reg_payment}'
    else:
        return no_update

# Clear the inputs by reseting the clicks of submit button 
@app.callback([
    Output("loan-input1", "value"),
    Output("rate-input1", "value"),
    Output("payment-input1", "value"), 
    Output("expayment-input1", "value")],
    [Input('button-clear1', 'n_clicks')]
    )
def reset_input(clear):
    if clear >= 1:
        return "", "", "", ""
    else:
        return no_update

# Clear the inputs by reseting the clicks of submit button 
@app.callback([
    Output("loan-input2", "value"),
    Output("rate-input2", "value"),
    Output("payment-input2", "value"), 
    Output("expayment-input2", "value")],
    [Input('button-clear2', 'n_clicks')]
    )
def reset_input2(clear):
    if clear >= 1:
        return "", "", "", ""
    else:
        return no_update

# Clear the inputs by reseting the clicks of submit button 
@app.callback([
    Output("loan-input3", "value"),
    Output("rate-input3", "value"),
    Output("payment-input3", "value"), 
    Output("expayment-input3", "value")],
    [Input('button-clear3', 'n_clicks')]
    )
def reset_input3(clear):
    if clear >= 1:
        return "", "", "", ""
    else:
        return no_update


# Loan collapse
@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, loan_num+1)],
    [Input(f"loan-{i}-toggle", "n_clicks") for i in range(1, loan_num+1)],
    [State(f"collapse-{i}", "is_open") for i in range(1, loan_num+1)]
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "loan-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "loan-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "loan-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False

# Toggle schedule 
@app.callback(
    [Output("collapse-table", "is_open")],
    [Input("tableToggle-button", "n_clicks")],
    [State("collapse-table", "is_open")],
)
def toggle_schedule(n, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [False]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "tableToggle-button" and n:
        return [not is_open]
    return [False]

# Toggle contribution table
@app.callback(
    [Output("collapse-conTable", "is_open")],
    [Input("conTableToggle-button", "n_clicks")],
    [State("collapse-conTable", "is_open")],
)
def toggle_conTable(n, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [False]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "conTableToggle-button" and n:
        return [not is_open]
    return [False]

@app.callback(
    Output("loanNum-card", "children"),
    [
        Input("loanNum-input", "value")
    ],
)
def num_change(radio_items_value):
    if not radio_items_value:
        return no_update
    else:
        loan_port = dbc.FormGroup(
            [
                html.Div(
                    [make_item(i) if i <= int(radio_items_value) else make_item(i, d=True) for i in range(1, 4)], className="accordion"
                    )
            ],
            className="mx-2 my-2"
        )
        
    
    return loan_port


# # Use tab for different ppl
# @app.callback(Output("pplcontent-tab", "children"), [Input("ppltabs-input", "active_tab")])
# def switch_tab(cur_tab):
#     if cur_tab == "ppltab-1":
#         return ppltab1_content
#     elif cur_tab == "ppltab-2":
#         return ppltab2_content
#     elif cur_tab == "ppltab-3":
#         return ppltab3_content
#     return html.P("This shouldn't ever be displayed...")

# Callback for contributors' input
@app.callback(
    Output('con-table', 'data'),
    [Input("loan-input4", "value"),
    Input("rate-input4", "value"),
    Input("payment-input4", "value"),
    Input("expayment-input4", "value"),
    Input("pplloan-input1_1", "value"),
    Input("pplloan-input2_1", "value"),
    Input("pplloan-input2_2", "value"),
    Input("pplloan-input3_1", "value"),
    Input("pplloan-input3_2", "value"),
    Input("pplloan-input3_3", "value"),
    Input("ppl-submit1", "n_clicks"),
    Input("ppl-submit2", "n_clicks"),
    Input("ppl-submit3", "n_clicks")]
)
def con_table_callback(loan_amount, rate, payment, expayment, con_1_1, con_2_1, con_2_2, con_3_1, con_3_2, con_3_3, click1, click2, click3):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks'
        print(button_id)
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(button_id)
    
    if (button_id == "ppl-submit1"):
        print(f'Initial click = {click1}')
        loan_impacts = LoanImpacts.LoanImpacts(principal=loan_amount, rate=rate, payment=payment, extra_payment=expayment, contributions=[con_1_1])
        df = loan_impacts.compute_impacts()
        updated_data = df.to_dict('records')
        print(f'data = {updated_data}')
        print(button_id)
        return updated_data

    elif (button_id == "ppl-submit2"):
        print(f'Initial click2 = {click2}')
        loan_impacts = LoanImpacts.LoanImpacts(principal=loan_amount, rate=rate, payment=payment, extra_payment=expayment, contributions=[con_2_1, con_2_2])
        df = loan_impacts.compute_impacts()
        updated_data = df.to_dict('records')
        print(button_id)
        return updated_data

    elif (button_id == "ppl-submit3"):
        print(f'Initial click3 = {click3}')
        loan_impacts = LoanImpacts.LoanImpacts(principal=loan_amount, rate=rate, payment=payment, extra_payment=expayment, contributions=[con_3_1, con_3_2, con_3_3])
        df = loan_impacts.compute_impacts()
        updated_data = df.to_dict('records')
        print(button_id)
        return updated_data

# Clear the inputs by reseting the clicks of submit button 
@app.callback([
    Output("loan-input4", "value"),
    Output("rate-input4", "value"),
    Output("payment-input4", "value"), 
    Output("expayment-input4", "value"),
    Output("pplloan-input1_1", "value"),
    Output("pplloan-input2_1", "value"),
    Output("pplloan-input2_2", "value"),
    Output("pplloan-input3_1", "value"),
    Output("pplloan-input3_2", "value"),
    Output("pplloan-input3_3", "value")],
    [Input('ppl-clear1', 'n_clicks'),
    Input('ppl-clear2', 'n_clicks'),
    Input('ppl-clear3', 'n_clicks'),]
    )
def reset_tab2_input(clear1, clear2, clear3):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id:
        return "", "", "", "", "", "", "", "", "", ""
    else:
        return no_update


if __name__ == '__main__':
    app.run_server(debug=True)
    print('App Start')