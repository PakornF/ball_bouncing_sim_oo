"""Ball"""
import turtle
import math

class Ball:
    """representing ball"""
    def __init__(self, size, x, y, vx, vy, color, id_num):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * size ** 2
        self.count = 0
        self.id = id_num
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]

    def draw(self):
        """draw ball"""
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        # draw = turtle.Turtle()
        # draw.penup()
        # draw.color(self.color)
        # draw.fillcolor(self.color)
        # draw.goto(self.x, self.y - self.size)
        # draw.pendown()
        # draw.begin_fill()
        # draw.circle(self.size)
        # draw.end_fill()
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y - self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        """deflect vertical ball"""
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        """deflect horizontal ball"""
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        """bounce off wall"""
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy  # dv dot dr
        dist = self.size + that.size  # distance between particle centers at collison

        # magnitude of normal force
        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        # update collision counts
        self.count += 1
        that.count += 1

    def distance(self, that):
        """distance"""
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return d

    def move(self, dt):
        """move"""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def time_to_hit(self, that):
        """calculate time to hit"""
        if self is that:
            return math.inf
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx * dvx + dvy * dvy
        if dvdv == 0:
            return math.inf
        drdr = dx * dx + dy * dy
        sigma = self.size + that.size
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        # if drdr < sigma*sigma:
        # print("overlapping particles")
        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv

        # shouldn't happen, but seems to be needed for some extreme inputs
        # (floating-point precision when dvdv is close to 0, I think)
        if t <= 0:
            return math.inf

        return t

    def time_to_hit_vertical_wall(self):
        """calculate time to hit vertical wall"""
        if self.vx > 0:
            return (0.9*self.canvas_width - self.x - self.size) / self.vx
        if self.vx < 0:
            return (0.9*self.canvas_width + self.x - self.size) / (-self.vx)
        return math.inf

    def time_to_hit_horizontal_wall(self):
        """calculate time to hit horizontal wall"""
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        if self.vy < 0:
            return (self.canvas_height + self.y - self.size) / (-self.vy)
        return math.inf

    def time_to_hit_paddle(self, paddle):
        """calculate time to hit paddle"""
        if self.vy == 0:
            return math.inf

        paddle_top = paddle.location[1] + paddle.height / 2
        paddle_bottom = paddle.location[1] - paddle.height / 2

        if self.vy > 0:
            if (self.y + self.size) >= paddle_bottom:
                return math.inf
            dt = (paddle_bottom - (self.y + self.size)) / self.vy

        else:
            if (self.y - self.size) <= paddle_top:
                return math.inf
            dt = ((self.y - self.size) - paddle_top) / (-self.vy)

        if dt <= 0:
            return math.inf

        x_future = self.x + self.vx * dt
        paddle_left = paddle.location[0] - paddle.width / 2
        paddle_right = paddle.location[0] + paddle.width / 2

        if (x_future + self.size >= paddle_left) and (x_future - self.size <= paddle_right):
            return dt
        return math.inf

    def bounce_off_paddle(self):
        """bounce off paddle"""
        self.vy = -self.vy
        self.count += 1

    def __str__(self):
        """string method"""
        return (str(self.x) + ":" + str(self.y) + ":" + str(self.vx)
                + ":" + str(self.vy) + ":" + str(self.count)+ str(self.id))
