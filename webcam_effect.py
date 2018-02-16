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

frame_width = 0.1
frame_height = 0.1
scale = 0.01

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and frame_width < 0.2:
                frame_width += scale
                frame_height += scale
            elif event.key == pygame.K_RIGHT and frame_width > 0.02:
                frame_width -= scale
                frame_height -= scale
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(utils.BLACK)

    ret, frame = camera.read()
    frame = np.rot90(frame)
    frame = cv2.resize(frame, None, fx=frame_width, fy=frame_height)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    f_width, f_height, f_chan = [float(s) for s in frame.shape]
    cell_w = w_width / f_width
    cell_h = w_height / f_height

    for x, row in enumerate(frame):
        for y, cell in enumerate(row):
            brightness = (int(cell[0]) + int(cell[1]) + int(cell[2])) / 3
            rw = utils.map_value(brightness, 0, 255, 0, cell_w)
            rh = utils.map_value(brightness, 0, 255, 0, cell_h)
            rx = x * cell_w + ((cell_w - rw) / 2)
            ry = y * cell_h + ((cell_h - rh) / 2)
            size = rw * rh
            c = int(utils.map_value(size, 0, cell_w * cell_h, 0, num_colors))
            pygame.draw.rect(screen, colors[c], (rx, ry, rw, rh))

    pygame.display.flip()

camera.release()
cv2.destroyAllWindows()
