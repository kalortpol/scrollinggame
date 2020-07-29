from config import cfg
import pygame
from component_handler import component_handler
from time import time


class Mouse:
    def __init__(self):
        # grab mouse
        pygame.event.set_grab(True)

        # cool downs (seconds)
        self.left_cd = 0.5
        self.right_cd = 0.5

        # last click times
        self.last_left_click = 0
        self.last_right_click = 0

    def try_left_click(self) -> bool:
        """
        Returns True if button is off cool down and begins a new cool down
        Returns False if button is on cool down

        :return bool:
        """
        if self.last_left_click > 0:
            if self.last_left_click + self.left_cd < time():
                self.last_left_click = time()
                return True
            elif self.last_left_click == 0:
                self.last_left_click = time()
                return True
            else:
                return False

    def try_right_click(self):
        """
        Returns True if button is off cool down and begins a new cool down
        Returns False if button is on cool down

        :return bool:
        """
        if self.last_right_click > 0:
            if self.last_right_click + self.right_cd < time():
                self.last_right_click = time()
                return True
            elif self.last_right_click == 0:
                self.last_right_click = time()
                return True
            else:
                return False


mouse = Mouse()
