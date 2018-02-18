import pygame
import cv2
import numpy as np
import utils

pygame.init()

camera = cv2.VideoCapture(0)

screen_mode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN

screen = pygame.display.set_mode((0, 0), screen_mode)
screen_width, screen_height = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h
)

pygame.display.set_caption("webcam effect")
pygame.mouse.set_visible(False)

num_colors = 100
colors = utils.generate_palette(num_colors)

scale = 0.1
scale_stepping = 0.01

running = True


def calculate_cell_parameters(cell_info):
    brightness = (int(cell_info[0]) + int(cell_info[1]) + int(cell_info[2])) / 3
    width = utils.rescale(brightness, 0, 255, 0, cell_w)
    height = utils.rescale(brightness, 0, 255, 0, cell_h)
    return width, height


def draw_cell(cell_info, position):
    rw, rh = calculate_cell_parameters(cell_info)
    rx = position[0] * cell_w + ((cell_w - rw) / 2)
    ry = position[1] * cell_h + ((cell_h - rh) / 2)
    size = rw * rh
    c = int(utils.rescale(size, 0, cell_w * cell_h, 0, num_colors))
    pygame.draw.rect(screen, colors[c], (rx, ry, rw, rh))


def capture_frame():
    success, image = camera.read()
    if not success:
        raise RuntimeError('Could not read image from camera.')
    image = np.rot90(image)
    image = cv2.resize(image, None, fx=scale, fy=scale)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def change_scale(key, scale):
    new_scale = scale
    if key == pygame.K_LEFT and scale < 0.2:
        new_scale += scale_stepping
    elif key == pygame.K_RIGHT and scale > 0.02:
        new_scale -= scale_stepping
    return new_scale


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            scale = change_scale(event.key, scale)
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(pygame.color.THECOLORS['black'])

    frame = capture_frame()
    f_width, f_height = frame.shape[:2]
    cell_w = screen_width / f_width
    cell_h = screen_height / f_height

    for x, row in enumerate(frame):
        for y, cell in enumerate(row):
            draw_cell(cell, (x, y))

    pygame.display.flip()

camera.release()
cv2.destroyAllWindows()