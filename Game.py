import ball
import my_event
import turtle
import random
import heapq
import paddleV2
import pandas as pd
import timer

class BouncingSimulator:
    def __init__(self, num_balls, player1_name, player2_name):
        self.num_balls = num_balls
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4 # was 4
        turtle.title("Air Hockey")
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        # self.ball = ball.Ball(ball_radius, 0, 0, random.uniform(10, 15), random.uniform(10,15), (255, 0, 255), 0)
        self.ball = ball.Ball(ball_radius, 0, 0, random.uniform(25, 30), random.uniform(25, 30), (255, 0, 255), 0)
        self.ball_list.append(self.ball)

        tom = turtle.Turtle()
        self.my_paddle = paddleV2.Paddle(150, 7.5, (255, 0, 0), tom)
        self.my_paddle.set_location([0, -100])
        self.my_paddle2 = paddleV2.Paddle(150, 7.5, (0, 255, 0), tom)
        self.my_paddle2.set_location([0, 100])

        self.screen = turtle.Screen()
        self.score1 = 0
        self.score2 = 0
        self.score_display = turtle.Turtle()
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, self.canvas_height // 2 + 75)
        self.update_score_display()

        self.clock = timer.Clock(self.screen)

        # self.stats_button = turtle.Turtle()
        # self.stats_button.penup()
        # self.stats_button.shape("square")
        # self.stats_button.color(204, 229, 255)
        # self.stats_button.goto(-0.755 * self.canvas_width, 0.095 * self.canvas_height)
        # self.stats_button.shapesize(stretch_wid=2, stretch_len=5)

        # self.stats_button.fillcolor("blue")
        # self.stats_button.goto(-0.755 * self.canvas_width, 0.095 * self.canvas_height)
        # self.stats_button.setheading(0)  # Make sure the button is horizontal
        # self.stats_button.begin_fill()
        # for _ in range(2):
        #     self.stats_button.forward(20)  # Length of the button
        #     self.stats_button.left(90)
        #     self.stats_button.forward(20)  # Height of the button
        #     self.stats_button.left(90)
        # self.stats_button.end_fill()
        #
        # # Write text on top of the button
        # self.stats_button.goto(-0.755 * self.canvas_width, 0.095 * self.canvas_height)
        # self.stats_button.color("white")
        # self.stats_button.pendown()
        # self.stats_button.write("Show Stats", align="center", font=("Arial", 12, "normal"))
        #
        self.screen.listen()
        self.screen.onkeypress(self.clear_and_show_stats,"Escape")
        # turtle.delay(6)

    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"{self.player1_name}: {self.score1}  {self.player2_name}: {self.score2}", align="center",
                                 font=("Arial", 24, "normal"))

    def clear_and_show_stats(self):
        self.screen.clear()

        file_path = "data/Air_Hockey.csv"
        try:
            df = pd.read_csv(file_path)
            turtle.penup()
            turtle.goto(0, 0.9 * self.canvas_height)
            turtle.write("Game Stats", align="center", font=("Arial", 18, "normal"))

            y_offset = self.canvas_height * 0.75
            for index, row in df.iterrows():
                winner = row["Winner"]
                duration = row["Duration"]
                turtle.goto(0, y_offset)
                turtle.write(f"Winner: {winner} - Duration: {duration}", align="center", font=("Arial", 12, "normal"))
                y_offset -= 30
        except FileNotFoundError:
            turtle.goto(0, 0)
            turtle.write("No stats available yet", align="center", font=("Arial", 18, "normal"))
            turtle.hideturtle()
        self.screen.onkeypress(self.clear_csv, "c")
        turtle.done()

    def clear_csv(self):
        """Clear the data in the specified CSV file by overwriting it with an empty DataFrame."""
        file_path = "data/Air_Hockey.csv"
        try:
            # Create an empty dataframe with the same columns
            df = pd.DataFrame(columns=["Winner", "Duration"])

            # Write the empty dataframe to the file, overwriting any existing data
            df.to_csv(file_path, index=False)
            print(f"Data in {file_path} has been cleared.")

            # Notify user that the data was cleared
            self.screen.clear()
            turtle.penup()
            turtle.goto(0, 0)
            turtle.write("Game Stats Cleared", align="center", font=("Arial", 18, "normal"))
            turtle.hideturtle()
        except Exception as e:
            print(f"An error occurred while clearing the CSV file: {e}")

    def check_goal(self):
        if -0.15 * self.canvas_width <= self.ball.x <= 0.15 * self.canvas_width:
            # Check if the ball is below the lower goal line (for player 1 scoring)
            if self.ball.y - self.ball.size <= -0.95*self.canvas_height:
                self.score1 += 1
                self.reset_ball()
            # Check if the ball is above the upper goal line (for player 2 scoring)
            elif self.ball.y + self.ball.size >= 0.95*self.canvas_height:
                self.score2 += 1
                self.reset_ball()


    def reset_ball(self):
        self.ball.x = 0
        self.ball.y = 0
        self.ball.vx = random.uniform(25, 30)  # or your desired velocity
        self.ball.vy = random.uniform(25, 30)  # or your desired velocity
        self.update_score_display()

    def __draw_border(self):
        turtle.penup()
        turtle.goto(-0.9 * self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(0.75 * self.canvas_width)
            turtle.penup()
            turtle.forward(0.3 * self.canvas_width)
            turtle.pendown()
            turtle.forward(0.75 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)
        turtle.penup()
        turtle.color((150, 0, 0))
        turtle.pensize(5)
        turtle.goto(-0.9 * self.canvas_width, -0.75 * self.canvas_height)
        turtle.pendown()
        turtle.forward(1.8 * self.canvas_width)
        turtle.penup()
        turtle.goto(-0.9 * self.canvas_width, 0.75 * self.canvas_height)
        turtle.pendown()
        turtle.forward(1.8 * self.canvas_width)
        turtle.penup()
        turtle.color((0, 255, 255))
        turtle.pensize(5)
        turtle.goto(-0.9 * self.canvas_width,0)
        turtle.pendown()
        turtle.forward(1.8 * self.canvas_width)

    def __redraw(self):

        turtle.clear()
        self.my_paddle.clear()
        self.my_paddle2.clear()

        self.__draw_border()
        self.my_paddle.draw()
        self.my_paddle2.draw()

        self.ball.draw()

        turtle.update()

        # self.__predict(self.ball)
        # self.__paddle_predict()
        # self.__paddle_predict2()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ, None, None, None))

    def store_winner(self, winner_name):
        # Specify the folder where you want to save the CSV (e.g., "data" folder)
        # folder = "data"
        #
        # # Ensure the folder exists
        # import os
        # if not os.path.exists(folder):
        #     os.makedirs(folder)

        # file_path = os.path.join(folder, 'Air_Hockey.csv')
        file_path = "data/Air_Hockey.csv"

        elapsed_time = self.clock.get_elapsed_time()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        duration_str = f"{minutes:02}:{seconds:02}"

        # Check if the file exists; if not, create it and write the header
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Winner", "Duration"])

        # Append the winner's name to the dataframe
        df = df._append({"Winner": winner_name, "Duration": duration_str}, ignore_index=True)
        df.to_csv(file_path, index=False)

    def random_ball(self):
        if self.ball.vx > 0:
            self.ball.vx += random.uniform(10,15)
        elif self.ball.vx < 0:
            self.ball.vx -= random.uniform(-10, -15)
        if self.ball.vy > 0:
            self.ball.vy += random.uniform(10,15)
        elif self.ball.vy < 0:
            self.ball.vy -= random.uniform(-10, -15)

        # self.ball.x = random.uniform(-0.75 * self.canvas_width, 0.75 * self.canvas_width)
        # self.ball.y = random.uniform(-0.9 * self.canvas_height, 0.9 * self.canvas_height)

    def move_right_track_1(self):
        self.my_paddle.move_right()
        self.__paddle_predict()
        self.__paddle_predict2()
    def move_left_track_1(self):
        self.my_paddle.move_left()
        self.__paddle_predict()
        self.__paddle_predict2()
    def move_up_track_1(self):
        self.my_paddle.move_up_player1()
        self.__paddle_predict()
        self.__paddle_predict2()
    def move_down_track_1(self):
        self.my_paddle.move_down_player1()
        self.__paddle_predict()
        self.__paddle_predict2()

    def __paddle_predict(self):
        dtP1 = self.ball.time_to_hit_paddle(self.my_paddle)
        # if dtP1 < 1.0:
        #     heapq.heappush(self.pq, my_event.Event(self.t + dtP1, self.ball, None, self.my_paddle))
        heapq.heappush(self.pq, my_event.Event(self.t + dtP1, self.ball, None, self.my_paddle))
    def __paddle_predict2(self):
        dtP2 = self.ball.time_to_hit_paddle(self.my_paddle2)
        # if dtP2 < 1.0:
        #     heapq.heappush(self.pq, my_event.Event(self.t + dtP2, self.ball, None, self.my_paddle2))
        heapq.heappush(self.pq, my_event.Event(self.t + dtP2, self.ball, None, self.my_paddle2))

    def __predict(self, a_ball):
        if a_ball is None:
            return

        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball_list[i], None))

        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        # if dtX < 1.0:
        #     heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None, None))
        # if dtY < 1.0:
        #     heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball, None))

    def run(self):
        # initialize pq with collision events and redraw event
        self.__predict(self.ball)
        # self.__paddle_predict()
        # self.__paddle_predict2()
        heapq.heappush(self.pq, my_event.Event(0, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        self.screen.listen()
        # self.screen.onkeypress(self.move_up_track_1, "Up")
        # self.screen.onkeypress(self.move_down_track_1, "Down")
        # self.screen.onkeypress(self.move_right_track_1, "Right")
        # self.screen.onkeypress(self.move_left_track_1, "Left")

        self.screen.onkeypress(self.my_paddle.move_up_player1, "Up")
        self.screen.onkeypress(self.my_paddle.move_down_player1, "Down")
        self.screen.onkeypress(self.my_paddle.move_right, "Right")
        self.screen.onkeypress(self.my_paddle.move_left, "Left")
        self.screen.onkeypress(self.my_paddle2.move_up_player2, "w")
        self.screen.onkeypress(self.my_paddle2.move_down_player2,"s")
        self.screen.onkeypress(self.my_paddle2.move_left, "a")
        self.screen.onkeypress(self.my_paddle2.move_right, "d")
        self.screen.onkeypress(self.random_ball, "space")

        print(self.pq)

        while (True):
            e = heapq.heappop(self.pq)
            # print(e)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle

            # update positions, and then simulation clock
            self.ball.move(e.time - self.t)
            self.t = e.time

            self.clock.display_time()

            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle()

            self.check_goal()

            self.conclude = turtle.Turtle()
            self.conclude.goto(0,0)
            if self.score1 == 5:
                self.conclude.write(f"{self.player1_name} Win", align="Center", font=("Ariel", 40, "normal"))
                self.store_winner(self.player1_name)
                self.clock.display_time()
                break

            elif self.score2 == 5:
                self.conclude.write(f"{self.player2_name} Win", align="Center", font=("Ariel", 40, "normal"))
                self.store_winner(self.player2_name)
                self.clock.display_time()
                break

            self.__predict(ball_a)
            self.__predict(ball_b)
            #  regularly update the prediction for the paddle as its position may always be changing due to keyboard events
            self.__paddle_predict()
            self.__paddle_predict2()

            # heapq.heappush(self.pq, my_event.Event(0, None, None, None))
            # heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ+10000, None, None, None))

        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()


# num_balls = int(input("Number of balls to simulate: "))
num_balls = 1
p1_name = input("Please input player1's name")
p2_name = input("Please input player2's name")
my_simulator = BouncingSimulator(num_balls, p1_name, p2_name)
my_simulator.run()