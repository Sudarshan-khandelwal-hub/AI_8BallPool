import itertools
import random

import zope.event  # Module to handle event notifications

from . import config   # Configuration module with game settings
from . import event    # Event handling module
from . import physics  # Physics calculations module

# Function to resolve all collisions in a pool game scenario
def resolve_all_collisions(balls, holes, table_sides):
    # Check and handle the event where any ball falls into any hole
    for ball_hole_combination in itertools.product(balls, holes):
        if physics.distance_less_equal(ball_hole_combination[0].ball.pos, ball_hole_combination[1].pos, config.hole_radius):
            # Notify the system that a ball has been potted
            zope.event.notify(event.GameEvent("POTTED", ball_hole_combination[0]))

    # Check and handle collisions between balls and the table sides
    for line_ball_combination in itertools.product(table_sides, balls):
        if physics.line_ball_collision_check(line_ball_combination[0], line_ball_combination[1].ball):
            # Apply physics calculation for collision between a line (table side) and a ball
            physics.collide_line_ball(line_ball_combination[0], line_ball_combination[1].ball)

    # Retrieve a list of ball sprites for processing
    ball_list = balls.sprites()
    # Shuffle the list of balls to randomize the collisions (commonly done on the first break in pool)
    random.shuffle(ball_list)

    # Check and handle collisions between any two balls
    for ball_combination in itertools.combinations(ball_list, 2):
        if physics.ball_collision_check(ball_combination[0].ball, ball_combination[1].ball):
            # Apply physics calculation for ball-ball collision
            physics.collide_balls(ball_combination[0].ball, ball_combination[1].ball)
            # Notify the system of a collision event
            zope.event.notify(event.GameEvent("COLLISION", ball_combination))

# Function to check if a ball placed at a given position touches other balls
def check_if_ball_touches_balls(target_ball_pos, target_ball_number, balls):
    touches_other_balls = False
    # Iterate over all balls to check for collisions
    for ball in balls:
        if target_ball_number != ball.number and \
                physics.distance_less_equal(ball.ball.pos, target_ball_pos, config.ball_radius * 2):
            # If collision is detected, set flag to True
            touches_other_balls = True
            break
    # Return True if the ball touches other balls, otherwise False
    return touches_other_balls
