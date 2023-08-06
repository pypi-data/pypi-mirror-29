import random

from pyschieber.card import from_string_to_card
from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, geschoben):
        return move(choices=list(Trumpf))

    def choose_card(self, state=None):
        table_cards = [from_string_to_card(entry['card']) for entry in state['table']]
        trumpf = Trumpf[state['trumpf']]
        cards = self.allowed_cards(table_cards=table_cards, trumpf=trumpf)
        return move(choices=cards)

def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
