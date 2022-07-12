'Tetris coding challendge'

from tkinter import *
import random
import copy

canvas_height = 645
canvas_width = 500

root = Tk()
root.title('tetris')
root.wm_attributes("-topmost", True)
canvas = Canvas(root, height=canvas_height, width=canvas_width, bg='#%02x%02x%02x' % (48, 100, 255))
canvas.pack(fill=BOTH, expand=True, anchor=CENTER)
canvas.focus_set()

class Field():

    """Python Shell Field Display"""

    def __init__(self, canvas, canvas_width, canvas_height):

        self.canvas = canvas
        self.canvas.bind('<KeyPress>', self.move_figure)
        self.canvas.bind('<Up>', self.rotate_figure)

        self.game_over = False

        self.score = 0
        #self.levels = {str(level): time for level, y in zip(range(1, 11), range())}

        self.field_x_size = 10
        self.field_y_size = 20
        self.figure_piece_size = 27

        self.field = [[0 for x in range(self.field_x_size)] for y in range(self.field_y_size)]
        self.figures = [{'figure_rotations':[[{'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1}],

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 - 1, 'y':0}], # T-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0}],

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 + 1, 'y':0}]],
            
                         'color':'#%02x%02x%02x' % (235, 10, 25)},
                        
                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                             {'x':self.field_x_size // 2 - 1, 'y':0},
                                             {'x':self.field_x_size // 2 + 1, 'y':0},
                                             {'x':self.field_x_size // 2 + 2, 'y':0}], #Straight-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2, 'y':2}]],
                         
                         'color':'#%02x%02x%02x' % (21, 255, 43)},

                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0}, #Block-Figure
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 + 1, 'y':1}]],

                         'color':'#%02x%02x%02x' % (243, 150, 150)},

                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 - 1, 'y':1}], #Stairs-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':1}]],
        
                         'color':'#%02x%02x%02x' % (21, 45, 255)},

                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 + 1, 'y':1}], #Reversed-Stairs-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':1}]],

                         'color':'#%02x%02x%02x' % (69, 15, 147)},

                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':1}], #Shoe-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 - 1, 'y':1}],

                                             [{'x':self.field_x_size // 2 - 1, 'y':-1},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0}],

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2 + 1, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1}]],

                         'color':'#%02x%02x%02x' % (192, 4, 222)},

                        {'figure_rotations':[[{'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':1}], #Reversed-Shoe-Figure

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2 - 1, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1}],

                                             [{'x':self.field_x_size // 2 + 1, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2 - 1, 'y':0},
                                              {'x':self.field_x_size // 2 + 1, 'y':0}],

                                             [{'x':self.field_x_size // 2, 'y':-1},
                                              {'x':self.field_x_size // 2, 'y':0},
                                              {'x':self.field_x_size // 2, 'y':1},
                                              {'x':self.field_x_size // 2 + 1, 'y':1}]],

                         'color':'#%02x%02x%02x' % (40, 40, 40)}]

        self.create_field('#%02x%02x%02x' % (255, 255, 255))
        
        self.score_text = self.canvas.create_text((self.canvas.coords(self.play_field)[0] + self.canvas.coords(self.play_field)[2]) / 2,
                                                  self.canvas.coords(self.play_field)[3] + 15,
                                                  text='Score:' + str(self.score), font='Verdana 19')
        self.canvas_stayable_figures = []
        self.spawn_figure()

        #print(self.field)

    def spawn_figure(self):

        self.figure = copy.deepcopy(random.choice(self.figures))
        self.figure['stayable'] = False
        self.figure_rotation_index = 0
        self.detect_coord_testability()

        for coord in self.figure['figure_rotations'][self.figure_rotation_index]:

            if self.field[coord['y']][coord['x']] == 1:

                self.game_over = True
                self.canvas_game_over()
                break

        if self.game_over == False:
        
            for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                self.field[coord['y']].pop(coord['x'])
                self.field[coord['y']].insert(coord['x'], 1)

            self.check_figure()
            
            self.canvas_display_figure()

    def figure_fall(self):

        if self.game_over == False:

            self.check_figure()

            if self.figure['stayable'] == False:

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    self.field[coord['y']].pop(coord['x'])
                    self.field[coord['y']].insert(coord['x'], 0)

                for rotation in self.figure['figure_rotations']:
                    for coord in rotation:
                        coord['y'] += 1

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    self.field[coord['y']].pop(coord['x'])
                    self.field[coord['y']].insert(coord['x'], 1)

                self.canvas_figure_fall()

    def check_figure(self):

        for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
            
            if coord['y'] >= self.field_y_size - 1 or self.field[coord['y'] + 1][coord['x']] == 1 and coord['down_move_check'] == True:

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    for move_check in ('down_move_check', 'right_move_check', 'left_move_check'):
                        del coord[move_check]

                self.figure['stayable'] == True
                self.canvas_stayable_figures.extend(self.canvas_figure)
                self.check_lines()
                self.spawn_figure()
                break

        #print(self.field)

    def move_figure(self, event):

        if self.game_over == False:

            if event.keysym == 'Down':
                self.check_figure()

            move_directions = {'Left':{'coord':'x', 'move_direction':-1, 'move_access':True},
                               'Right':{'coord':'x', 'move_direction':1, 'move_access':True},
                               'Down':{'coord':'y', 'move_direction':1, 'move_access':True}}

            if event.keysym in move_directions:

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:

                    if coord['x'] == 0:
                        move_directions['Left']['move_access'] = False
                        break

                    elif coord['x'] == self.field_x_size - 1:
                        move_directions['Right']['move_access'] = False
                        break

                    elif coord['x'] != 0 and coord['x'] != self.field_x_size - 1:

                        if self.field[coord['y']][coord['x'] - 1] == 1 and coord['left_move_check'] == True:
                            move_directions['Left']['move_access'] = False

                        if self.field[coord['y']][coord['x'] + 1] == 1 and coord['right_move_check'] == True:
                            move_directions['Right']['move_access'] = False

                direction = move_directions[event.keysym]

                if direction['move_access'] == True:
                
                    for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                        self.field[coord['y']].pop(coord['x'])
                        self.field[coord['y']].insert(coord['x'], 0)

                    for rotation in self.figure['figure_rotations']:
                        for coord in rotation:
                            coord[direction['coord']] += direction['move_direction']

                    for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                        self.field[coord['y']].pop(coord['x'])
                        self.field[coord['y']].insert(coord['x'], 1)

                    self.canvas_move_figure(direction)

                    #print(self.field)

    def check_lines(self):

        movable_coords = {str(lines): coord_list for lines in range(1, 5) for coord_list in ([] for i in range(4))}
        line_indexes = []
        scores = {'1':100, '2':300, '3':700, '4':1500}
        
        for index_y in range(len(self.field) - 1, -1, -1):
            if 0 not in self.field[index_y]:
                line_indexes.append(index_y)

        if len(line_indexes) > 0:
            
            for line_index in line_indexes:
                for x in self.field[line_index]:
                    index_x = self.field[line_index].index(x)
                    self.field[line_index][index_x] = 0
                    self.canvas_remove_rectangle(index_x, line_index, self.canvas_stayable_figures)

            #print(self.field)

            dist = 0

            for y in range(len(self.field) - 1, -1, -1):
                for line_index in line_indexes:
                    if y is line_index:
                        dist += 1
                        break

                if dist > 0:
                    for x in range(len(self.field[y])):
                        if self.field[y][x] == 1:
                            self.field[y].pop(x)
                            self.field[y].insert(x, 0)
                            movable_coords[str(dist)].append({'x':x, 'y':y})
            
            #print(self.field)

            if sum([len(movable_coords[str(i)]) for i in range(1, 5)]) > 0:

                for distance, coord_list in movable_coords.items():
                    for coord in coord_list:
                        canvas_coord = copy.deepcopy(coord)
                        coord['y'] += int(distance)
                        self.field[coord['y']].pop(coord['x'])
                        self.field[coord['y']].insert(coord['x'], 1)
                        self.canvas_move_rectangle(canvas_coord, int(distance))

                self.score += scores[str(len(line_indexes))]

                #print(self.field)
                self.canvas.itemconfig(self.score_text, text='Score:' + str(self.score))

    def detect_coord_testability(self):

        move_check_directions = {'Left':{'x':-1, 'y':0, 'check':'left_move_check'},
                                 'Right':{'x':1, 'y':0, 'check':'right_move_check'},
                                 'Down':{'x':0, 'y':1, 'check':'down_move_check'}}

        for coord in self.figure['figure_rotations'][self.figure_rotation_index]:

            for direction in move_check_directions:

                for checkable_coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    
                    if coord['y'] + move_check_directions[direction]['y'] == checkable_coord['y'] and coord['x'] + move_check_directions[direction]['x'] == checkable_coord['x']:
                        coord[move_check_directions[direction]['check']] = False
                        break

                    else:
                        coord[move_check_directions[direction]['check']] = True

    def rotate_figure(self, event):

        if self.game_over == False:

            rotate_access = True

            if self.figure_rotation_index == len(self.figure['figure_rotations']) - 1:
                actual_figure_rotation_index = 0

            else:
                actual_figure_rotation_index = self.figure_rotation_index + 1

            for coord in self.figure['figure_rotations'][actual_figure_rotation_index]:

                coord_check = True

                for coord_name, field_size in {'x':self.field_x_size, 'y':self.field_y_size}.items():

                    if coord[coord_name] < 0 or coord[coord_name] > field_size - 1:

                        rotate_access = False

                if rotate_access == True:

                    if self.figure['figure_rotations'][self.figure_rotation_index] != self.figure['figure_rotations'][actual_figure_rotation_index]:

                        for checkable_coord in self.figure['figure_rotations'][self.figure_rotation_index]:

                            if coord['x'] == checkable_coord['x'] and coord['y'] == checkable_coord['y']:

                                coord['check_rotatability'] = False
                                break

                    coord.setdefault('check_rotatability', True)

                    if self.field[coord['y']][coord['x']] == 1 and coord['check_rotatability'] == True:

                        rotate_access = False

            if rotate_access == True:

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    self.field[coord['y']].pop(coord['x'])
                    self.field[coord['y']].insert(coord['x'], 0)
                    self.canvas_remove_rectangle(coord['x'], coord['y'], self.canvas_figure)

                self.figure_rotation_index = actual_figure_rotation_index

                for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
                    self.field[coord['y']].pop(coord['x'])
                    self.field[coord['y']].insert(coord['x'], 1)

                self.detect_coord_testability()
                self.canvas_display_figure()
                #print(self.field)

    """Canvas Field Display"""

    def canvas_display_figure(self):

        self.canvas_figure = []

        for coord in self.figure['figure_rotations'][self.figure_rotation_index]:
            x = self.figure_piece_size * coord['x'] + self.canvas.coords(self.play_field)[0]
            y = self.figure_piece_size * coord['y'] + self.canvas.coords(self.play_field)[1]
            rect = self.canvas.create_rectangle(x, y, x + self.figure_piece_size, y + self.figure_piece_size, fill=self.figure['color'])
            self.canvas_figure.append(rect)

    def canvas_figure_fall(self):

        for rect in self.canvas_figure:
            self.canvas.move(rect, 0, self.figure_piece_size)

    def canvas_move_figure(self, direction):

        if direction['coord'] == 'x':
            
            for rect in self.canvas_figure:
                self.canvas.move(rect, direction['move_direction'] * self.figure_piece_size, 0)

        elif direction['coord'] == 'y':
            
            for rect in self.canvas_figure:
                self.canvas.move(rect, 0, direction['move_direction'] * self.figure_piece_size)

    def canvas_remove_rectangle(self, x, y, work_list):

        for rect in work_list:

            if self.canvas.coords(rect)[0] == self.figure_piece_size * x + self.canvas.coords(self.play_field)[0]:

                if self.canvas.coords(rect)[1] == self.figure_piece_size * y + self.canvas.coords(self.play_field)[1]:
                    work_list.remove(rect)
                    self.canvas.delete(rect)

    def canvas_move_rectangle(self, coord, lines_amount):

        for rect in self.canvas_stayable_figures:

            if self.canvas.coords(rect)[0] == self.figure_piece_size * coord['x'] + self.canvas.coords(self.play_field)[0]:

                if self.canvas.coords(rect)[1] == self.figure_piece_size * coord['y'] + self.canvas.coords(self.play_field)[1]:

                    self.canvas.move(rect, 0, self.figure_piece_size * lines_amount)
                    break

    def create_field(self, color):

        self.play_field = self.canvas.create_rectangle((canvas_width - (self.field_x_size * self.figure_piece_size)) / 2,
                                                       (canvas_height - (self.field_y_size * self.figure_piece_size)) / 2,
                                                       (canvas_width + (self.field_x_size * self.figure_piece_size)) / 2,
                                                       (canvas_height + (self.field_y_size * self.figure_piece_size)) / 2,
                                                       fill=color)

    def canvas_game_over(self):

        for rect in self.canvas_figure:
            self.canvas.delete(rect)

        self.create_field('#%02x%02x%02x' % (78, 130, 255))

        self.canvas.create_text((self.canvas.coords(self.play_field)[0] + self.canvas.coords(self.play_field)[2]) / 2,
                                (self.canvas.coords(self.play_field)[1] + self.canvas.coords(self.play_field)[3]) / 2,
                                text='GAME OVER', font='Ubuntu 30')            

field = Field(canvas, canvas_width, canvas_height)

def update():
    field.figure_fall()
    canvas.after(1000, update)

root.after(1, update)
root.mainloop()
