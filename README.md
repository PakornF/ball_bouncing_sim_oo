Multiplayer Air Hockey game made by turtle library, a game which can be played by two people on same device. Each player need to control the paddle to deflect a ball, making sure the ball cannot travel into their goal.

To setup and play this game, you need to fork or clone this repository into your device first, then you are good to go, open file name "Game.py" on your desired IDE, then hit run botton.
It should pop up a display screen for you to play. Player1 uses arrow key to control paddle, while Player2 uses wasd key to control paddle, escape for stat, then you can press c to clear stat.

I have modified:
1. ball.py ->
   1.1 time_to_hit_vertical_wall(): I modified the threshold of the position of vertical ball, as my project's game border is not as big as the original threshold
2. paddleV2.py ->
   2.1 draw(): I modified how the paddle will be drawn, to make it more beautiful with embedded paddle inside of it
   2.2 move_left(), move_right(), move_up_player1(), move_down_player1(), move_up_player2(), move_down_player2(): I modified the movement of the paddle, enabling it to move in 2D direction
3. timer.py ->
   3.1 class Clock: I added clock class to track the duration of the game that is playing
4. Game.py -> (run_ball.py)
   4.1 __init__(): Added some attributes and create an object neccessary for project
      4.1.1 score: for tracking player's score(score1, score2)
      4.1.2 clock: for tracking duration of the game(clock)
      4.1.3 player's name: for displaying player's name
   4.2 clear_and_show_stat(), clear_csv(): Clearing the screen, then display the game won by player with duration
   4.3 check_goal(), reset_ball(): Check for goal, if it is goal, reset ball's location to 0 and random ball's speed
   4.4 store_winner(): Store winner's name into CSV file name "Air_Hockey.csv"
   4.5 run(): Add if-else condition, ending the game when whoever's score is 5

I test this code, I have faced many bugs, first one that I have noticed that the performance of it decreased drastically, might be due to excessive heappushing, causing fps dropping overtime. Also, the ball calculate the next position it be when it hit something, for example, if the ball hits paddle, it will calculate whether it will collide with another paddle or not, if it collied, while the ball is travelling and you move away the paddle that need to be collided, the ball will still remember to original position of the paddle, not the current location, making its movement a bit off.

For UML class diagram, the picture of it can be seen in UML_Class_Diagram.png.
The purpose of each class are:
1. Ball: Object ball for simulating ball in real life, with position x y, size(radius), and velocity, calculating position by physics law.
2. Event: Checking that if the ball got disturb by any event, such as colliding with paddle, or colliding with another ball.
3. Paddle: Object for simulation paddle in real life, with position x y, width and height, acting as a deflector of ball.
4. Clock: Object for simulation clock or timer in real life, tracking duration of the game.
5. BouncingSimulator: Simulate ball bouncing event in real life, combined of object Ball and Paddle, checking which event occurs by Event, and track duration using Clock.
