'Snake coding challendge'

from tkinter import *
import random

canvas_height = 500
canvas_width = 500
field_size = 20
fragment_size = 20

root = Tk()
root.title('The Snake')
root.wm_attributes('-topmost', True)
canvas = Canvas(root, height=canvas_height, width=canvas_width, bg='#%02x%02x%02x' % (255, 255, 255))
canvas.pack(expand=True, fill=BOTH)
canvas.focus_set()

class Snake():

    def __init__(self, canvas, fragment_size, field_borders_coords):

        self.canvas = canvas
        self.field_borders_coords = field_borders_coords
        self.fragment_size = fragment_size
        #mods = ['easy', 'hard']
        #self.mod = mods[1]
        self.score = 0
        self.game_over = False
        self.speed_identified = False
        self.canvas.bind('<KeyPress>', self.identify_speed)
        self.speeds = {'xspeed':0, 'yspeed':0}
        self.fragments = [self.canvas.create_oval(self.field_borders_coords[0], self.field_borders_coords[1],
                                                  self.field_borders_coords[0] + self.fragment_size,
                                                  self.field_borders_coords[1] + self.fragment_size,
                                                  fill='#%02x%02x%02x' % (49, 129, 61))]

    def add_fragment(self):

        fragment = self.canvas.create_oval(self.canvas.coords(self.fragments[-1])[0],
                                           self.canvas.coords(self.fragments[-1])[1],
                                           self.canvas.coords(self.fragments[-1])[2],
                                           self.canvas.coords(self.fragments[-1])[3],
                                           fill='#%02x%02x%02x' % (49, 129, 61))
        self.fragments.append(fragment)

    def identify_speed(self, event):
        
        move_directions = {'Up':{'speed':'yspeed', 'direction':-1},
                           'Down':{'speed':'yspeed', 'direction':1},
                           'Left':{'speed':'xspeed', 'direction':-1},
                           'Right':{'speed':'xspeed', 'direction':1}}

        if event.keysym in move_directions and self.speeds[move_directions[event.keysym]['speed']] == 0 and not self.speed_identified:
            for speed in self.speeds:
                self.speeds[speed] = 0
            self.speeds[move_directions[event.keysym]['speed']] = move_directions[event.keysym]['direction']
            self.speed_identified = True

    def move(self):

        if len({self.speeds['xspeed'], self.speeds['yspeed']}) > 1:

            x, y = self.canvas.coords(self.fragments[0])[0] + self.speeds['xspeed'] * self.fragment_size, self.canvas.coords(self.fragments[0])[1] + self.speeds['yspeed'] * self.fragment_size
            if x < self.field_borders_coords[0] or x > self.field_borders_coords[2] - self.fragment_size or y < self.field_borders_coords[1] or y > self.field_borders_coords[3] - self.fragment_size:
                self.game_over = True
                    #x, y = self.canvas.coords(self.fragments[0])[0] + self.speeds['xspeed'] * (self.fragment_size + self.field_borders_coords[2] - self.field_borders_coords[0]), self.canvas.coords(self.fragments[0])[1] + self.speeds['yspeed'] * (self.fragment_size + self.field_borders_coords[3] - self.field_borders_coords[1])
            if [x, y] in [self.canvas.coords(fragment)[:2] for fragment in self.fragments]:
                self.game_over = True 

            if not self.game_over:
                fragment = self.canvas.create_oval(x, y, x + self.fragment_size, y + self.fragment_size, fill='#%02x%02x%02x' % (49, 129, 61))
                self.fragments.insert(0, fragment)
                self.canvas.delete(self.fragments[-1])
                self.fragments.pop(-1)

            self.speed_identified = False

    def eat_food(self, food_coords):

        if self.canvas.coords(self.fragments[0])[0] == food_coords[0] and self.canvas.coords(self.fragments[0])[1] == food_coords[1]:
            self.add_fragment()
            self.score += 1
            return True
        return False

class Food():

    def create_food(self, canvas, field_size, fragment_size, field_borders_coords, fragment_coords):

        self.canvas = canvas
        x, y = random.randint(0, field_size - 1) * fragment_size + field_borders_coords[0], random.randint(0, field_size - 1) * fragment_size + field_borders_coords[1]
        while [x, y] in fragment_coords:
            x, y = random.randint(0, field_size - 1) * fragment_size + field_borders_coords[0], random.randint(0, field_size - 1) * fragment_size + field_borders_coords[1]
        self.food = self.canvas.create_oval(x, y, x + fragment_size, y + fragment_size, fill='#%02x%02x%02x' % (255, 204, 0))

def update():
    snake.move()
    if snake.eat_food(food.canvas.coords(food.food)[:2]):
        food.canvas.delete(food.food)
        food.create_food(canvas, field_size, fragment_size, canvas.coords(field_borders)[:2], [snake.canvas.coords(fragment)[:2] for fragment in snake.fragments])
        canvas.itemconfig(score_text, text='Score:' + str(snake.score))
    canvas.after(150, update)
        

if __name__ == '__main__':

    field_borders = canvas.create_rectangle((canvas_width - field_size * fragment_size) / 2,
                                            (canvas_height - field_size * fragment_size) / 2,
                                            (canvas_width + field_size * fragment_size) / 2,
                                            (canvas_width + field_size * fragment_size) / 2,
                                            fill='#%02x%02x%02x' % (230, 230, 230))
    food = Food()
    snake = Snake(canvas, fragment_size, canvas.coords(field_borders))
    food.create_food(canvas, field_size, fragment_size, canvas.coords(field_borders)[:2], [snake.canvas.coords(fragment)[:2] for fragment in snake.fragments])
    score_text = canvas.create_text((canvas.coords(field_borders)[2] - canvas.coords(field_borders)[0]) / 2,
                                    canvas.coords(field_borders)[3] + 15, text='Score:' + str(snake.score), font='Verdana 20')
    update()
    root.update()
