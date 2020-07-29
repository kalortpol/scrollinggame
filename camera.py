from config import cfg


class Camera:
    def __init__(self):
        pass

    def move_camera(self, x, y):
        ss = cfg.screen_width, cfg.screen_height
        cp = cfg.camera_pos

        cpx = cp[0]
        cpy = cp[1]

        cpx += x
        cpy += y

        if cpx - x < ss[0] / 2 + 64:
            cpx = int(ss[0] / 2)

        if cpy - y < ss[1] / 2 + 64:
            cpy = int(ss[1] / 2)

        cfg.camera_pos[0] = cpx
        cfg.camera_pos[1] = cpy

    def center_camera(self, pos):
        """
        Note that if scrolling is done with high enough speed,
        camera will close enough to world edge to cause an index error
        in the tile fetching.

        However, it is completely safe for normal speeds (1-10 pixels/frame)

        :param pos:
        :return:
        """
        x, y = pos
        map_size = cfg.map_size
        screen_size = cfg.screen_width, cfg.screen_height

        left_max = screen_size[0] / 2 + 200
        right_max = map_size[0] - (screen_size[0] / 2) - 200
        top_max = screen_size[1] / 2 + 200
        bot_max = map_size[1] - (screen_size[1] / 2) - 200

        # limit camera to slightly more than half a screen from world border (tiles are not drawn correctly)
        if x < left_max:
            print("[Center camera] Edge reached!:", pos, "map_size:", map_size)
            x = left_max
        if x > right_max:
            print("[Center camera] Edge reached!:", pos, "map_size:", map_size)
            x = right_max
        if y < top_max:
            print("[Center camera] Edge reached!:", pos, "map_size:", map_size)
            y = top_max
        if y > bot_max:
            print("[Center camera] Edge reached!:", pos, "map_size:", map_size)
            y = bot_max

        cfg.camera_pos = x, y


camera = Camera()
