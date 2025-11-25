# scoreboard.py
from turtle import Turtle

class Scoreboard(Turtle):
    """
    Game scoreboard: tracks and displays the score of both players and also shows the victory message.
    """
    def __init__(self, winning_score: int = 5):
        """
        Initializes the scoreboard by setting its visual properties, tracking both
        players' scores, defining the winning score limit, and displaying the initial score.

        """
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.winning_score = winning_score
        self.update_score()

    def update_score(self):
        """Redraw the marker at the top of the screen"""
        self.clear()
        # Left fielder score
        self.goto(-100, 200)
        self.write(self.left_score, align="center", font=("Courier", 40, "normal"))
        # Right fielder score
        self.goto(100, 200)
        self.write(self.right_score, align="center", font=("Courier", 40, "normal"))

    def left_point(self):
        """Add a point to the left player and update the score."""
        self.left_score += 1
        self.update_score()

    def right_point(self):
        """Add a point to the right player and update the score."""
        self.right_score += 1
        self.update_score()

    def has_winner(self) -> bool:
        """Returns True if either of the two reached the winning score."""
        return (
            self.left_score >= self.winning_score
            or self.right_score >= self.winning_score
        )

    def show_winner(self):
        """Display the victory message in the center of the screen."""
        self.goto(0, 0)
        if self.left_score > self.right_score:
            message = "Left Player Wins!"
        elif self.right_score > self.left_score:
            message = "Right Player Wins!"
        else:
            message = "Draw!"
        self.write(message, align="center", font=("Courier", 30, "bold"))
