from collections import namedtuple
import pygame


CardTuple = namedtuple('Card', ['value', 'suit'])

card_values = ['2', '3', '4', '5', '6', '7', 'Queen', 'Jack', 'King', 'Ace']

card_suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

points = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':10, 'Queen':2, 'Jack':3, 'King':4, 'Ace':11}

suits_emoji = {'Spades':'♠️','Hearts': '♥️', 'Clubs':'♣️', 'Diamonds':'♦️'}



class Card:
    def __init__(self, input_value, input_suit):
        self.data = CardTuple(value=input_value, suit=input_suit)
        self.id = f'{self.data.value[0]}{self.data.suit[0]}'
        self.id_emoji = f'{self.data.value[0]}{suits_emoji[self.data.suit]}'
        self.rank = card_values.index(input_value)
        self.score = points[input_value]
        self.image = pygame.image.load(f'graphics/{self.id}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()/6), int(self.image.get_height()/6)))
        self.rect = self.image.get_rect()

    
    def __str__(self):
        return self.id_emoji

        