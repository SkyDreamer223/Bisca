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

# Set framerate
clock = pygame.time.Clock()
FPS = 60


class Player:
    def __init__(self, last_winner, is_bot=False):
        self.hand = []
        self.last_winner = last_winner
        self.is_bot = is_bot
        self.selected_card = None
        self.target_position = None
        self.animation_speed = 20  # Pixels per frame
        self.animation_cooldown = 0  # Cooldown timer in frames

    def draw_cards(self):
        for card in self.hand:
            screen.blit(pygame.transform.flip(card.image, False, False), card.rect)


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
                print(self.target_position)
                self.selected_card = None
                self.target_position = None
            else:
                # Move the card
                card.rect.centerx += delta_x * self.animation_speed / distance
                card.rect.centery += delta_y * self.animation_speed / distance
    def card_pressed(self):
        if self.is_bot or self.animation_cooldown > 0:
            return False
        for card in self.hand:
            x = -150 if self.last_winner else 150 
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                print(f"Card pressed: {card}")
                self.selected_card = card
                self.target_position = (SCREEN_WIDTH // 2 + x, SCREEN_HEIGHT // 2)
                self.animation_cooldown = 60  # Set cooldown to 60 frames (1 seconds at 60 FPS)
                return True
        return False
    
    def bot_play_card(self):
        if self.is_bot and not self.selected_card and self.animation_cooldown <= 0:
            x = -150 if self.last_winner else 150
            if self.hand:
                self.selected_card = self.hand[random.randint(0, len(self.hand) - 1)]
                self.target_position = (SCREEN_WIDTH // 2 + x, SCREEN_HEIGHT // 2)
                print(f"Bot played: {self.selected_card}")
                self.animation_cooldown = 60  # Set cooldown to 60 frames (1 seconds at 60 FPS)

    def update_cooldown(self):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= 1

class Game:
    def __init__(self):
        self.deck = self.generate_deck()
        self.p1 = Player(True)  # Human player
        self.p2 = Player(False, is_bot=True)  # Bot player
        self.deal_initial_cards()
        self.current_turn = self.p1 if self.p1.last_winner else self.p2  # Set the first turn based on the last winner
        self.animation_cooldown = 0
    
    def draw_deck(self):
        #screen.blit(pygame.transform.scale(card_back, (card_back.get_width() // 4, card_back.get_height() // 4)), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 70))
        pass


    def update_cooldowns(self):
        self.p1.update_cooldown()
        self.p2.update_cooldown()
    
    def sum_cooldowns(self):
        return self.p1.animation_cooldown + self.p2.animation_cooldown
    def generate_deck(self):
        fresh_deck = []
        for value in card_values:
            for suit in card_suits:
                fresh_deck.append(Card(value, suit))
        random.shuffle(fresh_deck)
        return fresh_deck

    def deal_initial_cards(self):
        for _ in range(5):
            self.p1.hand.append(self.deck.pop(-1))
            self.p2.hand.append(self.deck.pop(-1))
        self.set_initial_positions(self.p1.hand)
        self.set_initial_positions(self.p2.hand, is_bot=True)

    def set_initial_positions(self, hand, is_bot=False):
        for i, card in enumerate(hand):
            y_pos = 500 if not is_bot else 0
            card.rect.center = (int(SCREEN_WIDTH / len(hand)) * i + 80, y_pos)

    def switch_turn(self):
        self.current_turn = self.p1 if self.current_turn == self.p2 else self.p2

g = Game()

run = True

while run:
    clock.tick(FPS)
    draw_bg()
    g.p2.update_animation()
    g.p1.update_animation()
    g.p2.draw_cards()
    g.p1.draw_cards()
    g.update_cooldowns()
    

    if not g.current_turn.selected_card:
        if g.current_turn.is_bot and g.sum_cooldowns() <= 0:
            g.p2.bot_play_card()
            g.switch_turn()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and g.current_turn == g.p1 and g.sum_cooldowns() <= 0:
                if g.current_turn.card_pressed():
                    g.switch_turn()

    pygame.display.update()
pygame.quit()