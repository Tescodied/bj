import pygame, os
pygame.init()

from math import sin

# Dimensions - YOU MAY CHANGE THE WIDTH BUT NOT HEIGHT OR WH_RATIO
WH_RATIO = 5/7
W = 1500         
H = int(W * WH_RATIO)

# Display
FPS = 60
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Interactive blackjack")

# Colours 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (90, 255, 90)
LIGHT_GREEN = (135, 255, 135)

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
                return running
            

def choose_chips(clock:callable, player_cash:int, file_name:str, mouse_mask:pygame.mask.Mask):
    # General
    running = True
    frame = 0
    title_jiggle_speed = 0.1875
    title_sine_amplitude = 5

    # Images
        # BG
    bg = make_image("bg plain.png", (W,H))

    # Positioning
    CHIPS_TEXT_FIXED_GAP = H / 3

    # Animation
    def deny_animation(xcor, frame):
        duration_direction = FPS / 20
        length = 2
        add_frames = True
        
        if frame < duration_direction:
            xcor += length
        elif frame < duration_direction * 2:
            xcor -= length
        elif frame < duration_direction * 3:
            xcor -= length
        elif frame < duration_direction * 4:
            xcor += length
        else:
            add_frames = False

        return xcor, add_frames
    
    insert_animation = False
    animate_chip = None
    denial_frame = 0

    # Fonts
    text_size = W // 10
    font_path = os.path.abspath(__file__)[:-len(file_name)] + "font\\"
    text_font = pygame.font.Font(f"{font_path}bjfont.ttf", text_size)
    smaller_text_font = text_font = pygame.font.Font(f"{font_path}bjfont.ttf", text_size // 2)

    # Done Button
    done_text = text_font.render("Done", True, WHITE)
    done_dimensions = (done_text.get_width(), done_text.get_height())
    done_cors = (W / 20 * 19 - done_dimensions[0], H / 20)
    overlay_bg_rect_length = 10
    done_bg_rect = pygame.rect.Rect(done_cors[0] - overlay_bg_rect_length, done_cors[1] - overlay_bg_rect_length, done_dimensions[0] + overlay_bg_rect_length * 2, done_dimensions[1] + overlay_bg_rect_length * 2)
    done_border_radius = 10

    # General Chips
    chip_colours = ["red", "green", "blue", "black",  "purple"]
    chip_vals = [5, 25, 50, 100, 500] #PREFERABLY DO NOT CHANGE UNLESS YOU HAVE EXTREME STARTING CASH
    chip_values = { col : val for col, val in zip(chip_colours, chip_vals)}
    len_chip_types = len(chip_colours)
    chip_dimensions = ( W / len_chip_types * 0.65, W / len_chip_types * 0.65)
    chips = {col : make_image(f"chips\\{col} chip.png", chip_dimensions) for col in chip_colours}
    chip_surface_values = {surface : value for surface, value in zip(chips.values(), chip_vals)}
    chip_masks = {chip : pygame.mask.from_surface(chip) for chip in chips.values()}
    CHIPS_FIXED_GAP = W / 25

    center_chip_cors = (W / 2, H / 2 + CHIPS_TEXT_FIXED_GAP / 2 - chip_dimensions[1] / 2)

    # Correct Rounding
    def correct_round(num):
        return int(num + 0.5)

    chips_cors = {chip : (
        center_chip_cors[0] + 
        ((chip_dimensions[0] / 2) * (len_chip_types % 2)) + 
        (CHIPS_FIXED_GAP / 2 * ((len_chip_types + 1) % 2)) - 
        (chip_dimensions[0] * ((correct_round(len_chip_types / 2) - position))) - 
        (CHIPS_FIXED_GAP * (len_chip_types // 2 - position)), 
        center_chip_cors[1] - chip_dimensions[1] / 2
        )
        for position, chip in enumerate(chips.values())}
    
    changing_chip_cors = {chip : [xcor, ycor] for chip, (xcor, ycor) in chips_cors.items()}

    OUTLINE_WIDTH = 2
    outline_circle_radius = chip_dimensions[0] / 2 + OUTLINE_WIDTH

    # Chip Values to be blitted on top of the chi
    values_text = [smaller_text_font.render(f"${value}", True, LIGHT_RED) for value in chip_vals]
    values_size = {col: (value.get_width(), value.get_height()) for col, value in zip(chip_values.keys(), values_text)}
    # Very inefficient but works in terms of values_size[x]
    values_cors = [(chip_cors[0] + chip_dimensions[0] / 2 - values_size[col][0] / 2, chip_cors[1] + chip_dimensions[1] / 2 - values_size[col][1] / 2) for chip_cors, col in zip(chips_cors.values(), chip_values.keys())]
    values_blitting = {surface : cors for surface, cors in zip(values_text, values_cors)}


    # Chosen Chips
    chips_stats = {col : 0 for col in chips.values()}
    chosen_center_chip_cors = (center_chip_cors[0], center_chip_cors[1] + H / 4)
    chips_chosen = []

    # Divider Line
    divider_xaxis_margin = 50
    divider_cors = (divider_xaxis_margin, center_chip_cors[1] + (chosen_center_chip_cors[1] - center_chip_cors[1]) / 2)
    divider_dimensions = (W - divider_xaxis_margin * 2, 1)
    divider = pygame.rect.Rect(divider_cors[0], divider_cors[1], divider_dimensions[0], divider_dimensions[1])
    divider_col = (20, 20, 20)

    while running:
        # General
        clock.tick(FPS)
        frame += 1
        mouse_xcor, mouse_ycor = pygame.mouse.get_pos()
        left_clicked = False

        # Pygame Events (QUIT AND LEFT_CLICKED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # End the Programme Safely
                running = False
                return running, {}, {}, text_font
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_clicked = True

        # Texts and Player Info/Instructions
        info_text = text_font.render("Spend your money, pick your chips", True, WHITE)
        cash_text = smaller_text_font.render(f"${player_cash}", True, WHITE)

        cash_text_dimensions = (cash_text.get_width(), cash_text.get_height())
        text_cors = (W / 2 - cash_text_dimensions[0] / 2, H / 2 - CHIPS_TEXT_FIXED_GAP / 2 - cash_text_dimensions[1] / 2)
        info_text_dimensions = (info_text.get_width(), info_text.get_height())
        info_text_cors = (W / 2  - info_text_dimensions[0] / 2, text_cors[1] - H / 10)

        # Blitting to Screen
        win.blit(bg, (0,0))
        win.blit(cash_text, text_cors)

        moving_info_ycor = sin(frame * title_jiggle_speed) * title_sine_amplitude + info_text_cors[1]
        win.blit(info_text, (info_text_cors[0], moving_info_ycor))

        outline_circle_cors = {chip : (cors[0] + chip_dimensions[0] / 2, cors[1] + chip_dimensions[1] / 2) for chip, cors in changing_chip_cors.items()}
        outline_circle_cols = {chip : WHITE if player_cash >= val else LIGHT_RED for chip, val in zip(outline_circle_cors.keys(), chip_vals)}

        for chip, cors in changing_chip_cors.items():
            # Blit the chips with their allocated cors
            win.blit(chip, cors)

            # Decision on which play button to blit
            hover_offset = (cors[0] - mouse_xcor, cors[1] - mouse_ycor)
            hovering = mouse_mask.overlap(chip_masks[chip], (hover_offset))
            if hovering:
                pygame.draw.circle(win, outline_circle_cols[chip], outline_circle_cors[chip], outline_circle_radius, OUTLINE_WIDTH)
                if left_clicked:
                    if outline_circle_cols[chip] == LIGHT_RED:
                        insert_animation = True
                        animate_chip = chip
                    elif outline_circle_cols[chip] == WHITE:
                        player_cash -= chip_surface_values[chip]
                        chips_stats[chip] += 1
                        if chip not in chips_chosen:
                            chips_chosen.append(chip)

        # Animation Logic
        if insert_animation:
            changing_chip_cors[animate_chip][0], add_frames = deny_animation(changing_chip_cors[animate_chip][0], denial_frame)
            if add_frames:
                denial_frame += 1
            else:
                insert_animation = False
                denial_frame = 0

        for chip_text, cors in values_blitting.items():
            # Blit the value of the chips centrally on top of the chip
            win.blit(chip_text, cors)


        # Chosen Chips underneath
        len_chosen_chips = len(chips_chosen)

        chosen_chips_cors = {chip : (
            chosen_center_chip_cors[0] + 
            ((chip_dimensions[0] / 2) * (len_chosen_chips % 2)) + 
            (CHIPS_FIXED_GAP / 2 * ((len_chosen_chips + 1) % 2)) - 
            (chip_dimensions[0] * ((correct_round(len_chosen_chips / 2) - position))) - 
            (CHIPS_FIXED_GAP * (len_chosen_chips // 2 - position)), 
            chosen_center_chip_cors[1] - chip_dimensions[1] / 2
            )
            for position, chip in enumerate(chips_chosen)}

        # Chosen Chip Count Overlay - build texts in the same order as chips_chosen
        chips_chosen_texts = [text_font.render(str(chips_stats[chip]), True, WHITE) for chip in chips_chosen]
        chips_chosen_texts_cors = []
        for chip, text in zip(chips_chosen, chips_chosen_texts):
            cors = chosen_chips_cors[chip]
            text_cors = (cors[0], cors[1])
            chips_chosen_texts_cors.append(text_cors)

        # Blit each Chosen Chip and the number (preserve chosen order)
        for chip, text, text_cors in zip(chips_chosen, chips_chosen_texts, chips_chosen_texts_cors):
            win.blit(chip, chosen_chips_cors[chip])
            win.blit(text, text_cors)

        
        # Blit divider
        pygame.draw.rect(win, divider_col, divider)

        # Done Button
        cursor_rect = pygame.rect.Rect(mouse_xcor, mouse_ycor, 1, 1)
        if cursor_rect.colliderect(done_bg_rect):
            pygame.draw.rect(win, LIGHT_GREEN, done_bg_rect, border_radius=done_border_radius)
            if left_clicked and True in list(chips_stats.values()): # Change in future
                return running, player_cash, chips_stats, text_font
        else:
            pygame.draw.rect(win, GREEN, done_bg_rect, border_radius=done_border_radius)
        win.blit(done_text, done_cors)


        pygame.display.flip()
            

def play(clock:pygame.time.Clock, make_image:callable, mouse_mask:pygame.mask.Mask, chips:dict, cash:int):
    # General
    running = True
    frame = 0

    # Font
    text_size = W // 50
    font_path = os.path.abspath(__file__)[:-len(file_name)] + "font\\"
    text_font = pygame.font.Font(f"{font_path}bjfont.ttf", text_size)

    # Gamerules
    BLACKJACK = 3/2
    INSURANCE = 2

    # Render Cards
    card_dimensions = (W / 14, H / 7)
    card_path = os.path.abspath(__file__)[:-len(file_name)] + "assets\\cards\\"
    card_files = [f for f in os.listdir(card_path)]
    cards = [make_image("cards\\" + file, card_dimensions) for file in card_files]

    # Chips
    chip_dimensions = (W / 15, W / 15)
    chip_surfaces = []

    counts = []
    for surface, count in chips.items():
        if count > 0:
            chip_surfaces.append(pygame.transform.scale(surface, chip_dimensions))
            counts.append(count)


    center_chip_cors = (W / 2, H / 7 * 6)
    
    len_chip_types = len(chip_surfaces)
    CHIPS_FIXED_GAP = 10

    # Correct Rounding
    def correct_round(num):
        return int(num + 0.5)

    chips_cors = {chip : (
        center_chip_cors[0] + 
        ((chip_dimensions[0] / 2) * (len_chip_types % 2)) + 
        (CHIPS_FIXED_GAP / 2 * ((len_chip_types + 1) % 2)) - 
        (chip_dimensions[0] * ((correct_round(len_chip_types / 2) - position))) - 
        (CHIPS_FIXED_GAP * (len_chip_types // 2 - position)), 
        center_chip_cors[1] - chip_dimensions[1] / 2
        )
        for position, chip in enumerate(chip_surfaces)}
    
    count_texts = {chip : text_font.render(str(count), True, WHITE) for chip, count in zip(chip_surfaces, counts)}
    count_texts_dimensions = {text : (text.get_width(), text.get_height()) for text in count_texts.values()}
    COUNT_GAP = H / 50
    count_cors = {text : (cors[0] + chip_dimensions[0] / 2 - text_dimensions[0] / 2, cors[1] + chip_dimensions[1] + COUNT_GAP) for cors, (text, text_dimensions) in zip(chips_cors.values(), count_texts_dimensions.items())}
        
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

        for chip, cors in chips_cors.items():
            # Blit the chips with their allocated cors
            win.blit(chip, cors)

        for text, cors in count_cors.items():
            win.blit(text, cors)

        for i, card in enumerate(cards):
            win.blit(card, (W / 2 - card_dimensions[0] / 2, H / 112 * 73))
            win.blit(cards[i], (W / 2 - card_dimensions[0] / 4, H / 112 * 73 - card_dimensions[1] / 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # End the Programme Safely
                running = False
                return False


# Main Operations
def main(make_image:callable, mouse_mask:pygame.mask.Mask, file_name:str):
    # General
    clock = pygame.time.Clock()
    running = load(clock, make_image, mouse_mask)
    starting_sum = 1000
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Change this value to change starting sum, $100 by default

    if running:
        running, player_cash, chips, font = choose_chips(clock, starting_sum, file_name, mouse_mask)

    while running:
        clock.tick(FPS)

        running = play(clock, make_image, mouse_mask, chips, player_cash)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

if __name__ == "__main__":
    main(make_image, mouse_mask, file_name)
