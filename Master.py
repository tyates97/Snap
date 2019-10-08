import random as rand
from operator import attrgetter


# AH is Ace of Hearts. Could have made a class with suit and number attributes, but this is much quicker.
deck = ["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"]


class Player:
    def __init__(self, hand=None, min_reaction_time=0.2, max_reaction_time=0.4, name=0):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand
        self.min_reaction_time = min_reaction_time
        self.max_reaction_time = max_reaction_time
        self.name = name

    def play_card(self, played_cards):
        played_cards.append(self.hand.pop(0))
        print("Player ", self.name, "has ", len(self.hand)+1, " cards in their hand. They play ", played_cards[-1], ".")
        return played_cards

    def pick_up(self, played_cards):
        print("Player ", self.name, " has picked up ", len(played_cards), " cards!")
        while len(played_cards) > 0:
            self.hand.append(played_cards.pop(-1))

    def get_reaction_time(self):                                                         # so players have varying chances of winning
        reaction_time = rand.uniform(self.min_reaction_time, self.max_reaction_time)     # pick random reaction time between min + max
        print("Player ", self.name, "said 'Snap!' in ", reaction_time, " seconds.")
        return reaction_time

# -----------------------------------------------------------------------------------------------------------------------
# GAME START


def get_num_players():
    num_players = input("How many players are in the game? ")
    try:
        num_players = int(num_players)                                                        # turning string to int + accept integers
        print("Excellent. The number of players is ", num_players)
    except ValueError:
        print("Please type an integer number.")                                               # don't accept non-integers
        get_num_players()
    return num_players


def get_num_decks(players):                                                                   # v similar to howManyPlayers()
    num_decks = input("How many decks are in the game? ")
    try:
        num_decks = int(num_decks)
        print("Great! There will be ", len(players), " players playing with ", num_decks, " decks.")
    except ValueError:
        print("Please type an integer number.")
        get_num_decks(players)
    return num_decks


def make_play_deck(deck, num_decks):
    return [deck[i % len(deck)] for i in range(len(deck)*num_decks)]


def make_players(num_players):
    return [Player(name=i) for i in range(num_players)]

def shuffle_deck(deck):
    print("The deck has been shuffled.")
    rand.shuffle(deck)


def deal_cards(players):
    for i in range(len(deck)):                     # cycling through the cards
        turn = i % len(players)                    # which player is drawing the card
        players[turn].hand.append(deck.pop(0))
    print("Each player has now been dealt their hand.")


# -----------------------------------------------------------------------------------------------------------------------
# GAME PLAY

def is_snap(played_cards):
    if len(played_cards) > 1:
        if played_cards[len(played_cards) - 1][0] is played_cards[len(played_cards) - 2][0]:        # if first element of last card matches first element of penultimate card
            print("The cards match!")
            return True
        else:
            return False


def is_game_over(players):
    if len(players) is 1:
        print("Player ", players[0].name, " is the winner!")
        return True
    else:
        return False


def player_is_out(players):
    for player in players:
        if len(player.hand) is 0:
            return player
        #return False


def play_game(players):
    played_cards = []
    while not is_game_over(players):
        for player in players:

            #if player_is_out(players):
            #    print("Player ", player_is_out(players).name, " can't play - they're out!")
            #    players.remove(player_is_out(players))
            #    #players = [player for player in players if player is not player_is_out(players)]   #TODO: after player goes out, it's the wrong player's turn
            #else:
            #    played_cards = player.play_card(played_cards)

            try:
                played_cards = player.play_card(played_cards)
            except IndexError:
                print("Player ", player_is_out(players).name, " can't play - they're out!")        #TODO: after player goes out, it's the wrong player's turn
                players.remove(player_is_out(players))

            if is_snap(played_cards):
                fastest_reaction = max(players, key=attrgetter('max_reaction_time')).max_reaction_time
                for snapper in players:
                    player_reaction = snapper.get_reaction_time()
                    if player_reaction < fastest_reaction:
                        fastest_reaction = player_reaction
                        winning_snapper = snapper
                    elif player_reaction is fastest_reaction:
                        winning_snapper
                winning_snapper.pick_up(played_cards)

            if len(player.hand) is 1:
                print(player.name)


# -----------------------------------------------------------------------------------------------------------------------
# GameStart Run
num_players = get_num_players()
players = make_players(num_players)
num_decks = get_num_decks(players)
deck = make_play_deck(deck, num_decks)
shuffle_deck(deck)
deal_cards(players)

# GamePlay Run
play_game(players)
