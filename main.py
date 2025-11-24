import pygame, os
pygame.init()

from math import sin

#YOU MAY CHANGE THE WIDTH BUT NOT HEIGHT OR WH_RATIO
WH_RATIO = 5/7
W = 1400         
H = int(W * WH_RATIO)

# Display
FPS = 60
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Interactive blackjack")

# Cursor 
mouse_mask = pygame.mask.Mask((1, 1), True)

# Get Images
file_name = os.path.basename(__file__)
assets_path = os.path.abspath(__file__)[:-len(file_name)] + "assets\\"

def make_image(name, size):
    return pygame.transform.scale(pygame.image.load(assets_path + name), size)


# Hovering check (Only works on Rects)
def check_hover(mouse_xcor, mouse_ycor, surface_xcor, surface_ycor, surface_width, surface_height):
    if surface_xcor <= mouse_xcor <= surface_xcor + surface_width: # Check X range
        if surface_ycor <= mouse_ycor <= surface_ycor + surface_height: # Check Y range
            return True
    return False


# Loading screen
def load(clock:pygame.time.Clock, make_image:callable, mouse_mask:pygame.mask.Mask):
    # General
    running = True
    frame = 0

    # Images
        # BG
    bg = make_image("bg.png", (W,H))
    bg_title = make_image("bg title.png", (W, H))
    title_jiggle_speed = 0.1875
    title_sine_amplitude = 5

        # Play Button
    play_button_dimensions = ( W / 5, W / 10)
    play_button = make_image("play button.png", play_button_dimensions)
    play_button_fixed_cors = ( W / 2 - play_button_dimensions[0] / 2, H / 3 * 2)
    play_button_mask = pygame.mask.from_surface(play_button)

        # Hovered Play Button
    hovering_enlargement = 1.1
    play_button_hovered = pygame.transform.scale(play_button, (play_button_dimensions[0] * hovering_enlargement, play_button_dimensions[1] * hovering_enlargement))
    play_button_hovered_cors = (W / 2 - play_button_hovered.get_width() / 2, play_button_fixed_cors[1] + play_button.get_height() / 2 - play_button_hovered.get_height() / 2)

    while running:
        # General
        clock.tick(FPS)
        frame += 1
        mouse_xcor, mouse_ycor = pygame.mouse.get_pos()
        

        # Blitting to Screen
        win.blit(bg, (0,0))

        title_ycor = sin(frame * title_jiggle_speed) * title_sine_amplitude
        win.blit(bg_title, (0, title_ycor))


        # Decision on which play button to blit
        hover_offset = (play_button_fixed_cors[0] - mouse_xcor, play_button_fixed_cors[1] - mouse_ycor)
        hovering_play_button = mouse_mask.overlap(play_button_mask, (hover_offset))

        if hovering_play_button:
            win.blit(play_button_hovered, play_button_hovered_cors)

            if pygame.mouse.get_pressed()[0]:
                # Continue Onwards with the Programme
                return running  
        else:
            win.blit(play_button, play_button_fixed_cors)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # End the Programme Safely
                running = False
                return False
            

def choose_chips():
    pass
            

def play(clock:pygame.time.Clock, make_image:callable, mouse_mask:pygame.mask.Mask):
    # General
    running = True
    frame = 0

    # Bets & Money 
    INSURANCE = 2
    BLACKJACK = 3/2

    ### (change these to change betting range, $1 - $100 by default)
    MIN_BET = 1
    MAX_BET = 100

    # Chips
    chip_colours = ["black", "blue", "green", "purple", "red"]
    chip_dimensions = ( W / 15, W / 15)
    chips = {col:make_image(f"chips\\{col} chip.png", chip_dimensions) for col in chip_colours}
    center_chip_cors = (W / 2, H / 7 * 6)

    # Images
        # BG
    bg = make_image("bg play.png", (W,H))

    while running:
        # General
        clock.tick(FPS)
        frame += 1
        mouse_xcor, mouse_ycor = pygame.mouse.get_pos()

        # Blitting to Screen
        win.blit(bg, (0,0))

        for i, chip in enumerate(chips.values()):
            win.blit(chip, (center_chip_cors[0] - chip.get_width() / 2, center_chip_cors[1] - chip.get_height() / 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # End the Programme Safely
                running = False
                return False


# Main Operations
def main(make_image:callable, mouse_mask:pygame.mask.Mask):
    clock = pygame.time.Clock()
    running = load(clock, make_image, mouse_mask)

    # Player (Change this value to change starting sum, $100 by default)
    starting_sum = 100

    while running:
        clock.tick(FPS)

        
        running = play(clock, make_image, mouse_mask)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main(make_image, mouse_mask)