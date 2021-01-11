class card():
    def __init__(self, value) -> None:
        self.value = value
        self.bg_color = '#ad0000'
        self.text_color = '#ffffff'

class game_engine():
    def __init__(self) -> None:
        super().__init__()
        self.card_list = []
        for i in range(6):
            self.card_list.append(card(str(i+1)))

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
