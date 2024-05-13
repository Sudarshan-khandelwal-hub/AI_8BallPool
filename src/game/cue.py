import math
import numpy as np
import pygame

from . import config
from . import event
from . import gamestate
from . import physics

# Class for the cue sprite used in a pool game
class Cue(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)  # Initialize sprite
        self.angle = 0  # Initial angle of the cue
        self.color = config.player1_cue_color  # Default cue color from config
        self.target_ball = target  # The ball targeted by the cue
        self.visible = False  # Visibility state of the cue
        self.displacement = config.ball_radius  # Displacement of the cue from its target ball
        self.sprite_size = np.repeat(
            [config.cue_length + config.cue_max_displacement], 2)  # Size of the cue sprite
        self.clear_canvas()  # Setup the initial graphical state of the cue

    def clear_canvas(self):
        # Clears the canvas to reset the cue's image
        self.image = pygame.Surface(2 * self.sprite_size)  # Create a surface for the cue sprite
        self.image.fill((200, 200, 200))  # Fill the background color
        self.image.set_colorkey((200, 200, 200))  # Set transparency key color
        self.rect = self.image.get_rect()  # Get the image rectangle
        self.rect.center = self.target_ball.ball.pos.tolist()  # Position it at the target ball's position

    def update(self, *args):
        # Update the cue's graphical representation based on its state
        if self.visible:
            self.image = pygame.Surface(2 * self.sprite_size)
            self.image.fill((200, 200, 200))
            self.image.set_colorkey((200, 200, 200))

            sin_cos = np.array([math.sin(self.angle), math.cos(self.angle)])  # Calculate sin and cos for rotation
            initial_coords = np.array([math.sin(self.angle + 0.5 * math.pi), math.cos(self.angle + 0.5 * math.pi)]) * config.cue_thickness
            coord_diff = sin_cos * config.cue_length  # Calculate the length component for the cue
            rectangle_points = np.array((initial_coords, -initial_coords,
                                         -initial_coords + coord_diff, initial_coords + coord_diff))  # Define rectangle corners
            rectangle_points_from_circle = rectangle_points + self.displacement * sin_cos  # Adjust points for displacement
            self.points_on_screen = rectangle_points_from_circle + self.target_ball.ball.pos
            self.rect = self.image.get_rect()
            self.rect.center = self.target_ball.ball.pos.tolist()
        else:
            self.clear_canvas()  # Clear the canvas if the cue is not visible

    def is_point_in_cue(self, point):
        # Check if a given point is within the cue's rectangle
        rect_sides = [config.cue_thickness * 2, config.cue_length] * 2  # Dimensions of the cue rectangle
        triangle_sides = np.apply_along_axis(
            physics.point_distance, 1, self.points_on_screen, point)  # Calculate distances from point to each corner
        calc_area = np.vectorize(physics.triangle_area)
        triangle_areas = np.sum(
            calc_area(triangle_sides, np.roll(triangle_sides, -1), rect_sides))  # Calculate areas of triangles formed with the point
        rect_area = rect_sides[0] * rect_sides[1]  # Rectangle area
        return rect_area + 1 >= triangle_areas  # Compare the sum of triangle areas to the rectangle area

    def update_cue_displacement(self, displacement):
        # Set the cue displacement while respecting maximum and minimum bounds
        if displacement > config.cue_max_displacement:
            self.displacement = config.cue_max_displacement
        elif displacement < config.ball_radius:
            self.displacement = config.ball_radius
        else:
            self.displacement = displacement

    def draw_lines(self, game_state, target_ball, angle, color):
        # Draw aiming lines from the cue
        cur_pos = np.copy(target_ball.ball.pos)
        diff = np.array([math.sin(angle), math.cos(angle)])  # Direction vector for the line
        while config.resolution[1] > cur_pos[1] > 0 and config.resolution[0] > cur_pos[0] > 0:
            cur_pos += config.aiming_line_length * diff * 2  # Extend the line

    def is_clicked(self, events):
        # Check if the cue has been clicked based on the mouse position
        return events["clicked"] and self.is_point_in_cue(events["mouse_pos"])

    def make_visible(self, current_player):
        # Set the cue visible and adjust its color based on the current player
        if current_player == gamestate.Player.Player1:
            self.color = config.player1_cue_color
        else:
            self.color = config.player2_cue_color
        self.visible = True
        self.update()

    def make_invisible(self):
        # Set the cue invisible
        self.visible = False

    def cue_is_active(self, game_state, events):
        # Handle cue movement and interaction during gameplay
        initial_mouse_pos = events["mouse_pos"]
        initial_mouse_dist = physics.point_distance(
            initial_mouse_pos, self.target_ball.ball.pos)

        while events["clicked"]:
            events = event.events()
            self.update_cue(game_state, initial_mouse_dist, events)

        if self.displacement > config.ball_radius + config.cue_safe_displacement:
            self.ball_hit()

    def ball_hit(self):
        # Calculate the impact of the cue on the ball and apply the resulting force
        new_velocity = -(self.displacement - config.ball_radius - config.cue_safe_displacement) * \
                       config.cue_hit_power * np.array([math.sin(self.angle), math.cos(self.angle)])
        change_in_disp = np.hypot(*new_velocity) * 0.1
        while self.displacement - change_in_disp > config.ball_radius:
            self.displacement -= change_in_disp
            self.update()
            pygame.display.flip()
        self.target_ball.ball.apply_force(new_velocity)
        self.displacement = config.ball_radius
        self.visible = False

    def update_cue(self, game_state, initial_mouse_dist, events, angle):
        # Update cue position based on mouse events and position
        current_mouse_pos = events["mouse_pos"]
        displacement_from_ball_to_mouse = self.target_ball.ball.pos - current_mouse_pos
        prev_angle = self.angle
        if not displacement_from_ball_to_mouse[0] == 0:
            self.angle = angle  # Update the angle based on calculations
        game_state.redraw_all(update=False)
        pygame.display.flip()