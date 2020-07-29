import pygame
import entities
from renderer import render
from config import cfg
from camera import camera
from component_handler import component_handler
from input import keyboard
from input import mouse


class Main:
    def __init__(self):
        pass

    def startup(self):
        pygame.init()

    def systems(self, state):
        # cfg.running = False
        pass

    def processors(self, state):
        c = component_handler
        if state == 1:
            c.iterate_processor("Life")
            c.iterate_processor("CSprite")
        c.try_move_sprite(2, -1, -1)

    def game_loop(self):
        """
        Full of debug shit

        :return:
        """
        printonce = False
        while cfg.running:

            # first input
            keyboard.event_poller()
            keyboard.keyboard_input(cfg.current_state)

            # then processors
            self.processors(1)

            # update sprite group
            cfg.sprite_group.update()
            self.systems(cfg.current_state)

            # update renderer
            render.update(cfg.current_state)
            camera.center_camera(component_handler.get_cattr_uid("CSprite", 1, "pos"))



engine = Main()
engine.game_loop()
