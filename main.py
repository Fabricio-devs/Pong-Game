# main.py
import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

# Dummy sound to avoid lag (keeps the hook if you want real sound later)
def play_beep(freq=440, duration=50):
    """
    Dummy sound function.
    If you want actual sound on Windows, implement winsound.Beep here.
    """
    # if SOUND_AVAILABLE:
       # winsound.Beep(freq, duration)
    pass


# Global states
game_started = False
paused = False


def main():
    
    '''
    Inicializes and runs the main game loop for the Pong game.
    Sets up the screen, loads all game objects (paddles, ball, scoreboard).
    Displays start instructions and handles user input for selecting
    game mode (1 vs 1 or player vs AI) before the game begins
    '''
    
    global game_started, paused
    
    #-----------------------------------
    # ---------- SCREEN SETUP ----------
    #-----------------------------------
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black")
    screen.title("Pong - 1v1 / 1vAI")
    screen.tracer(0)

    #-----------------------------------
    # ---------- GAME OBJECTS ----------
    #-----------------------------------
    
    left_paddle = Paddle(position=(-350, 0))   # Player
    right_paddle = Paddle(position=(350, 0))   # Player or AI
    ball = Ball()
    scoreboard = Scoreboard(winning_score=5)
    
    #---------------------------------
    # ---------- START MENU ----------
    #---------------------------------
    
    start_message = Turtle()
    start_message.color("white")
    start_message.penup()
    start_message.hideturtle()
    start_message.goto(0, 0)
    start_message.write(
        "PONG\n\n"
        "Press 1 -> 1 vs 1\n"
        "Press 2 -> 1 vs AI\n\n"
        "Left: W / S   |   Right: Up / Down\n"
        "P to pause",
        align="center",
        font=("Courier", 16, "normal"),
    )

    # Game mode: "PVP" (1v1) or "PVE" (1vAI)
    game_mode = None

    #----------------------------------------
    # ---------- CONTROL FUNCTIONS ----------
    #----------------------------------------

    def start_pvp():
        """Start Player vs Player mode."""
        nonlocal game_mode, start_message
        global game_started
        if not game_started:
            game_mode = "PVP"
            game_started = True
            start_message.clear()

    def start_pve():
        """Start Player vs AI mode."""
        nonlocal game_mode, start_message
        global game_started
        if not game_started:
            game_mode = "PVE"
            game_started = True
            start_message.clear()

    def toggle_pause():
        """Toggle pause state when pressing P."""
        global paused
        if game_started:
            paused = not paused

    #--------------------------------------
    # ---------- PLAYER CONTROLS ----------
    #--------------------------------------
    
    screen.listen()

    # Left paddle (Player 1)
    screen.onkeypress(left_paddle.up, "w")
    screen.onkeypress(left_paddle.down, "s")
    screen.onkeyrelease(left_paddle.stop, "w")
    screen.onkeyrelease(left_paddle.stop, "s")

    # Right paddle (Player 2 in PVP mode)
    screen.onkeypress(right_paddle.up, "Up")
    screen.onkeypress(right_paddle.down, "Down")
    screen.onkeyrelease(right_paddle.stop, "Up")
    screen.onkeyrelease(right_paddle.stop, "Down")

    # Mode selection
    screen.onkeypress(start_pvp, "1")
    screen.onkeypress(start_pve, "2")

    # Pause
    screen.onkeypress(toggle_pause, "p")
    
    #------------------------------------
    # ---------- AI PARAMETERS ----------
    #------------------------------------
    
    AI_TOLERANCE = 20            # Vertical dead zone (higher = easier)
    AI_ACTIVE_X = 0              # Only follow the ball when it is to the right of this X
    AI_FOLLOW_WHEN_TOWARDS = True  # Follow only if ball is moving toward AI

    game_is_on = True

    while game_is_on:
        
        '''Main game loop:'''
        # Continuously updates the game state while the game is active.
        # Handles paddle movement (player or AI), ball movement, collision
        # detection, scoring and screen refresh timing to keep the game running
        # smoodthly until the match ends.
        
        screen.update()
        time.sleep(0.01)  # Small delay for smooth animation

        # If no mode selected, not started, or paused → no updates
        if not game_started or paused or game_mode is None:
            continue

        # ---------- LEFT PADDLE MOVEMENT (always controlled by player) ----------
        left_paddle.move()

        # ---------- RIGHT PADDLE MOVEMENT ----------
        if game_mode == "PVP":
            # In multiplayer mode, right paddle is controlled by player 2
            right_paddle.move()

        elif game_mode == "PVE":
            # AI logic for right paddle
            ball_moving_right = ball.x_move > 0
            ball_on_right_side = ball.xcor() > AI_ACTIVE_X

            # AI reaction logic
            if (not AI_FOLLOW_WHEN_TOWARDS or ball_moving_right) and ball_on_right_side:
                # Move AI paddle up/down depending on ball's Y position
                if ball.ycor() > right_paddle.ycor() + AI_TOLERANCE:
                    right_paddle.y_move = right_paddle.speed_value
                elif ball.ycor() < right_paddle.ycor() - AI_TOLERANCE:
                    right_paddle.y_move = -right_paddle.speed_value
                else:
                    right_paddle.y_move = 0
            else:
                # AI stays still when ball is far or moving away
                right_paddle.y_move = 0

            right_paddle.move()
        
        #------------------------------------
        # ---------- BALL MOVEMENT ----------
        #------------------------------------
        
        '''Moves the ball forward based on its current direction and speed'''
        ball.move()
        #-----------------------------------
        # ---------- WALL BOUNCES ----------
        #-----------------------------------
        
        '''Reveses the vertical direction of the ball when it hits the loop or bottom walls.'''
        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.bounce_y()
            play_beep(600, 40)

        #---------------------------------------
        # ---------- PADDLE COLLISIONS ---------
        #---------------------------------------
        
        '''
        Checks if the ball collides with either paddle.
        If so, reverses the ball's horizontal direction and 
        increases its speed slightly
        '''
        
        if ball.distance(right_paddle) < 50 and ball.xcor() > 320:
            ball.bounce_x()
            play_beep(800, 40)

        if ball.distance(left_paddle) < 50 and ball.xcor() < -320:
            ball.bounce_x()
            play_beep(800, 40)

        #------------------------------
        # ---------- SCORING ----------
        #------------------------------
    
        # Ball goes out on the right
        '''
        If the ball passes beyond the right boundary, Player 1 scores.
        Resets ball and paddle position and updates the scoreboard
        '''
        if ball.xcor() > 380:
            scoreboard.left_point()
            ball.reset_position()
            play_beep(400, 80)

        # Ball goes out on the left
        '''
        If the ball passes beyond the left boundary, Player 2 scores.
        Resets ball and paddle position and updates the scoreboard
        '''
        if ball.xcor() < -380:
            scoreboard.right_point()
            ball.reset_position()
            play_beep(400, 80)
            
        #------------------------------------
        # ---------- WIN CONDITION ----------
        #------------------------------------
        '''
        If either player reaches the target score. the game ends.
        Displays the winner and stops the main game loop
        '''
        if scoreboard.has_winner():
            scoreboard.show_winner()
            game_is_on = False

    # Exit
    screen.exitonclick()

# Runs the game only when this script is executed directly
if __name__ == "__main__":
    main()
