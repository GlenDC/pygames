"""
pingrunner.py is an infinite runner inspired by the
POSIX ping command and written in Python3 using Pygame 2.0.0.dev6.

License: MIT
Author: Glen De Cauwsemaecker
        contact@glendc.com
"""

from abc import ABC, abstractmethod
import os
from dataclasses import dataclass
from typing import List, Tuple

import pygame


class GameObject(ABC):
    """
    Base class for all Game Objects
    """

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
        """
        Optional method, to be implemented in case
        the game object requires to be drawn.
        """
        pass


@dataclass
class Hero(GameObject):
    pos: Tuple[int, int]
    width: int
    height: int

    def draw(self, ctx):
        pygame.draw.rect(ctx.screen, (0, 0, 0), self.get_rect())

    def handle_event(self, ctx, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(self.pos, width=5, height=10, speed=3)
            ctx.game_objects.append(bullet)

    def update(self, ctx):
        pressed = pygame.key.get_pressed()
        x, y = self.pos
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
        self.pos = (x, y)

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.width/2,
            self.pos[1] - self.height/2,
            self.width, self.height,
        )


@dataclass
class Bullet(GameObject):
    pos: Tuple[int, int]
    width: int
    height: int
    speed: int

    def draw(self, ctx):
        pygame.draw.rect(ctx.screen, (0, 200, 0), self.get_rect())

    def update(self, ctx):
        # move bullet
        pressed = pygame.key.get_pressed()
        x, y = self.pos
        y -= self.speed
        self.pos = (x, y)

        # TODO: destroy when from screen

        # kill all enemies in my path
        destroyed = False
        mob = None
        for game_object in ctx.game_objects:
            if isinstance(game_object, Mob):
                mob = game_object
                break
        for idx, game_object in enumerate(mob.members):
            rect = self.get_rect()
            enemy_rect = game_object.get_rect()
            if rect.colliderect(enemy_rect):
                # DESTROY HIM
                del mob.members[idx]
                destroyed = True
                break
        if destroyed:
            for idx, game_object in enumerate(ctx.game_objects):
                if game_object is self:
                    del ctx.game_objects[idx]
                    break


    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.width/2,
            self.pos[1] - self.height/2,
            self.width, self.height,
        )


@dataclass
class Enemy(GameObject):
    pos: Tuple[int, int]
    width: int
    height: int
    previous_x: int = 0

    def draw(self, ctx):
        pygame.draw.rect(ctx.screen, (200, 0, 0), self.get_rect())

    def update(self, ctx):
        self.previous_x = self.pos[0]

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.width/2,
            self.pos[1] - self.height/2,
            self.width, self.height,
        )


@dataclass
class Mob(GameObject):
    members: List[Enemy]
    speed: int
    offset: int

    def draw(self, ctx):
        for member in self.members:
            member.draw(ctx)

    def handle_event(self, ctx, event):
        for member in self.members:
            member.handle_event(ctx, event)

    def update(self, ctx):
        for member in self.members:
            x, y = member.pos
            x = (x + self.speed) % ctx.screen.get_rect().width

            if member.previous_x > x:
                y += self.offset
            member.pos = (x, y)

            member.update(ctx)


@dataclass
class GameContext:
    """
    Context that objects and the world use to
    know how to handle events and display the content to the screen.
    """
    screen: object
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
    background.fill((225, 225, 225))
    ctx.screen.blit(background, (0, 0))

    # draw all game objects
    for game_object in ctx.game_objects:
        game_object.draw(ctx)

    # flip the screen and display it all
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption('Space Invader')

    # create the initial context,
    # context can be updated ad-hoc in handle_event,
    # dirty indeed
    ctx = GameContext(
        screen=pygame.display.set_mode((400, 300)),
        clock=pygame.time.Clock(),
        font=pygame.font.Font(pygame.font.get_default_font(), 12),
        game_objects=[
            Hero(
                pos=(200, 275),
                width=50, height=20,
            ),
            Mob(
                members=[
                    Enemy(
                        pos=(5, 5),
                        width=35, height=35,
                    ),
                    Enemy(
                        pos=(55, 5),
                        width=35, height=35,
                    ),
                    Enemy(
                        pos=(105, 5),
                        width=35, height=35,
                    ),
                    Enemy(
                        pos=(155, 5),
                        width=35, height=35,
                    ),
                    Enemy(
                        pos=(205, 5),
                        width=35, height=35,
                    ),
                ],
                speed=3,
                offset=40,
            ),
        ],
    )

    # start the game
    while True:
        for event in pygame.event.get():
            handle_event(ctx, event)
        update(ctx)
        draw(ctx)
        ctx.clock.tick(60)
