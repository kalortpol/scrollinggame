import pygame

from config import cfg
import component_handler


def event_poller() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cfg.running = False

        if event.type == pygame.KEYDOWN:
            keydown_input(event)


def keydown_input(event):
    pass


def keyboard_input(state):
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        cfg.running = False

    if pygame.key.get_pressed()[pygame.K_d]:
        component_handler.component_handler.get_cattr_uid("CSprite", 1, "move_queue").append((1, 0))
        #cfg.move_camera(50, 0)

    if pygame.key.get_pressed()[pygame.K_a]:
        component_handler.component_handler.get_cattr_uid("CSprite", 1, "move_queue").append((-1, 0))
        #cfg.move_camera(-50, 0)

    if pygame.key.get_pressed()[pygame.K_w]:
        component_handler.component_handler.get_cattr_uid("CSprite", 1, "move_queue").append((0, -1))
        #cfg.move_camera(0, -1)

    if pygame.key.get_pressed()[pygame.K_s]:
        component_handler.component_handler.get_cattr_uid("CSprite", 1, "move_queue").append((0, 1))
        #cfg.move_camera(0, 1)

    if pygame.key.get_pressed()[pygame.K_p]:
        print("Sprite:", component_handler.component_handler.get_cattr_uid("CSprite", 1, "pos"),
              "Camera:", cfg.camera_pos, "Tile:", cfg.camera_pos[0]/32, cfg.camera_pos[1]/32)

    if pygame.key.get_pressed()[pygame.K_r]:
        component_handler.component_handler.set_cattr_uid("CSprite", 1, "pos", [2800, 2800])  # TODO DEBUG PURPOSE ONLY

    if pygame.key.get_pressed()[pygame.K_n]:
        cfg.current_move_speed += 1

    if pygame.key.get_pressed()[pygame.K_m]:
        cfg.current_move_speed -= 1