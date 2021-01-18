class card():
    def __init__(self, value, bg_color, text_color) -> None:
        self.value = value
        self.bg_color = bg_color
        self.text_color = text_color
        self.username = ''

    def set_username(self, username):
        self.username = username

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

    def push_card(self, card):
        self.card_list.append(card)

    def push_cards(self, card_list):
        for _card in card_list:
            self.push_card(_card)

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
        
        if __card in self.card_list:
            self.card_list.remove(__card)
        return __card


class card_engine():
    def __init__(self) -> None:
        super().__init__()
        self.user_list = []
        self.card_stack_list = []
        self.stich_open = False
        self.stich = []
        self.chat = []
    
    def set_stich_state(self, bool):
        self.stich_open = bool
    
    def is_stich_open(self):
        return self.stich_open
    
    def card_stack_empty(self):
        return len(self.card_stack_list) == 0
    
    def cards_distributed(self):
        if len(self.user_list) > 0 and len(self.user_list[0].get_card_list()) > 0:
            return True
        else:
            return False
    
    def create_card_stack(self):
        import secrets
        stack_unmixed_type = [
            {
                'color': 'blue',
                'number': 9
            },
            {
                'color': 'green',
                'number': 9
            },
            {
                'color': 'yellow',
                'number': 9
            },
            {
                'color': 'red',
                'number': 9
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

            _card = stack_unmixed.pop(index)

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

    def get_usernames(self):
        usernames = None
        for _user in self.user_list:
            if usernames is not None:
                usernames = usernames + ',' + _user.name
            else:
                usernames = _user.name
        return usernames
    
    def distribute_cards(self):
        import math
        if len(self.user_list) > 0:
            cards_per_user = math.ceil(len(self.card_stack_list)/len(self.user_list))
            for _user in self.user_list:
                for index in range(0,cards_per_user):
                    if len(self.card_stack_list) > 0:
                        _user.push_card(self.card_stack_list.pop(0))

    def get_card_list_for_user(self, username):
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
        card = None
        for _user in self.user_list:
            if username == _user.name:
                card = _user.remove_card(value, bg_color)
                card.set_username(username)
        return card

    def create_stich(self):
        self.stich = []
    
    def card_to_stich(self, card):
        self.stich.append(card)

    def get_stich(self):
        return self.stich

    def create_chat(self):
        self.chat = []
    
    def add_message_to_chat(self, username, message):
        self.chat.append("{username}: {message}".format(username=username, message=message))

    def get_chat(self):
        return self.chat

    def get_chat_formated(self):
        chat_formated = None
        for msg in self.chat:
            if not chat_formated:
                chat_formated = msg
            else:
                chat_formated = chat_formated + '\n' + msg
        return chat_formated
