Multiplayer Air Hockey game made by turtle library, a game which can be played by two people on same device. Each player need to control the paddle to deflect a ball, making sure the ball cannot travel into their goal.

To setup and play this game, you need to fork or clone this repository into your device first, then you are good to go, open file name "Game.py" on your desired IDE, then hit run botton.
It should pop up a display screen for you to play.

I have modified:
1. ball.py ->
   1.1 time_to_hit_vertical_wall(): I modified the threshold of the position of vertical ball, as my project's game border is not as big as the original threshold.
2. paddleV2.py ->
   2.1 draw(): I modified how the paddle will be drawn, to make it more beautiful with embedded paddle inside of it.
   2.2 move_left(), move_right(), move_up_player1(), move_down_player1(), move_up_player2(), move_down_player2(): I modified the movement of the paddle, enabling it to move in 2D direction.
3. timer.py ->
   3.1 class Clock: I added clock class to track the duration of the game that is playing.
4. Game.py ->
   4.1 """TODO"""

#Usage to be added

#UML and its purpose
