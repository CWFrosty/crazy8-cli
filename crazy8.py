from random import shuffle

# ----------------------------------------
#  Models
# ----------------------------------------

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit          # ♥ ♦ ♣ ♠
        self.rank = rank          # 2-10, J, Q, K, A, 8

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        suits  = "♥♦♣♠"
        ranks  = [str(n) for n in range(2, 11)] + list("JQKA8")
        self.cards = [Card(s, r) for s in suits for r in ranks]
        shuffle(self.cards)

    def draw(self):
        """Vzemi vrhnjo karto; če jih zmanjka vrni None."""
        return self.cards.pop() if self.cards else None
        
def legal_move(card, top_card):
    """Karta je legalna, če:
       • je enake barve ali ranga kot zgornja
       • ALI je osmica (wild)
    """
    return (
        card.rank == "8"
        or card.suit == top_card.suit
        or card.rank == top_card.rank
    )

class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai

def choose_card(self, top_card):
        """Vrne (index, card) ali None, če nima legalne poteze."""
        for idx, card in enumerate(self.hand):
            if legal_move(card, top_card):
                return idx, card         # prva legalna
        return None                      # nič ne ustreza


class Game:
    def __init__(self):
        self.deck     = Deck()
        self.players  = [Player("Ti"), Player("CPU", is_ai=True)]
        self.discard  = []
        self.current  = 0  # indeks trenutnega igralca

    def deal(self):
        """Razdeli 5 kart vsakemu igralcu in položi eno karto na mizo."""
        for _ in range(5):
            for p in self.players:
                p.hand.append(self.deck.draw())
        self.discard.append(self.deck.draw())

    # TODO: implement play_turn(), check_winner(), run()

if __name__ == "__main__":
    game = Game()
    game.deal()
    # TODO: game.run()
