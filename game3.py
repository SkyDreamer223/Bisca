import pygame
from card import *
import random

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
BG = (33, 124, 66)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bisca')

def draw_bg():
    screen.fill(BG)

# Set framerate
clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self, last_winner, is_bot, positions, bag_position):
        self.hand = []
        self.last_winner = last_winner
        self.is_bot = is_bot
        self.selected_card = None
        self.target_position = None
        self.animation_speed = 20  # Pixels per frame
        self.animation_cooldown = 0  # Cooldown timer in frames
        self.last_position = None
        self.positions = positions
        self.bag = []
        self.bag_position = bag_position
    
    def render_hand(self):
        for card in self.hand:

            if card.visible:
                screen.blit(pygame.transform.scale(card.image, (card.image.get_width(), card.image.get_height())), card.rect)
            else:
                screen.blit(pygame.transform.scale(card.back_image, (card.back_image.get_width(), card.back_image.get_height())), card.rect)
    
    def play_card(self, card):
        self.selected_card = card
        card.visible = True
        self.target_position = (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))
        self.animation_cooldown = 30
        self.last_position = self.selected_card.rect.center
    

    def update_animation(self):
        if self.selected_card and self.target_position:
            card = self.selected_card
            target_x, target_y = self.target_position

            # Calculate the distance to move
            delta_x = target_x - card.rect.centerx
            delta_y = target_y - card.rect.centery

            distance = (delta_x ** 2 + delta_y ** 2) ** 0.5

            if distance < self.animation_speed:
                card.rect.center = self.target_position
                self.selected_card = None
                self.target_position = None
                
            else:
                # Move the card
                card.rect.centerx += delta_x * self.animation_speed / distance
                card.rect.centery += delta_y * self.animation_speed / distance


class Game:
    def __init__(self):
        self.deck = self.generate_deck()
        self.p1 = Player(True, False, [(200, 700),(350,700),(500,700),(650,700),(800,700)], (SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        self.p2 = Player(False, True, [(200, 100),(350,100),(500,100),(650,100),(800,100)], (SCREEN_WIDTH//2, SCREEN_HEIGHT + 100))
        self.trump = self.deck[0]
        self.trump.visible = True
        #turn trump card 90 degrees in its center axis
        self.trump.image = pygame.transform.rotate(self.trump.image, 90)
        self.round_in_progress = False
        self.animation_cooldown = 0
        self.table = []
        self.table_positions = [(300, 300), (400, 300)]

        
    
    
        

    def generate_deck(self):
        fresh_deck = []
        for value in  card_values:
            for suit in card_suits:
                fresh_deck.append(Card(value, suit))
        random.shuffle(fresh_deck)
        return fresh_deck
    
    def render_deck(self):
        for card in self.deck:
            card.rect.center = (100, int(SCREEN_HEIGHT/2))
            if card.visible:
                #render card
                card.rect.move_ip(25, 25)
                screen.blit(pygame.transform.scale(card.image, (card.image.get_width(), card.image.get_height())), card.rect)
            else:
                #render back
                screen.blit(pygame.transform.scale(card.back_image, (card.back_image.get_width(), card.back_image.get_height())), card.rect)
    def deal_p1(self):
        card = self.deck.pop(-1)
        card.visible = True
        self.p1.hand.append(card)
        self.p1.selected_card = card
        print(len(self.p1.hand))
        self.p1.target_position = self.p1.positions[len(self.p1.hand)-1]
        self.animation_cooldown = 30
    
    def deal_p2(self):
        card = self.deck.pop(-1)
        self.p2.hand.append(card)
        self.p2.selected_card = card
        self.p2.target_position = self.p2.positions[len(self.p2.hand)-1]
        self.animation_cooldown = 30
    
    def deal_cards(self):
        if len(self.p1.hand) == len(self.p2.hand) and len(self.p1.hand) < 5:
            if self.p1.last_winner:
                self.deal_p1()
            else:
                self.deal_p2()
        elif len(self.p1.hand) > len(self.p2.hand):
            self.deal_p2()
        else:
            self.deal_p1()
    
    def update_cooldowns(self):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= 1
                   



g = Game()

run = True

while run:
    
    clock.tick(FPS)
    draw_bg()
    g.render_deck()
    g.p1.render_hand()
    g.p2.render_hand()
    if not g.round_in_progress and not g.animation_cooldown:
        if min(len(g.p1.hand), len(g.p2.hand)) < 5 and g.deck and not g.animation_cooldown:
            g.deal_cards()
            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for card in g.p1.hand:
                    if card.rect.collidepoint(pygame.mouse.get_pos()):
                        g.p1.play_card(card)
    
    g.p1.update_animation()
    g.p2.update_animation()
    g.update_cooldowns()
    
    pygame.display.update()

