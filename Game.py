import ball
import my_event
import turtle
import random
import heapq
import paddleV2

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        self.ball = ball.Ball(ball_radius, 0, 0, 10 * random.uniform(-1.0, 1.0), 10 * random.uniform(-1.0, 1.0), (255, 0, 255), 0)
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

    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"Player 1: {self.score1}  Player 2: {self.score2}", align="center",
                                 font=("Arial", 24, "normal"))

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        # dt = a_ball.time_to_hit(self.ball)
        # heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball, None)) #No particle-particle

        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball, None))

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
        # for i in range(len(self.ball_list)):
        #     self.ball_list[i].draw()
        self.ball.draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ, None, None, None))

    def __paddle_predict(self):
        for i in range(len(self.ball_list)):
            a_ball = self.ball_list[i]
            dtP1 = a_ball.time_to_hit_paddle(self.my_paddle)
            dtP2 = a_ball.time_to_hit_paddle(self.my_paddle2)
            heapq.heappush(self.pq, my_event.Event(self.t + dtP1, a_ball, None, self.my_paddle))
            heapq.heappush(self.pq, my_event.Event(self.t + dtP2, a_ball, None, self.my_paddle2))

    def run(self):
        # initialize pq with collision events and redraw event
        self.__predict(self.ball)
        heapq.heappush(self.pq, my_event.Event(0, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        self.screen.listen()
        self.screen.onkey(self.my_paddle.move_up, "Up")
        self.screen.onkey(self.my_paddle.move_down, "Down")
        self.screen.onkey(self.my_paddle.move_right, "Right")
        self.screen.onkey(self.my_paddle.move_left, "Left")
        self.screen.onkey(self.my_paddle2.move_up, "w")
        self.screen.onkey(self.my_paddle2.move_down,"s")
        self.screen.onkey(self.my_paddle2.move_left, "a")
        self.screen.onkey(self.my_paddle2.move_right, "d")
        print(self.pq)

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle

            # update positions, and then simulation clock
            self.ball.move(e.time - self.t)
            self.t = e.time

            # if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
            #     ball_a.bounce_off(ball_b)
            #
            # elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
            #     ball_a.bounce_off_vertical_wall()
            #
            # elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
            #     ball_b.bounce_off_horizontal_wall()

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

            self.__predict(ball_a)
            self.__predict(ball_b)

            # regularly update the prediction for the paddle as its position may always be changing due to keyboard events
            self.__paddle_predict()
            # heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ, None, None, None))

        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()


# num_balls = int(input("Number of balls to simulate: "))
num_balls = 1
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()

