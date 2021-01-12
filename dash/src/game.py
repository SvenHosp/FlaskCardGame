class card():
    def __init__(self, value, bg_color, text_color) -> None:
        self.value = value
        self.bg_color = bg_color
        self.text_color = text_color

    def get_possible_card_color_list():
        return [
            {
                'name': 'red',
                'value': '#ad0000',
                'contrast': 'white'
            },
            {
                'name': 'blue',
                'value': '#0000ad',
                'contrast': 'white'
            },
            {
                'name': 'yellow',
                'value': '#cac600',
                'contrast': 'white'
            },
            {
                'name': 'green',
                'value': '#00ad00',
                'contrast': 'white'
            },
            {
                'name': 'black',
                'value': '#000000',
                'contrast': 'white'
            },
            {
                'name': 'white',
                'value': '#ffffff',
                'contrast': 'black'
            },
            {
                'name': 'lila',
                'value': '#e30082',
                'contrast': 'white'
            }
        ]
    
    def get_bg_text_color_hex(col_name):
        color_dict = {}
        colors_list = card.get_possible_card_color_list()
        for _color_dict in colors_list:
            if _color_dict['name'] == col_name:
                color_dict['bg_color'] = _color_dict['value']
                for __color_dict in colors_list:
                    if __color_dict['name'] == _color_dict['contrast']:
                        color_dict['text_color'] = __color_dict['value']
        return color_dict


class user():
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.card_list = []


    def push_cards(self, card_list):
        for _card in card_list:
            self.card_list.append(_card)

    def get_card_list(self):
        return self.card_list
    
    def get_card(self, value, bg_color):
        for _card in self.card_list:
            if _card.value == value and _card.bg_color == bg_color:
                return _card
        return None

    def remove_card(self, _card):
        self.card_list.remove(_card)
    
    def remove_card(self, value, bg_color):
        __card = None
        for _card in self.card_list:
            if _card.value == value and _card.bg_color == bg_color:
                __card = _card
                continue
        self.card_list.remove(__card)
class card_engine():
    def __init__(self) -> None:
        super().__init__()
        self.user_list = []
        self.card_stack_list = []
    
    def create_card_stack(self):
        import secrets
        stack_unmixed_type = [
            {
                'color': 'blue',
                'number': 10
            },
            {
                'color': 'green',
                'number': 10
            },
            {
                'color': 'yellow',
                'number': 10
            },
            {
                'color': 'red',
                'number': 10
            },
            {
                'color': 'black',
                'number': 4
            }
        ]
        stack_unmixed = []
        for type in stack_unmixed_type:
            for _value in range(1, type['number'] + 1):
                color_dict = card.get_bg_text_color_hex(type['color'])
                stack_unmixed.append(
                    card(
                        _value,
                        color_dict['bg_color'],
                        color_dict['text_color']
                    )
                )

        total_number_cards = len(stack_unmixed)
        
        stack_mixed = []
        
        for i in range(0, total_number_cards):
            index = secrets.randbelow(len(stack_unmixed))

            _card = stack_unmixed[index]

            stack_unmixed.pop(index)

            stack_mixed.append(_card)

        self.card_stack_list = stack_mixed
    
    def create_user(self, name):
        for _user in self.user_list:
            if _user.name == name:
                return None
        self.user_list.append(user(name))
    
    def get_user(self, name):
        for _user in self.user_list:
            if _user.name == name:
                return _user
        return None
    
    def distribute_cards(self):
        for _user in self.user_list:
            _user.push_cards(self.card_stack_list)

    def get_card_list(self, username):
        for _user in self.user_list:
            if username == _user.name:
                return _user.get_card_list()
    
    def get_card(self, username, value, bg_color):
        for _user in self.user_list:
            if username == _user.name:
                return _user.get_card(value, bg_color)


    def remove_card(self, username, _card):
        for _user in self.user_list:
            if username == _user.name:
                _user.remove_card(_card)
    
    def remove_card(self, username, value, bg_color):
        for _user in self.user_list:
            if username == _user.name:
                _user.remove_card(value, bg_color)


