import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_html_components as html
import dash_core_components as dcc
import game
import os

# read URL base path from environment
urlbase = os.getenv('URL_BASE_PATH', default='/')
# Dash requires it to end with slash. Thus, make sure it does.
if not urlbase.endswith('/'):
    urlbase = urlbase +'/'

app = dash.Dash(__name__, suppress_callback_exceptions=True, url_base_pathname=urlbase)

global card_game
card_game = game.card_engine()

def trigger_prop_to_dict(trigger_prop):
    import json

    ret_dict = {}

    prop_ids = trigger_prop['prop_id']
    prop_id_dict = json.loads(prop_ids[:prop_ids.find('.')])

    ret_dict['index'] = prop_id_dict['index']
    ret_dict['type'] = prop_id_dict['type']
    ret_dict['card_value'] = prop_id_dict['card_value']
    ret_dict['bg_color'] = prop_id_dict['bg_color']

    return ret_dict

def generate_card_representations(username):
    container_list = []
    i = 0
    user_cards = card_game.get_card_list_for_user(username)
    if user_cards is not None:
        for _card in user_cards:
            container_list.append(
                dcc.Textarea(
                    id={
                        'type': 'card_Textarea',
                        'index': i,
                        'card_value': _card.value,
                        'bg_color': _card.bg_color
                    },
                    value=str(_card.value),
                    style={'width': 50, 'height': 100, 'backgroundColor': _card.bg_color, 'color': _card.text_color, 'textAlign': 'center', 'fontSize': 20},
                    readOnly=True,
                    n_clicks=0,
                )
            )
            i = i + 1
    return container_list

def generate_stich_representations():
    container_list = []
    i = 0
    user_cards = card_game.get_stich()
    if user_cards is not None:
        for _card in user_cards:
            container_list.append(
                dcc.Textarea(
                    id={
                        'type': 'card_Textarea',
                        'index': i,
                        'card_value': _card.value,
                        'bg_color': _card.bg_color
                    },
                    value=_card.username + ':\n' + str(_card.value),
                    style={'width': 50, 'height': 100, 'backgroundColor': _card.bg_color, 'color': _card.text_color, 'textAlign': 'center', 'fontSize': 20},
                    readOnly=True,
                    n_clicks=0,
                )
            )
            i = i + 1
    return container_list

