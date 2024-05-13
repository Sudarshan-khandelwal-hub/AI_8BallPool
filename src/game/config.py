import math

import numpy as np
import pygame

# Function to retrieve the default font from Pygame at a specified size
def get_default_font(size):
    font_default = pygame.font.get_default_font()
    return pygame.font.Font(font_default, size)

# Function to set the maximum display resolution based on the current display settings
def set_max_resolution():
    infoObject = pygame.display.Info()  # Gets current display info from Pygame
    global resolution
    global white_ball_initial_pos
    resolution = np.array([infoObject.current_w, infoObject.current_h])  # Sets the resolution to the current display width and height
    white_ball_initial_pos = (resolution + [table_margin + hole_radius, 0]) * [0.25, 0.5]  # Sets initial position of the white ball

# Window settings
fullscreen = False  # Indicates whether the game will run in fullscreen mode
if not fullscreen:
    resolution = np.array([1000, 500])  # Default resolution if not fullscreen
window_caption = "Pool"  # Window title
fps_limit = 2000  # Maximum frames per second

# Table settings
table_margin = 40  # Margin around the pool table
table_side_color = (200, 200, 0)  # Color of the table sides
table_color = (0, 100, 0)  # Color of the table surface
separation_line_color = (200, 200, 200)  # Color of the separation line
hole_radius = 22  # Radius of the table holes
# Positions of middle and side holes relative to their central positions
middle_hole_offset = np.array([
    [-hole_radius * 2, hole_radius], [-hole_radius, 0],
    [hole_radius, 0], [hole_radius * 2, hole_radius]
])
side_hole_offset = np.array([
    [-2 * math.cos(math.radians(45)) * hole_radius - hole_radius, hole_radius],
    [-math.cos(math.radians(45)) * hole_radius, -math.cos(math.radians(45)) * hole_radius],
    [math.cos(math.radians(45)) * hole_radius, math.cos(math.radians(45)) * hole_radius],
    [-hole_radius, 2 * math.cos(math.radians(45)) * hole_radius + hole_radius]
])

# Cue settings
player1_cue_color = (200, 100, 0)  # Cue color for player 1
player2_cue_color = (0, 100, 200)  # Cue color for player 2
cue_hit_power = 3  # Power of cue hit
cue_length = 250  # Length of the cue stick
cue_thickness = 4  # Thickness of the cue stick
cue_max_displacement = 100  # Maximum pull back displacement of the cue
cue_safe_displacement = 1  # Safe pull back displacement before hitting the ball
aiming_line_length = 14  # Length of the aiming line

# Ball settings
total_ball_num = 2  # Total number of balls
ball_radius = 14  # Radius of each ball
ball_mass = 20  # Mass of each ball
speed_angle_threshold = 0.09  # Threshold for speed angle
visible_angle_threshold = 0.05  # Threshold for visibility angle
ball_colors = [  # Colors of the balls
    (255, 255, 255), (0, 200, 200), (0, 0, 200), (150, 0, 0),
    (200, 0, 200), (200, 0, 0), (50, 0, 0), (100, 0, 0),
    (0, 0, 0), (0, 200, 200), (0, 0, 200), (150, 0, 0),
    (200, 0, 200), (200, 0, 0), (50, 0, 0), (100, 0, 0)
]
ball_stripe_thickness = 5  # Thickness of stripes on striped balls
ball_stripe_point_num = 25  # Number of points used to define a stripe on the balls

# Physics settings
friction_threshold = 0.4  # Velocity threshold below which balls stop moving
friction_coeff = 0.99  # Coefficient of friction affecting ball movement
ball_coeff_of_restitution = 0.9  # Coefficient of restitution for ball collisions
table_coeff_of_restitution = 0.9  # Coefficient of restitution for table collisions

# Menu settings
menu_text_color = (255, 255, 255)  # Text color in menu
menu_text_selected_color = (0, 0, 255)  # Color of selected menu text
menu_title_text = "Pool"  # Menu title text
menu_buttons = ["Play Pool", "Exit"]  # Buttons in the menu
menu_margin = 20  # Margin around menu elements
menu_spacing = 10  # Spacing between menu items
menu_title_font_size = 40  # Font size for the menu title
menu_option_font_size = 20  # Font size for menu options
exit_button = 2  # Index for the 'Exit' button
play_game_button = 1  # Index for the 'Play Game' button

# In-game ball target variables
player1_target_text = 'P1 balls - '  # Label for player 1's target balls
player2_target_text = 'P2 balls - '  # Label for player 2's target balls
target_ball_spacing = 3  # Spacing between displayed target balls
player1_turn_label = "Player 1 turn"  # Label indicating it's player 1's turn
player2_turn_label = "Player 2 turn"  # Label indicating it's player 2's turn
penalty_indication_text = " (click on the ball to move it)"  # Text indicating a penalty
game_over_label_font_size = 40  # Font size for the game over label
