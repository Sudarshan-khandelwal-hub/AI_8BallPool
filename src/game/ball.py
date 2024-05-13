import itertools
import math
from enum import Enum

import numpy as np
import pygame

from . import collisions  # Module for collision handling
from . import config      # Configuration module with game settings
from . import event       # Event handling module
from . import physics     # Physics calculations module

# Ball class representing a generic ball object
class Ball():
    def __init__(self):
        # Initialize position and velocity vectors as zero arrays
        self.pos = np.zeros(2, dtype=float)
        self.velocity = np.zeros(2, dtype=float)

    def apply_force(self, force, time=1):
        # Apply force to the ball, updating its velocity
        self.velocity += (force / config.ball_mass) * time

    def set_velocity(self, new_velocity):
        # Set the ball's velocity
        self.velocity = np.array(new_velocity, dtype=float)

    def move_to(self, pos):
        # Move ball to a new position
        self.pos = np.array(pos, dtype=float)

    def update(self, *args):
        # Update the ball's position and handle friction
        self.velocity *= config.friction_coeff
        self.pos += self.velocity

        # Stop the ball if its velocity falls below the threshold
        if np.hypot(*self.velocity) < config.friction_threshold:
            self.velocity = np.zeros(2)

# Enum class to distinguish different types of pool balls
class BallType(Enum):
    Striped = "striped"
    Solid = "solid"

# Class for striped balls
class StripedBall():
    def __init__(self):
        # Initialize points on a ball for stripes
        point_num = config.ball_stripe_point_num
        self.stripe_circle = config.ball_radius * np.column_stack((np.cos(np.linspace(0, 2 * np.pi, point_num)),
                                                                   np.sin(np.linspace(0, 2 * np.pi, point_num)),
                                                                   np.zeros(point_num)))

    def update_stripe(self, transformation_matrix):
        # Transform the stripes on the ball using a matrix
        for i, stripe in enumerate(self.stripe_circle):
            self.stripe_circle[i] = np.matmul(stripe, transformation_matrix)

    def draw_stripe(self, sprite):
        # Draw the stripes on the ball sprite
        for num, point in enumerate(self.stripe_circle[:-1]):
            if point[2] >= -1:
                pygame.draw.line(sprite, (255, 255, 255), config.ball_radius + point[:2],
                                 config.ball_radius + self.stripe_circle[num + 1][:2], config.ball_stripe_thickness)

# Class for solid balls
class SolidBall():
    def __init__(self):
        pass

# Sprite class for displaying a ball in Pygame
class BallSprite(pygame.sprite.Sprite):
    def __init__(self, ball_number):
        # Initialize sprite with ball number and type
        self.number = ball_number
        self.color = config.ball_colors[ball_number]
        if ball_number <= 8:
            self.ball_type = BallType.Solid
            self.ball_type_custom = "solid"
            self.ball_stripe = SolidBall()
        else:
            self.ball_type = BallType.Striped
            self.ball_type_custom = "stripe"
            self.ball_stripe = StripedBall()
        self.ball = Ball()
        pygame.sprite.Sprite.__init__(self)
        # Label configuration for the ball
        self.label_offset = np.array([0, 0, config.ball_radius])
        self.label_size = config.ball_radius // 2
        font_obj = config.get_default_font(config.ball_label_text_size)
        self.text = font_obj.render(str(ball_number), False, (0, 0, 0))
        self.text_length = np.array(font_obj.size(str(ball_number)))
        self.update_sprite()
        self.update()
        self.top_left = self.ball.pos - config.ball_radius
        self.rect.center = self.ball.pos.tolist()

    def update(self, *args):
        # Update ball sprite and position if it's moving
        if (self.ball.velocity[0]**2 + self.ball.velocity[1]**2) != 0:
            self.update_sprite()
            self.ball.update()

    def update_sprite(self):
        # Create a new sprite surface and apply transformations for label and colorkey
        sprite_dimension = np.repeat([config.ball_radius * 2], 2)
        new_sprite = pygame.Surface(sprite_dimension)
        colorkey = (200, 200, 200)
        new_sprite.fill(self.color)
        new_sprite.set_colorkey(colorkey)

        label_dimension = np.repeat([self.label_size * 2], 2)
        label = pygame.Surface(label_dimension)
        label.fill(self.color)
        dist_from_centre = 1.1 - (self.label_offset[0] ** 2 +
                                  self.label_offset[1] ** 2) / (config.ball_radius ** 2)

        if self.label_offset[2] > 0:
            pygame.draw.circle(label, (255, 255, 255),
                               label_dimension // 2, self.label_size)

            if self.number != 0:
                label.blit(self.text, (config.ball_radius - self.text_length) / 2)

            if self.label_offset[0] != 0:
                angle = -math.degrees(
                    math.atan(self.label_offset[1] / self.label_offset[0]))
                label = pygame.transform.scale(
                    label, (int(config.ball_radius * dist_from_centre), config.ball_radius))
                label = pygame.transform.rotate(label, angle)

        new_sprite.blit(
            label, self.label_offset[:2] + (sprite_dimension - label.get_size()) / 2)
        if self.ball_type == BallType.Striped:
            self.ball_stripe.draw_stripe(new_sprite)

        # Apply circular mask to the sprite using colorkey
        grid_2d = np.mgrid[-config.ball_radius:config.ball_radius +
                                               1, -config.ball_radius:config.ball_radius + 1]
        is_outside = config.ball_radius < np.hypot(*grid_2d)

        for xy in itertools.product(range(config.ball_radius * 2 + 1), repeat=2):
            if is_outside[xy]:
                new_sprite.set_at(xy, colorkey)

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.ball.pos - config.ball_radius
        self.rect.center = self.ball.pos.tolist()

    def create_image(self, surface, coords):
        surface.blit(self.image, coords)

    def is_clicked(self, events):
        # Check if the ball sprite is clicked by comparing the mouse position and ball position
        return physics.distance_less_equal(events["mouse_pos"], self.ball.pos, config.ball_radius)

    def move_to(self, pos):
        # Move ball to specified position and update the sprite center
        self.ball.move_to(pos)
        self.rect.center = self.ball.pos.tolist()

    def is_active(self, game_state, behind_separation_line=False):
        game_state.cue.make_invisible()
        events = event.events()

        while events["clicked"]:
            events = event.events()
            # Ensure that the new ball position is valid and does not collide with other balls
            if np.all(np.less(config.table_margin + config.ball_radius + config.hole_radius, events["mouse_pos"])) and \
                    np.all(np.greater(config.resolution - config.table_margin - config.ball_radius - config.hole_radius,
                                      events["mouse_pos"])) and \
                    not collisions.check_if_ball_touches_balls(events["mouse_pos"], self.number, game_state.balls):
                if behind_separation_line:
                    if events["mouse_pos"][0] <= config.white_ball_initial_pos[0]:
                        self.move_to(events["mouse_pos"])
                else:
                    self.move_to(events["mouse_pos"])
            game_state.redraw_all()
        game_state.cue.make_visible(game_state.current_player)
