"""
Renderer.
Scrolling map.
"""

import pygame
import pytmx

from config import cfg
import scrolling_funcs


class Renderer:
    def __init__(self):

        # screen is display field
        self.height, self.width = cfg.screen_width, cfg.screen_height

        self.tile_buffer_size = 2

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        # tile vars
        self.map_data = pytmx.load_pygame("map.tmx")
        self.tile_size = self.map_data.tilewidth, self.map_data.tileheight

        # store map data globally to allow terrain collision
        self.store_map_data()

        # background is the scrolled surface
        self.background = pygame.Surface((5000, 5000))
        #self.background.fill((255, 255, 255))

        # ...caption?
        pygame.display.set_caption("Adventures of Sven")

    def store_map_size(self, state: int) -> None:
        cfg.map_size = self.map_data.width * self.map_data.tilewidth, self.map_data.height * self.map_data.tileheight

    def store_map_data(self):
        cfg.map_data_copy = self.map_data

    def blit_tiles(self):
        map_size = self.map_data.width * self.map_data.tilewidth,\
                   self.map_data.height * self.map_data.tileheight

        # Get world coordinates of start and end point of screen area (+buffer)
        start, end = scrolling_funcs.get_tile_area_to_blit(self.tile_size, self.tile_buffer_size, map_size)

        start_x = start[0]
        end_x = end[0]

        start_y = start[1]
        end_y = end[1]

        # blit column for column
        for x in range(start_x, end_x, self.tile_size[0]):
            for y in range(start_y, end_y, self.tile_size[1]):
                # Fetch tile
                tile_image = scrolling_funcs.fetch_tile((x, y), self.tile_size, self.map_data)

                # Translate to screen coordinate
                screen_coordinate = scrolling_funcs.translate_world_to_screen((x, y),
                                                                              cfg.camera_pos,
                                                                              self.width,
                                                                              self.height,
                                                                              self.tile_size)

                # Blit to screen
                self.background.blit(tile_image,
                                     screen_coordinate)

    def draw_to_screen(self, state):
        # add tiles here ...
        self.screen.blit(self.background, (0, 0))

    def draw_sprites(self, state):
        # Blit sprites in correct positions

        for spr in cfg.sprite_group:
            # Translate world to screen coords
            wc = spr.pos

            sc = scrolling_funcs.translate_world_to_screen(wc,
                                                           cfg.camera_pos,
                                                           cfg.screen_width,
                                                           cfg.screen_height,
                                                           self.tile_size)

            # Blit sprite to screen
            self.background.blit(spr.image, sc)

    def update(self, state):
        self.store_map_size(state)
        self.blit_tiles()
        self.draw_sprites(state)
        self.draw_to_screen(state)

        pygame.display.update()
        pygame.display.flip()


render = Renderer()
