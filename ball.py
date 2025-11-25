# ball.py
from turtle import Turtle

class Ball(Turtle):
    """
    Game ball with movement and bounces.
    """
    def __init__(self):
        
        ''' Initializes the ball: sets its shape, color, starting position,
        and initial movement speed/direction.'''
        
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 4
        self.y_move = 4
        self.move_speed = 0.025  # Inicial speed

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9  # each bounce speeds up a little

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.05
        self.bounce_x()
