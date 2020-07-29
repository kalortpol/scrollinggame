from config import cfg
import pytmx

"""
Helper functions for scrolling
"""


def fetch_tile(point: tuple, tile_size: tuple, map_data: object) -> object:
    """

    :param point:
    :param tile_size:
    :param map_data tmx map data, just pass it right in:
    :return object - tile:
    """
    ts = tile_size
    x = point[0]
    y = point[1]

    # Convert to tilemap coordinate (tmc) and fetch from tilemap
    first_tile_tmc = translate_to_tile_coordinates((x, y), ts)

    # Wow much hack, very elegant
    gti = map_data.__getattribute__("get_tile_image")

    tmx_tile = gti(int(first_tile_tmc[0]), int(first_tile_tmc[1]), 0)

    return tmx_tile


def first_tile(camera_pos: tuple, screen_size: tuple, tile_buffer_size: int, tile_size: tuple) -> tuple:
    """

    :param camera_pos:
    :param screen_size:
    :param tile_buffer_size:
    :param tile_size:
    :return tuple, WORLD COORDINATES:
    """
    tl = get_screen_box_topleft(camera_pos, screen_size[0], screen_size[1])

    firstx = tl[0]
    # make sure firstx is never below 0 (or loading tile from tmx will fail)
    if firstx - (tile_size[0] * tile_buffer_size) >= 0:
        firstx -= (tile_size[0] * tile_buffer_size) >= 0

    firsty = tl[1]
    # make sure firsty is never below 0 (or loading tile from tmx will fail)
    if firsty - (tile_size[1] * tile_buffer_size) >= 0:
        firsty -= (tile_size[1] * tile_buffer_size) >= 0

    x = firstx
    y = firsty

    return int(x), int(y)


def get_screen_box_lower_right(campos: tuple, screen_size: tuple) -> tuple:
    _x = campos[0] + (0.5 * screen_size[0])
    _y = campos[1] + (0.5 * screen_size[1])

    return _x, _y


def translate_to_tile_coordinates(point: tuple, tile_size: tuple) -> tuple:
    """
    Returns coordinates of tile topleft that contains posx, posy
    If topleft is 0,0 in tmx_file

    :param point: world coordinates x, y
    :param tile_size: [x, y]
    :return tuple TILEMAP COORDINATES:
    """
    ts = tile_size

    _rounded_x = point[0] - (point[0] % ts[0])  # rounds down to closest tile_left_x
    _rounded_y = point[1] - (point[1] % ts[1])  # rounds down to closest tile_top_y

    tile_x = _rounded_x / ts[0]
    tile_y = _rounded_y / ts[1]

    tilemap_coord = int(tile_x), int(tile_y)

    #print("[trans. to tile co] input:", point, "output:", tilemap_coord)
    return tilemap_coord


def get_screen_box_topleft(campos: tuple, screen_width: int, screen_height: int) -> tuple:
    """
    Returns topleft corner of the screen-box in world coordinates

    :param campos: should be cfg.camera_pos[x, y]
    :param screen_width: renderer var
    :param screen_height: renderer var
    :return tuple WORLD COORDINATES:
    """
    _camposx = campos[0]
    _camposy = campos[1]

    _topleft = _camposx - (screen_width/2), _camposy - (screen_height/2)

    return _topleft


def get_tile_offset(campos: tuple, tile_size: tuple) -> tuple:
    """
    The difference between pixel position and tile position in world
    :param campos:
    :param tile_size:
    :return:
    """

    c = campos
    ts = tile_size

    offset_x = c[0] % ts[0]
    offset_y = c[1] % ts[1]

    return offset_x, offset_y


def translate_world_to_screen(point: tuple, campos: tuple, screen_width, screen_height, tile_size: tuple) -> tuple:
    """

    :param point:
    :param campos:
    :param screen_width:
    :param screen_height:
    :return tuple, SCREEN COORDINATE:
    """
    tl = get_screen_box_topleft(campos, screen_width, screen_height)
    offset = get_tile_offset(cfg.camera_pos, tile_size)

    x, y = point[0], point[1]
    x += -tl[0]
    y += -tl[1]

    return x, y


def translate_screen_to_world(point: tuple, campos: tuple, screen_size: tuple) -> tuple:
    tl = get_screen_box_topleft(campos, screen_size[0], screen_size[1])
    x, y = point[0] + tl[0], point[1] + tl[1]

    return x, y


def get_tile_area_to_blit(tile_size: tuple, tile_buffer_size: int, map_size: tuple) -> tuple:
    """

    :param screen_size:
    :param tile_size:
    :param tile_buffer_size:
    :param map_size:
    :return starting and ending point of blittable screen area:
    """
    tl = get_screen_box_topleft(cfg.camera_pos, cfg.screen_width, cfg.screen_height)
    tr = get_screen_box_lower_right(cfg.camera_pos, (cfg.screen_width, cfg.screen_height))
    tbs = tile_buffer_size
    ts = tile_size

    # Determine starting point, subtract tile buffer size to begin off-screen
    _start_x = tl[0] - tbs * ts[0]
    _start_y = tl[1] - tbs * ts[1]

    # Add some kind of offset here...
    offset = get_tile_offset(cfg.camera_pos, tile_size)

    _start_x -= int(offset[0])
    _start_y -= int(offset[1])

    # Make sure starting point isn't negative (outside of tilemap)
    # TODO CAUSING NON-SCROLLING BG BUG?
    if _start_x < 0:
        _start_x = 0
    if _start_y < 0:
        _start_y = 0
    #if _start_x >

    # Determine ending point, add tile buffer size to end off-screen
    _end_x = tr[0] + tbs * ts[0]
    _end_y = tr[1] + tbs * ts[1]

    start = int(_start_x), int(_start_y)
    end = int(_end_x), int(_end_y)

    return start, end
