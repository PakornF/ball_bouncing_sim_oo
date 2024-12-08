import turtle


class Paddle:
    def __init__(self, width, height, color, my_turtle):
        self.width = width
        self.height = height
        self.location = [0, 0]
        self.color = color
        self.my_turtle = my_turtle
        self.my_turtle.penup()
        self.my_turtle.setheading(0)
        self.my_turtle.hideturtle()

    def set_location(self, location):
        self.location = location
        self.my_turtle.goto(self.location[0], self.location[1])

    def draw(self):
        self.my_turtle.color(self.color)
        self.my_turtle.goto(self.location[0], self.location[1] - self.height/2) #(0, -200)
        self.my_turtle.forward(self.width/2) #25
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(2):
            self.my_turtle.left(90)
            self.my_turtle.forward(self.height)
            self.my_turtle.left(90)
            self.my_turtle.forward(self.width)
        self.my_turtle.end_fill()
        self.my_turtle.penup()
        self.my_turtle.color("Blue")
        self.my_turtle.goto(self.location[0], self.location[1]-self.height*3/10)
        self.my_turtle.forward(self.width*3/10)
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(2):
            self.my_turtle.left(90)
            self.my_turtle.forward(self.height*3/5)
            self.my_turtle.left(90)
            self.my_turtle.forward(self.width*3/5)
        self.my_turtle.end_fill()
        self.my_turtle.penup()

    def clear(self):
        self.my_turtle.clear()

    def move_left(self):
        if (self.location[0] - self.width / 2 - 40) >= -turtle.screensize()[0]:
            self.set_location([self.location[0] - 40, self.location[1]])
            print("Left")

    def move_right(self):
        if (self.location[0] + self.width / 2 + 40) <= turtle.screensize()[0]:
            self.set_location([self.location[0] + 40, self.location[1]])
            print("Right")

    def __str__(self):
        return "paddle"