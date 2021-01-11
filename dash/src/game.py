class card():
    def __init__(self, value) -> None:
        self.value = value
        self.bg_color = '#ad0000'
        self.text_color = '#ffffff'

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

class game_engine():
    def __init__(self) -> None:
        super().__init__()
        self.user_list = []
        self.card_stack_list = []
        for i in range(6):
            self.card_stack_list.append(card(str(i+1)))
    
    def create_user(self, name):
        self.user_list.append(user(name))
    
    def get_user(self, name):
        for _user in self.user_list:
            if _user.name == name:
                return _user
    
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


