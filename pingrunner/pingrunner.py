"""
pingrunner.py is an infinite runner inspired by the
POSIX ping command and written in Python3 using Pygame 2.0.0.dev6.

License: MIT
Author: Glen De Cauwsemaecker
        contact@glendc.com
"""

import os
from dataclasses import dataclass, field
from typing import List, Tuple

import pygame


@dataclass
class Vec2D:
    x: int = 0
    y: int = 0


@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255

    def tuple(self):
        return (
            max(0, min(self.r, 255)),
            max(0, min(self.g, 255)),
            max(0, min(self.b, 255)),
        )


@dataclass
class GameObject:
    """
    Base class for all Game Objects

    width and height expressed in units
    """

    pos: Vec2D = field(default_factory=Vec2D)
    width: int = 1
    height: int = 1
    color: Color = field(default_factory=Color)

    def handle_event(self, ctx, event):
        """
        Optional method, to be implemented in case
        the game object requires at least one event to be handled for it.
        """
        pass

    def update(self, ctx):
        """
        Optional method, to be implemented in case
        the game object requires update logic not bound to a specific event.
        """
        pass

    def draw(self, ctx):
        pygame.draw.rect(ctx.screen, self.color.tuple(), self.get_rect(ctx))

    def get_rect(self, ctx):
        screen_rect = ctx.screen.get_rect()
        height = self.height*ctx.unit_size
        return pygame.Rect(
            # for this game it's easiest to have coords start at bottom left
            self.pos.x*ctx.unit_size,
            screen_rect.height - (self.pos.y*ctx.unit_size + ctx.menu_height) - height,
            self.width*ctx.unit_size, height,
        )


@dataclass(init=False)
class Hero(GameObject):
    def __init__(self):
        super().__init__()

        self.color = Color(r=65, g=255, b=0)
        self.pos.x = 2
        self.width = 1
        self.height = 2

        self.acceleration = 0

    def update(self, ctx):
        # jump if can
        pressed = pygame.key.get_pressed()
        if self.pos.y == 0 and pressed[pygame.K_SPACE]:
            self.acceleration = 0.6

        # compute height movement, if in jump-mode
        if self.acceleration != 0:
            # decrease height acceleration of player using the gravity
            self.acceleration -= ctx.gravity / max(1, ctx.clock.get_fps())
            self.pos.y += self.acceleration

            # land on the ground, yay,
            # landing in a gap is not something we control here,
            # but the gap instead will collide with the player, think about that :)
            if self.pos.y <= 0:
                self.pos.y = 0
                self.acceleration = 0


@dataclass
class GameContext:
    """
    Context that objects and the world use to
    know how to handle events and display the content to the screen.
    """
    screen: object
    menu_height: int
    unit_size: int
    gravity: int
    speed: int
    clock: pygame.time.Clock
    font: pygame.font.Font
    game_objects: List[GameObject]


def handle_event(ctx, event):
    if event.type == pygame.QUIT:
        print("Bye!")
        exit(0)

    # update all game objects
    for game_object in ctx.game_objects:
        game_object.handle_event(ctx, event)


def update(ctx):
    for game_object in ctx.game_objects:
        game_object.update(ctx)


def draw(ctx):
    # wipe screen
    background = pygame.Surface(ctx.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    ctx.screen.blit(background, (0, 0))

    # draw all game objects
    for game_object in ctx.game_objects:
        game_object.draw(ctx)

    # flip the screen and display it all
    pygame.display.flip()


#################### main ########################

pygame.init()
pygame.display.set_caption('pingrunner')

# create the initial context,
# context can be updated ad-hoc in handle_event,
# dirty indeed
ctx = GameContext(
    screen=pygame.display.set_mode((480, 200)),
    menu_height=75,
    unit_size=(200 - 75) / 10,  # (screen_height - menu_height) / 8
    gravity=1.75,
    speed=1,
    clock=pygame.time.Clock(),
    font=pygame.font.Font(pygame.font.get_default_font(), 12),
    game_objects=[
        Hero(),
    ],
)

# start the game
while True:
    for event in pygame.event.get():
        handle_event(ctx, event)
    update(ctx)
    draw(ctx)
    ctx.clock.tick(60)
