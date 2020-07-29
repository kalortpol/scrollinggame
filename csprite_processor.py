import pygame
from processors import processor_base
from config import cfg


class CSpriteProcessor(processor_base.CProcessor):
    """
    Functionality: TODO document all functionality
    """
    def __init__(self):
        super().__init__()
        self.component_name = "CSprite"

    def private_process(self, component):
        self.master_movement_method(component)

    """
    Helper methods
    """
    def get_component_instances(self):
        clist = cfg.components["CSprite"]

        return clist
    """
    Collision methods
    """

    def determine_if_on_screen(self, component) -> bool:
        """
        Checks if component (that is CSprite) has a pos that is on screen or not
        This is done to be able to collide check/perform other actions on only on-screen
        sprites to improve performance.

        Working :)

        :param component:
        :return:
        """

        # make ranges that describe x- and y-coordinates on screen
        start_range = cfg.camera_pos[0] - (cfg.screen_width / 2), cfg.camera_pos[1] - (cfg.screen_height / 2)
        end_range = cfg.camera_pos[0] + (cfg.screen_width / 2), cfg.camera_pos[1] + (cfg.screen_height / 2)

        # make sure they are int, int
        xrange = range(int(start_range[0]), int(end_range[0]))
        yrange = range(int(start_range[1]), int(end_range[1]))

        if int(component.pos[0]) in xrange and int(component.pos[1]) in yrange:
            return True
        else:
            #print("NOT on screen pos:", component.pos[0], component.pos[1], "range:", xrange, yrange)
            return False

    def determine_if_collide_check(self, component):
        """
        1. check if it has collide = True
        2. check if on screen
        4. handle collision detection is separate method

        :param component:
        :return:
        """

        # check if component will move at the end of frame
        # if it's not about to move, no point in collision
        # detection
        # if it gets hit by something the moving sprite will
        # detect the collision anyway
        if len(component.move_queue) > 0:

            # check if component has collide first, because this operation
            # is cheaper than checking if it is on screen
            if self._has_collide(component):

                # only carry on if component is also on screen
                if self.determine_if_on_screen(component):
                    # start collision checking
                    self.perform_collision_checks(component)
             #   else:
            #        print("COLLISION NOT CHECKED [DETERMINE_IF_SCREEN]")
           # else:
          #      print("COLLISION NOT CHECKED [_HAS_COLLIDE]")
        #else:
         #   print("COLLISION NOT CHECKED [QUEUE_LENGTH]")

    def _has_collide(self, component):
        if component.collide:
            return True
        else:
            return False

    def determine_tile_terrain_type(self, x, y):
        tile_x = (x - (x % cfg.map_data_copy.tilewidth)) / cfg.map_data_copy.tilewidth
        tile_y = (y - (y % cfg.map_data_copy.tileheight)) / cfg.map_data_copy.tileheight

        # get the properties for the next tile
        props = cfg.map_data_copy.get_tile_properties(tile_x, tile_y, 0)
        #print(int(tile_x), int(tile_y), "properties:", props)

        # and return them...
        return props["type"]

    def terrain_collide(self, component):
        #print("[terrain collide]")
        # retrieve map data
        md = cfg.map_data_copy

        # get next_pos and make ghost rect
        newpos = self._next_pos(component)
        comp_rect = component.rect.copy()
        comp_rect.center = newpos

        # get tile_type
        tile_type = self.determine_tile_terrain_type(newpos[0], newpos[1])
        #print(tile_type)

        # make a tile rect
        # calculate x and y position of tile
        tile_x = int((newpos[0] - (newpos[0] % cfg.map_data_copy.tilewidth)) / cfg.map_data_copy.tilewidth)
        tile_y = int((newpos[1] - (newpos[1] % cfg.map_data_copy.tileheight)) / cfg.map_data_copy.tileheight)

        tile_rect = pygame.rect.Rect(tile_x, tile_y, cfg.map_data_copy.tilewidth, cfg.map_data_copy.tileheight)
        #print(tile_rect, tile_type)

        if component.terrain_move_speed[tile_type] == 0:
            #print("Collide! Should stop")
            component.move_queue.clear()
            #print("Move queue after collide:", component.move_queue)

    def collision_adjust_move_queue(self, component_a, next_pos_a, component_b, next_pos_b):
        """
        TODO: If sprite is blocked, try only removing the x, and y that cause it to get blocked

        Use below code, but also for sprite_b and make a method to adjust the move_queues so they
        don't collide ...
        """

        # component a

        delta_a_sign_x = None  # is delta_x positive or negative?
        delta_a_sign_y = None  # is delta_y positive or negative?

        delta_a = [component_a.pos[0] - next_pos_a[0], component_a.pos[1] - next_pos_a[1]]  # list(delta_x, delta_y)

        delta_a_sign_x = "positive" if delta_a[0] > 0 else "negative"
        delta_a_sign_y = "positive" if delta_a[1] > 0 else "negative"

        # component b

        delta_b_sign_x = None  # is delta_x positive or negative?
        delta_b_sign_y = None  # is delta_y positive or negative?

        delta_b = [component_b.pos[0] - next_pos_b[0], component_b.pos[1] - next_pos_b[1]]  # list(delta_x, delta_y)

        delta_b_sign_x = "positive" if delta_a[0] > 0 else "negative"
        delta_b_sign_y = "positive" if delta_a[1] > 0 else "negative"

        # compare destinations
        # TODO
        """
        Compare destinations, and try to remove movement from component_a and test again if that avoids
        the collision.
        If this doesn't help, also stop component_b.
        If this doesn't help, slightly adjust both component_a and component_b positions, but check them
        for collisions with terrain or other sprites of course when trying to do this. Do this by checking
        if component_a has a smaller x, y than component_b. If true -> make it even smaller by decreasing
        component_a x,y. If False -> slightly increase component_a x, y. Then test for collision again. If it doesnt
        help, do the same for component_b.
        If nothing of the above is enough, a rescue procedure is required to keep them from getting stuck in eachother
        """

    def sprite_collide(self, component):
        """
        Collision detection between sprites.
        1. Get next position for self sprite and all other sprites
        2. Compare these positions, and if they overlap, don't allow either to move

        :param component:
        :return:
        """
        # get all sprites
        clist = self.get_component_instances()

        # determine where self sprite will move to
        newpos_a = self._next_pos_multiplied(component)

        for x in clist:

            # don't check against self
            if x.uid != component.uid:

                # determine where other sprite will move to
                newpos_b = self._next_pos(x)

                # create ghost rects to compare
                rect_a = component.rect.copy()
                rect_a.center = newpos_a

                rect_b = component.rect.copy()
                rect_b.center = newpos_b

                if rect_a.colliderect(rect_b):
                    # determine if collision can be avoided by slight changes in move queues
                    self.collision_adjust_move_queue(component, newpos_a, x, newpos_b)
                    print(component.uid, "collided with", x.uid)
                    component.move_queue.clear()

    def _next_pos(self, component):
        """
        Determine what position the sprite will move to after all move-orders are performed

        :param component:
        :return:
        """
        posx = component.pos[0]
        posy = component.pos[1]

        mq = component.move_queue.copy()

        while len(mq) > 0:
            x, y = mq.pop()

            posx += x
            posy += y

        return posx, posy

    def _next_pos_multiplied(self, component):
        """
        Determine what position the sprite will move to after all move-orders are performed
        Multiplied to prevent sprites from getting stuck in each-other

        :param component:
        :return:
        """
        posx = component.pos[0]
        posy = component.pos[1]

        mq = component.move_queue.copy()

        while len(mq) > 0:
            x, y = mq.pop()

            posx += x * 4
            posy += y * 4

        return posx, posy

    def perform_collision_checks(self, component):
        self.terrain_collide(component)
        self.sprite_collide(component)

    """
    Movement methods
    """
    def master_movement_method(self, component):
        """
        All movement related methods need to be called from here.

        Currently:
        * Collision handling: (1) Terrain [done], (2) Sprites [done]
        * Committing movement = adding move queue to position [done]
        * Different move speeds on different terrains [done]
            - values stored in component.terrain_move_speed
            - unlimited scalability

        :param component:
        :return:
        """
        if len(component.move_queue) > 0:
            self.determine_if_collide_check(component)
            self.flush_move_queue(component)

    def flush_move_queue(self, component):
        """
        Commits all the movement queued.
        Queue will be empty if movement would have led to a collision.

        :param component:
        :return:
        """
        mq = component.move_queue

        # first determine what terrain is under feet
        component.current_terrain_type_under_feet = self.determine_tile_terrain_type(component.pos[0], component.pos[1])
        move_speed_modifier = component.terrain_move_speed[component.current_terrain_type_under_feet]
        #print("terrain:", component.current_terrain_type_under_feet, "move speed modifier:", move_speed_modifier)

        # print("Component:", component.uid, "move_queue:", mq)

        total_x = 0
        total_y = 0

        # print(total_x, total_y)

        while len(mq) > 0:
            x, y = mq.pop()
            total_x += x
            total_y += y

        # print("after loop:", total_x, total_y)

        # prevent move_speed_modifier from reaching 0 (or else sprites get stuck)
        if move_speed_modifier == 0:
            move_speed_modifier = 0.1

        # print("old component pos:", component.pos[0], component.pos[1])
        component.pos[0] += (total_x * move_speed_modifier)
        component.pos[1] += (total_y * move_speed_modifier)

        # print("new component pos:", component.pos[0], component.pos[1])


csp = CSpriteProcessor()