app.layout = html.Div([
    html.H1(children='Card Board'),
    dcc.Interval(
        id='intervalComponent',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Tabs([
        dcc.Tab(label='Board', children=[
            html.Div(id='game_board', children=[
                html.Div(id='player', children=[
                    dcc.Input(
                        id='input-username',
                        placeholder='Enter your name...',
                        type='text',
                        value=''
                    ),
                    html.Button('Create or set user', id='button-username', n_clicks=0),
                    html.Div(id='div-username',
                        children='Enter your name and press submit')
                ]),
                html.Div(id='cards', children=''),
                html.Div(id='cards_hidden', style={'display':'none'}),
                html.Table(id='table', children=[
                    html.Tr(id='row', children=[
                        html.Td(id='td_chat', children=[
                            html.Div(id='div_chat_desc', children='enter your hint and press button hint:'),
                            dcc.Input(
                                id='input_chat',
                                placeholder='Enter your hint...',
                                type='text',
                                value=''
                            ),
                            html.Button('push hint', id='button_push_hint', n_clicks=0),
                            html.Div(id='button_push_hint_hidden', style={'display':'none'}),
                            html.Button('start/clear hints', id='button_reset_hints', n_clicks=0),
                            html.Div(id='button_reset_hints_hidden', style={'display':'none'}),
                            html.Div(id='hint_format_field', children=[
                                dcc.Textarea(id='textarea_hint', value='')
                            ])
                        ]),
                        html.Td(id='td_stich', children=[
                            html.Div(id='stich_board', children=[
                                html.Button('Open Stich', id='button-stich-open', n_clicks=0),
                                html.Div(id='stich-open_hidden', style={'display':'none'}),
                                html.Button('close Stich', id='button-stich-close', n_clicks=0),
                                html.Div(id='stich-close_hidden', style={'display':'none'}),
                                html.Div(id='div_stich-status', children=''),
                                html.Div(id='stich_field', children='')
                            ])
                        ])
                    ])
                ]),
                
            ])
        ]),
        dcc.Tab(label='Admin', children=[
            html.Div(id='admin_board', children=[
                html.Button('create card stack', id='button_card_stack', n_clicks=0),
                html.Div(id='div_card_stack_hidden', style={'display':'none'}),
                html.Button('distribute cards', id='button_distribute_cards', n_clicks=0),
                html.Div(id='div_distribute_card_hidden', style={'display':'none'}),
                html.Div(id='div_card_stack', children='klick to create and mix card stack'),
                html.Div(id='div_usernames_description', children='Players are:'),
                html.Div(id='div_usernames', children=''),
                html.Button('restart', id='button_restart', n_clicks=0),
                html.Div(id='div_restart_hidden', style={'display':'none'}),
            ])
        ])
    ])
])

@app.callback(
    Output('div_card_stack', 'children'),
    [
        Input('intervalComponent', 'n_intervals')
    ])
def update_card_status(n):
    if not card_game.card_stack_empty() and not card_game.cards_distributed():
        return 'card stack is created'
    elif card_game.cards_distributed():
        return 'cards distributed to players'
    else:
        return 'card stack is empty'

@app.callback(
    Output('div_usernames', 'children'),
    [
        Input('intervalComponent', 'n_intervals')
    ])
def update_usernames_list(n):
    names = card_game.get_usernames()
    return names

@app.callback(
    Output('div_card_stack_hidden', 'children'),
    [
        Input('button_card_stack', 'n_clicks')
    ])
def create_card_stack(n_clicks):
    if n_clicks >= 1:
        card_game.create_card_stack()
        return 'hidden'

@app.callback(
    Output('div_distribute_card_hidden', 'children'),
    [
        Input('button_distribute_cards', 'n_clicks')
    ])
def distribute_cards(n_clicks):
    if n_clicks >= 1:
        card_game.distribute_cards()
        return 'hidden'

@app.callback(
    Output('div-username', 'children'),
    [Input('button-username', 'n_clicks')],
    [State('input-username', 'value')])
def create_user(n_clicks, value):
    if n_clicks >= 1:
        card_game.create_user(value)
        return 'Now you can distribute cards to the users.'

@app.callback(
    Output('cards', 'children'),
    [
        Input('intervalComponent', 'n_intervals')
    ],
    [State('input-username', 'value')])
def update_cards_for_user(n, username):
    cards = []
    if username:
        cards = generate_card_representations(username)
    return cards

@app.callback(
    Output('cards_hidden', 'children'),
    [
        Input({'type': 'card_Textarea', 'index': ALL, 'card_value': ALL, 'bg_color': ALL}, 'n_clicks'),
    ],
    [
        State('input-username','value')
    ]
)
def action_card_clicked(n, username):
    # n_clicks is a list!!!!! of elements
    if card_game.is_stich_open() and 1 in n:
        trigger = None
        for t in dash.callback_context.triggered:
            trigger = t
            continue

        if trigger['value'] is not None:
            trigger_dict = trigger_prop_to_dict(trigger)
        
            stich_card = card_game.remove_card(username, trigger_dict['card_value'], trigger_dict['bg_color'])
            card_game.card_to_stich(stich_card)

    return 'hidden'

@app.callback(
    Output('stich-open_hidden', 'children'),
    [Input('button-stich-open', 'n_clicks')])
def create_user(n_clicks):
    if n_clicks >= 1:
        card_game.set_stich_state(True)
        card_game.create_stich()
        return 'hidden'

@app.callback(
    Output('stich-close_hidden', 'children'),
    [Input('button-stich-close', 'n_clicks')])
def create_user(n_clicks):
    if n_clicks >= 1:
        card_game.set_stich_state(False)
        return 'hidden'

@app.callback(
    Output('div_stich-status', 'children'),
    [
        Input('intervalComponent', 'n_intervals')
    ])
def update_cards_for_user(n):
    if card_game.is_stich_open():
        return 'you can play your card'
    else:
        return 'stich field is closed'

@app.callback(
    Output('stich_field', 'children'),
    [
        Input('intervalComponent', 'n_intervals')
    ])
def update_stich_field(n):
    cards = generate_stich_representations()
    return cards

@app.callback(
    Output('div_restart_hidden', 'children'),
    [Input('button_restart', 'n_clicks')])
def restart_game(n_clicks):
    global card_game
    if n_clicks >= 1:
        card_game = game.card_engine()
    return 'hidden'

@app.callback(
    Output('button_reset_hints_hidden', 'children'),
    [Input('button_reset_hints', 'n_clicks')])
def restart_game(n_clicks):
    card_game.create_chat()
    return 'hidden'

@app.callback(
    Output('button_push_hint_hidden', 'children'),
    [Input('button_push_hint', 'n_clicks')],
    [
        State('input_chat','value'),
        State('input-username', 'value')
    ])
def restart_game(n_clicks, msg, username):
    card_game.add_message_to_chat(username, msg)
    return 'hidden'

@app.callback(
    Output('textarea_hint', 'value'),
    [
        Input('intervalComponent', 'n_intervals')
    ])
def update_stich_field(n):
    return card_game.get_chat_formated()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
