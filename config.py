"""
All vars are kept here to be accessible from all modules.
"""

import pygame
import pytmx


class Config:
    def __init__(self):
        """
        Engine vars
        """

        self.running = True                                 # False -> Main loop off

        """
        State vars
        """

        self.states = {1: "main menu",                      # Game states
                       2: "character creation",
                       3: "main game",
                       4: "et c.. add to your liking"}
        self.current_state = self.states[1]                 # Current game state

        """
        Renderer vars
        """
        self.screen_width = 1000
        self.screen_height = 1000
        self.map_size = 0, 0  # updated from renderer. _MEASURED IN PIXELS_
        self.map_data_copy = None

        """
        Scrolling vars
        """
        self.camera_pos = [1000, 1000]
        self.redraw = True

        """
        Component vars
        """
        self.components = {}

        """
        Sprites
        """
        self.sprite_group = pygame.sprite.Group()

        """
        Input
        """

        """
        Global log
        Events can be posted here
        Component processors can read them and take actions
        Don't forget to remove event
        
        format:
        uid: [list of log events in string format]
        """
        self.global_log = dict()

    def post_to_log(self, uid: int, message: str) -> None:
        log = cfg.global_log
        u = uid
        m = message

        if u not in log:
            log[u] = []

        log[u].append(m)
        print(u, "posted", m, "to global log")

    def read_log(self):
        return self.global_log

    def read_log_uid(self, uid: int) -> list:
        try:
            return self.global_log[uid]

        except KeyError:
            return []


cfg = Config()
