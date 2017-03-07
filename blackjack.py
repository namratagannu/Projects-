#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:06:50 2017

@author: namratagannu
"""

import random

playing = False

chip_pool = 100 

bet = 1

restart_phrase = "Press 'd' to deal the cards again, or press 'q' to quit"

suits = ('H','D','C','S')

ranking = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')

card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.suit + self.rank
    
    def grab_suit(self):
        return self.suit
    
    def grab_rank(self):
        return self.rank
    
    def draw(self):
        print (self.suit + self.rank)
        
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = False
        
    def __str__(self):
        ''' Return a string of current hand composition'''
        hand_comp = ""
        
        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name
            
        return 'The hand has %s' %hand_comp
        
    def card_add(self,card):
        ''' Add another card to the hand'''
        self.cards.append(card)
        

        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]
        
    def calc_val(self):
        '''Calculate the value of the hand, make aces an 11 if they don't bust the hand'''
        if (self.ace == True and self.value < 12):
            return self.value + 10
        else:
            return self.value
        
    def draw(self,hidden):
        if hidden == True and playing == True:
            
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card,len(self.cards)):
            self.cards[x].draw()
            
class Deck:
    
    def __init__(self):
        ''' Create a deck in order '''
        self.deck = []
        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit,rank))
                
    def shuffle(self):
        ''' Shuffle the deck, python actually already has a shuffle method in its random lib '''
        random.shuffle(self.deck)
        
    def deal(self):
        ''' Grab the first item in the deck '''
        single_card = self.deck.pop()
        return single_card
    
    def __str__(self):
        deck_comp = ""
        for card in self.cards:
            deck_comp += " " + deck_comp.__str__()

        return "The deck has" + deck_comp

def make_bet():
    ''' Ask the player for the bet amount and '''
    
    global bet
    bet = 0
    
    print ' What amount of chips would you like to bet? (Enter whole integer please) '
    

    while bet == 0:
        bet_comp = raw_input() 
        bet_comp = int(bet_comp)
       
        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print "Invalid bet, you only have " + str(chip_pool) + " remaining"
            
def deal_cards():
    ''' This function deals out cards and sets up round '''
    
    
    global result,playing,deck,player_hand,dealer_hand,chip_pool,bet
    
    deck = Deck()
    
 
    deck.shuffle()
    
  
    make_bet()
    
    player_hand = Hand()
    dealer_hand = Hand()
    

    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())
    
    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())
    
    result = "Hit or Stand? Press either h or s: "
    
    if playing == True:
        print 'Fold, Sorry'
        chip_pool -= bet
    

    playing = True 
    game_step()
    
    
def hit():
    
    ''' Implement the hit button '''
    global playing,chip_pool,deck,player_hand,dealer_hand,result,bet
    
    if playing:
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())
        
        print "Player hand is %s" %player_hand
        
        if player_hand.calc_val() > 21:
            result = 'Busted! '+ restart_phrase
            
            chip_pool -= bet
            playing = False
    
    else:
        result = "Sorry, can't hit" + restart_phrase
    
    game_step()
    

def stand():
    global playing,chip_pool,deck,player_hand,dealer_hand,result,bet
    ''' This function will now play the dealers hand, since stand was chosen '''
    
    if playing == False:
        if player_hand.calc_val() > 0:
            result = "Sorry, you can't stand!"
            
    else:
      
        while dealer_hand.calc_val() < 17:
            dealer_hand.card_add(deck.deal())
            
           
        if dealer_hand.calc_val() > 21:
            result = 'Dealer busts! You win!' + restart_phrase
            chip_pool += bet
            playing = False
            

        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = 'You beat the dealer, you win!' + restart_phrase
            chip_pool += bet
            playing = False
        
       
        elif dealer_hand.calc_val() == player_hand.calc_val():
            result = 'Tied up, push!' + restart_phrase
            playing = False
        
      
        else:
            result = 'Dealer Wins!' + restart_phrase
            chip_pool -= bet
            playing = False
    game_step()
    
def game_step():
    'Function to print game step/status on output'
    
    
    print ""
    print('Player Hand is: '),
    player_hand.draw(hidden =False)
    
    print 'Player hand total is: '+str(player_hand.calc_val())
    
  
    print('Dealer Hand is: '),
    dealer_hand.draw(hidden=True)
    
   
    if playing == False:
        print  " --- for a total of " + str(dealer_hand.calc_val() )
        print "Chip Total: " + str(chip_pool)
    
    else: 
        print " with another card hidden upside down"
    

    print result
    
    player_input()
    
def game_exit():
    print 'Thanks for playing!'
    exit()
    
def player_input():
    ''' Read user input, lower case it just to be safe'''
    plin = raw_input().lower()
    
    
    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin == 'd':
        deal_cards()
    elif plin == 'q':
        game_exit()
    else:
        print "Invalid Input...Enter h, s, d, or q: "
        player_input()
        
def intro():
    statement = '''Hi guys! Welcome to BlackJack in python! Get as close to 21 as you can without going over!
    Dealer hits until she reaches 17. Aces count as 1 or 11.
    '''
    print statement
    
deck = Deck()

deck.shuffle()

player_hand = Hand()
dealer_hand = Hand()

intro()

deal_cards()