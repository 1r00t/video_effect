import pygame
import cv2
import numpy as np
import utils

pygame.init()

camera = cv2.VideoCapture(0)

w_size = w_width, w_height = (
    int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))


screen = pygame.display.set_mode(w_size)
pygame.display.set_caption("webcam effect")
pygame.mouse.set_visible(False)

num_colors = 100
colors = utils.get_colors(num_colors)

width_factor = 0.1
height_factor = 0.1
scale = 0.01

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
    if success:
        image = np.rot90(image)
        image = cv2.resize(image, None, fx=width_factor, fy=height_factor)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and width_factor < 0.2:
                width_factor += scale
                height_factor += scale
            elif event.key == pygame.K_RIGHT and width_factor > 0.02:
                width_factor -= scale
                height_factor -= scale
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(utils.BLACK)

    frame = capture_frame()
    f_width, f_height, f_chan = frame.shape
    cell_w = w_width / f_width
    cell_h = w_height / f_height

    for x, row in enumerate(frame):
        for y, cell in enumerate(row):
            draw_cell(cell, (x, y))

    pygame.display.flip()

camera.release()
cv2.destroyAllWindows()
