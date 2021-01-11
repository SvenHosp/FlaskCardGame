import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_html_components as html
import dash_core_components as dcc
import game

app = dash.Dash(__name__, suppress_callback_exceptions=True)

global card_game
card_game = game.game_engine()

bg_color = '#ad0000'


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

def generate_card_representations():
    container_list = []
    card_to_game = []
    i = 0
    for _card in card_game.get_card_list():
        container_list.append(
            dcc.Textarea(
                id={
                    'type': 'card_Textarea',
                    'index': i,
                    'card_value': _card.value,
                    'bg_color': _card.bg_color
                },
                value=str(_card.value),
                style={'width': 50, 'height': 200, 'backgroundColor': _card.bg_color, 'color': _card.text_color, 'textAlign': 'center', 'fontSize': 20},
                readOnly=True,
                n_clicks=0,
            )
        )
        i = i + 1
    return container_list

app.layout = html.Div([
    html.Div(id='dynamic-cards-container', children=generate_card_representations())
])

@app.callback(
    Output('dynamic-cards-container', 'children'),
    Input({'type': 'card_Textarea', 'index': ALL, 'card_value': ALL, 'bg_color': ALL}, 'n_clicks'),
    State({'type': 'card_Textarea', 'index': ALL, 'card_value': ALL, 'bg_color': ALL}, 'value')
)
def update_output(n_clicks, value):
    # n_clicks is a list!!!!! of elements
    trigger = None
    for t in dash.callback_context.triggered:
        trigger = t
        continue

    if trigger['value'] is not None:
        trigger_dict = trigger_prop_to_dict(trigger)
    
        card_game.remove_card(trigger_dict['card_value'], trigger_dict['bg_color'])

    return generate_card_representations()

if __name__ == '__main__':
    app.run_server(debug=True)