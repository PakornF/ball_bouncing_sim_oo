'''clock'''
import time
import turtle

class Clock:
    '''clock representing'''
    def __init__(self, screen, position=(0, 50)):
        self.start_time = time.time()
        self.screen = screen
        self.position = position
        self.display = turtle.Turtle()
        self.display.penup()
        self.display.hideturtle()
        self.display.goto(self.position)

    def get_elapsed_time(self):
        '''get elapsed time'''
        return time.time() - self.start_time

    def display_time(self):
        '''display time'''
        elapsed_time = self.get_elapsed_time()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.display.clear()
        self.display.write(f"Time: {minutes:02}:{seconds:02}",
                           align="center", font=("Arial", 18, "normal"))

    def reset(self):
        '''reset'''
        self.start_time = time.time()
