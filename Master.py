import random as rand

noPlayers = 0
noDecks = 1
players = []
playedCards = []
snap = False
gameOver = False
snappers = [None]*2                                  # the two contending for snap()
totalCards = 0
whoHasNoCards = 0;


#AH is Ace of Hearts. Could have made a class with suit and number attributes, but this is much quicker.
deck = ["AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD"]

class Player:
    def __init__(self):
        self.hand = [None]*(int(len(deck) / noPlayers))
        self.minReactionTime = 0.2                      # included so you can easily make some players stronger than others
        self.maxReactionTime = 0.4
        self.reactionTime = self.maxReactionTime
        self.name = 0

    def playCard(self):
            playedCards.append(self.hand[0])                # play your top card
            print("Player ", self.name, "plays ", self.hand[0])
            self.hand.remove(self.hand[0])                  # remove that card from your hand


    def pickUp(self):                                   #TODO: check pickUp() works.
        global playedCards
        for i in range(len(playedCards)):
            self.hand.append(playedCards[i])
        print("Player ", self.name, " has picked up ", len(playedCards), " cards!")
        playedCards = []

    def saySnap(self):                                  # so players have varying chances of winning
        self.reactionTime = rand.uniform(self.minReactionTime, self.maxReactionTime)  # pick random reaction time between min + max
        print("Player ", self.name, "said 'Snap!' in ", self.reactionTime, " seconds.")

#-----------------------------------------------------------------------------------------------------------------------
# GAME START

def howManyPlayers():
    global noPlayers
    noPlayers = input("How many players are in the game? ")
    try:
        noPlayers = int(noPlayers)                                                          # turning string to int + accept integers
        print("Excellent. The number of players is ", noPlayers)
    except ValueError:
        print("Please type an integer number.")                                             # don't accept non-integers
        howManyPlayers()

def howManyDecks():                                                                         # v similar to howManyPlayers()
    global deck
    global noDecks
    global totalCards
    tempDeck = deck
    noDecks = input("How many decks are in the game? ")
    try:
        noDecks = int(noDecks)
        print("Great! There will be ", noPlayers, " players playing with ", noDecks, " decks.")
    except ValueError:
        print("Please type an integer number.")
        howManyDecks()

    for i in range(noDecks):
        for i in range(len(deck)):
            tempDeck.append(deck[i])               # add number of decks to dummy variable
    deck = tempDeck                         # make dummy variable the deck.
    totalCards = len(deck)

def createPlayers():
    global players
    players = [None]*noPlayers              # create list of players
    for i in range(0, noPlayers):
        players[i] = Player()               # populate list
        players[i].name = i

def calculateHandSize():
    for i in range(len(deck) % noPlayers):  # leftover cards, that dont divide evenly by no. of players
        players[i].hand.append(None)        # add an extra card. Makes total cards add to 52.

def shuffleDeck():
    rand.shuffle(deck)
    print("The deck has been shuffled.")


def dealCards():
    global players
    for i in range(len(deck)):              # cycling through the cards
        j = i % noPlayers                   # which player is drawing the card
        cardsInHand = int(i/noPlayers)      # opposite of modulo - smallest number of cards in players' hand
        players[j].hand[cardsInHand] = deck[i]
    print("Each player has now been dealt their hand.")

def GameStart():
    howManyPlayers()
    howManyDecks()
    createPlayers()
    calculateHandSize()
    shuffleDeck()
    dealCards()

#-----------------------------------------------------------------------------------------------------------------------
# GAME PLAY

def checkSnap():
    global snap
    global playedCards
    if len(playedCards) > 1:
        if playedCards[len(playedCards) - 1][0] == playedCards[len(playedCards) - 2][0]:        # if first element of last card matches first element of penultimate card
            snap = True
            print("The cards match!")

def checkWinLoss():
    global players
    global noPlayers
    global totalCards
    global gameOver
    global whoHasNoCards
    index = 0

    for i in range(noPlayers):

        if len(players[i].hand) == totalCards or len(players) == 1:
            gameOver = True
            print("Player ", players[i].name, " is the winner!")

        if len(players[i].hand) == 0:
            index = i                                           # use this dummy variable to mark which player is out.
            noPlayers = noPlayers - 1
            print("Player ", players[i].name, " is out!")

    if len(players[index].hand) == 0:
        players.remove(players[index])                          # then get rid of the player (can't do it in the for loop)



def playRound():
    global noPlayers
    global gameOver
    global snap
    global snappers
    global playedCards
    global whoHasNoCards
    reactionTimes = [None]*noPlayers

    for i in range(noPlayers):
        players[i].playCard()
        checkSnap()

        if(snap):                                               # if snap is true
            snappers[0] = players[i]                            # player that played + previous player are contending.
            if(i == 0):                                         # if player 0 just played
                snappers[1] = players[len(players) - 1]         # final player contends with them
            else:
                snappers[1] = players[i-1]                      # otherwise it's the player before the one that played.

            for i in range(noPlayers):
                players[i].saySnap()                            # each player says snap
                reactionTimes[i] = players[i].reactionTime

            for i in range(len(reactionTimes)):
                if reactionTimes[i] == min(reactionTimes):      # take the index of the minimum reaction time
                    players[i].pickUp()                         # that player picks up the cards.
                    snap = False

    checkWinLoss()                                              # check if any players win/have no cards at the end of the round.


def PlayGame():
    while(gameOver == False):
        playRound()
#-----------------------------------------------------------------------------------------------------------------------

GameStart()
PlayGame()




