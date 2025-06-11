from random import shuffle

# ----------------------------------------
#  MODELI
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
        """Vzemi vrhnjo karto; vrne None, če je kup prazen."""
        return self.cards.pop() if self.cards else None


def legal_move(card: Card, top_card: Card) -> bool:
    """Karta je legalna, če je:
       • enak SUIT ali RANK kot zgornja
       • ali je osmica (wild)
    """
    return (
        card.rank == "8"
        or card.suit == top_card.suit
        or card.rank == top_card.rank
    )

# ----------------------------------------
#  IGRALEC
# ----------------------------------------

class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name   = name
        self.hand   = []
        self.is_ai  = is_ai

    def choose_card(self, top_card: Card):
        """Vrne (index, karta) ali None."""
        # ───────── ČLOVEK: vprašaj za vnos, dokler ne izbere legalnega ali 'p'
        if not self.is_ai:
            # pokaži roko
            print("Tvoja roka:", ", ".join(f"[{i}]{c}" for i, c in enumerate(self.hand)))
            while True:
                choice = input("Izberi index karte ali 'p' za potegni: ")
                if choice.lower() == 'p':
                    return None
                if choice.isdigit():
                    idx = int(choice)
                    if 0 <= idx < len(self.hand) and legal_move(self.hand[idx], top_card):
                        return idx, self.hand[idx]
                print("Neveljavna poteza – poskusi ponovno.")
  
        for idx, card in enumerate(self.hand):
            if legal_move(card, top_card):
                return idx, card
        return None



# ----------------------------------------
#  GLAVNA IGRA
# ----------------------------------------

class Game:
    def __init__(self):
        self.deck     = Deck()
        self.players  = [Player("Ti"), Player("CPU", is_ai=True)]
        self.discard  = []
        self.current  = 0  # indeks trenutnega igralca

    # --------------------
    #  Setup
    # --------------------
    def deal(self):
        """Razdeli po 5 kart + 1 odloži na kup za začetek."""
        for _ in range(5):
            for p in self.players:
                p.hand.append(self.deck.draw())
        self.discard.append(self.deck.draw())

    # --------------------
    #  Ena poteza
    # --------------------
    def play_turn(self):
        player  = self.players[self.current]
        top     = self.discard[-1]

        choice = player.choose_card(top)

        if choice is None:
            drawn = self.deck.draw()
            if drawn:
                player.hand.append(drawn)
                print(f"{player.name} vleče {drawn}")
            else:
                print("Kup je prazen, {player.name} preskoči.")
        else:
            idx, card = choice
            self.discard.append(player.hand.pop(idx))
            print(f"{player.name} odigra {card}")

        # Preveri zmago
        if not player.hand:
            return player

        # Na vrsto pride naslednji
        self.current = (self.current + 1) % len(self.players)
        return None

    # --------------------
    #  Glavna zanka
    # --------------------
    def run(self):
        winner = None
        while not winner:
            winner = self.play_turn()

        print(f"\n🏆  Zmagovalec je: {winner.name}  🏆")

# ----------------------------------------
#  ZAŽENI IGRO
# ----------------------------------------

if __name__ == "__main__":
    game = Game()
    game.deal()
    game.run()

