import pygame
from card import *
import random

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
BG = (33, 124, 66)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bisca')

def draw_bg():
    screen.fill(BG)

#set framerate
clock = pygame.time.Clock()
FPS = 60

class Player:

    def __init__(self, last_winner):
        self.hand = []
        self.last_winner = last_winner
    
    def draw_cards(self):
        
        for i,card in enumerate(self.hand):
            card.rect.center = (int(SCREEN_WIDTH/len(self.hand)) * i + 80 , 500)
            screen.blit(pygame.transform.flip(card.image, False, False), card.rect)

    def card_pressed(self):
        for i,card in enumerate(self.hand):
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                print(card)
                card.rect.move_ip(100,100)
                




class Game:
    def __init__(self):
        self.deck = self.generate_deck()
        self.p1 = Player(True)
        self.p2 = Player(False)
        for i in range(5):
            self.p1.hand.append(self.deck.pop(-1))
            self.p2.hand.append(self.deck.pop(-1))


    def generate_deck(self):
        fresh_deck = []
        for value in  card_values:
            for suit in card_suits:
                fresh_deck.append(Card(value, suit))
        random.shuffle(fresh_deck)
        return fresh_deck
        

g = Game()

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    g.p1.draw_cards()
    

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                g.p1.card_pressed()


    pygame.display.update()
pygame.quit()    