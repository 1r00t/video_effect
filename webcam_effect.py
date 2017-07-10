import pygame
import cv2
import numpy as np
from colors import *


pygame.init()

cap = cv2.VideoCapture(0)

w_size = w_width, w_height = (
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

screen = pygame.display.set_mode(w_size)
pygame.display.set_caption("Kachel Effect")

num_colors = 100
coll = list(reversed(get_c(num_colors)))

fx = 0.0625
fy = 0.0625
scale = 0.03125

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and fx > scale:
                fx -= scale
                fy -= scale
            if event.key == pygame.K_RIGHT and fx <= scale * 6:
                fx += scale
                fy += scale

    screen.fill(BLACK)

    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=fx, fy=fy)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    f_width, f_height, f_chan = frame.shape
    cell_w = w_width / f_width
    cell_h = w_height / f_height

    for x, row in enumerate(frame):
        for y, cell in enumerate(row):
            brightness = (int(cell[0]) + int(cell[1]) + int(cell[2])) / 3
            rw = mapp(brightness, 0, 255, 0, cell_w)
            rh = mapp(brightness, 0, 255, 0, cell_h)
            rx = x * cell_w + ((cell_w - rw) / 2)
            ry = y * cell_h + ((cell_h - rh) / 2)
            size = rw * rh
            c = int(mapp(size, 0, cell_w * cell_h, 0, num_colors))
            pygame.draw.rect(screen, coll[c], (rx, ry, rw, rh))

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
