import turtle
import math


class Ball:
    def __init__(self, size, x, y, vx, vy, color, id):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * size ** 2
        self.count = 0
        self.id = id
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]

    def draw(self):
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y - self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy;  # dv dot dr
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
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return d

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def time_to_hit(self, that):
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

        # should't happen, but seems to be needed for some extreme inputs
        # (floating-point precision when dvdv is close to 0, I think)
        if t <= 0:
            return math.inf

        return t

    def time_to_hit_vertical_wall(self):
        if self.vx > 0:
            return (0.9*self.canvas_width - self.x - self.size) / self.vx
        elif self.vx < 0:
            return (0.9*self.canvas_width + self.x - self.size) / (-self.vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (self.canvas_height + self.y - self.size) / (-self.vy)
        else:
            return math.inf

    def time_to_hit_paddle(self, paddle):
        # ถ้าบอลไม่ได้เคลื่อนที่ในแนวดิ่ง ก็ไม่มีการชน
        if self.vy == 0:
            return math.inf

        paddle_top = paddle.location[1] + paddle.height / 2
        paddle_bottom = paddle.location[1] - paddle.height / 2

        # ถ้าบอลเคลื่อนที่ขึ้น (vy > 0) บอลต้องอยู่ต่ำกว่าพื้นที่ paddle (บน)
        # เพื่อที่จะวิ่งขึ้นไปหา paddle
        if self.vy > 0:
            # ถ้าจุดบนของบอล (y + size) อยู่เหนือ paddle_bottom อยู่แล้ว แปลว่าบอลอยู่เลย paddle ไปหรือไม่ได้จะชน
            if (self.y + self.size) >= paddle_bottom:
                return math.inf
            # คำนวณเวลาถึงแนวระดับล่างของ paddle
            # ระยะทาง = paddle_bottom - (y + size)
            dt = (paddle_bottom - (self.y + self.size)) / self.vy

        # ถ้าบอลเคลื่อนลง (vy < 0) บอลต้องอยู่สูงกว่าพื้นที่ paddle (ล่าง)
        # เพื่อวิ่งลงไปหา paddle
        else:
            # ถ้าจุดล่างของบอล (y - size) อยู่ต่ำกว่าพื้นที่ paddle_top แปลว่าบอลอยู่เลย paddle ไปแล้ว
            if (self.y - self.size) <= paddle_top:
                return math.inf
            # คำนวณเวลาถึงแนวระดับบนของ paddle
            # ระยะทาง = (y - size) - paddle_top
            # เนื่องจาก vy < 0 เราจะเอาค่าเป็นบวกโดยหารด้วย -vy
            dt = ((self.y - self.size) - paddle_top) / (-self.vy)

        # ถ้าเวลาที่คำนวณได้ไม่สมเหตุสมผล (น้อยกว่าหรือเท่ากับ 0) แสดงว่าการชนไม่เกิดในอนาคต
        if dt <= 0:
            return math.inf

        # ตรวจสอบตำแหน่งแนวนอน ณ เวลานั้น
        x_future = self.x + self.vx * dt
        paddle_left = paddle.location[0] - paddle.width / 2
        paddle_right = paddle.location[0] + paddle.width / 2

        # ถ้าตำแหน่งในอนาคตของบอล (รวมรัศมีบอล) อยู่ในแนว paddle ก็ชน
        if (x_future + self.size >= paddle_left) and (x_future - self.size <= paddle_right):
            return dt
        else:
            return math.inf

    def bounce_off_paddle(self):
        self.vy = -self.vy
        self.count += 1

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)