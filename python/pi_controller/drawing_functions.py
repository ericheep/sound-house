import pygame

def draw_slider():
    # need to define by bottom/top attributes
    slider = pygame.draw.rect(screen, slider_color, (10, 10, slider_w, slider_h), 0)
    knob = pygame.draw.rect(screen, knob_color, (10, knob_pos, slider_w, knob_h), 0)
    return slider, knob

def check_slider(knob_pos):
    knob_clicked = slider.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        knob_moving = True
        knob_pos = mouse_y
    else:
        knob_moving = False
    return knob_moving, knob_pos

pygame.init()

screen = pygame.display.set_mode(
    (400, 400))
pygame.display.set_caption("Sound House Pi Controller")

slider_color = (100, 100, 100)
knob_color = (255, 0, 0)
slider_h = 100
slider_w = 20
knob_h = 10
knob_pos = slider_h

knob_moving = False

done = False

while not done:

    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            knob_moving, knob_pos = check_slider(knob_pos)
            slider_value = slider_h - knob_pos
            print(slider_value)
        elif event.type == pygame.MOUSEBUTTONUP:
            knob_moving = False
        elif knob_moving:

            if knob_pos <= slider_h + 10: #offset variable
                knob_pos = mouse_y
            else:
                knob_pos = slider_h
                knob_moving = False
            slider_value = slider_h - knob_pos
            print(slider_value)

    screen.fill((0, 0, 0))
    slider, knob = draw_slider()

    pygame.display.flip()

pygame.quit()