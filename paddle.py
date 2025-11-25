# paddle.py
from turtle import Turtle

class Paddle(Turtle):
    """
    Palette with continuous movement (hold key = keep moving).
    """
    def __init__(self, position):
        '''
        Sets up the paddle with its visual appearance, initial position, and 
        movement configuration, allowing it to move vertically during gameplay.

        '''
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

        # continuous speed
        self.y_move = 0
        self.speed_value = 18  # adjustable (bigger = faster)

    def move(self):
        """Move the paddle each frame according to its current speed."""
        new_y = self.ycor() + self.y_move
        # screen limits
        if new_y < 260 and new_y > -260:
            self.goto(self.xcor(), new_y)

    def up(self):
        """Starts moving upwards."""
        self.y_move = self.speed_value

    def down(self):
        """Starts moving down."""
        self.y_move = -self.speed_value

    def stop(self):
        """Stops the movement."""
        self.y_move = 0
