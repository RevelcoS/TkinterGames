'Minesweeper coding challendge'
'Need Mouse to Play'

from tkinter import *
import random
import timeit

canvas_width = 600
canvas_height = 600

field_x_size = 10
field_y_size = 10

game_over = False
mines = 10

root = Tk()
root.title('Minesweeper')
root.wm_attributes('-topmost', True)
canvas = Canvas(width=canvas_width, height=canvas_height, bg='#%02x%02x%02x' % (100, 100, 100))
canvas.pack(expand=True, fill=BOTH)
canvas.focus_set()

class Cell():

    def __init__(self, canvas, x, y, canvas_width, canvas_height, field_x_size, field_y_size):

        self.canvas = canvas

        self.cell_size = 50
        self.mined = False
        self.activated = False
        self.flag_placed = False
        self.near_mines = 0

        toal_y = (canvas_height - field_y_size * self.cell_size) / 2 + y * self.cell_size
        total_x = (canvas_width - field_x_size * self.cell_size) / 2 + x * self.cell_size
        self.cell = self.canvas.create_rectangle(total_x, toal_y, total_x + self.cell_size, toal_y + self.cell_size, fill='#%02x%02x%02x' % (200, 200, 200))

def check_win():
    win = True
    for y in range(field_y_size):
        for x in range(field_x_size):
            if field[y][x].mined and not field[y][x].flag_placed or not field[y][x].activated and not field[y][x].mined:
                win = False
    return win

def show_status(cell):
    colors = {'1':'#0000FF', '2':'#009900', '3':'#DC0C04', '4':'#06036D', '5':'#740302', '6':'#069CB7', '7':'#990066', '8':'#0A0A0A'}
    cell.activated = True
    cell.canvas.itemconfig(cell.cell, fill='#%02x%02x%02x' % (255, 255, 255))
    if cell.near_mines != 0:
        cell.canvas.create_text(cell.canvas.coords(cell.cell)[0] + cell.cell_size / 2,
                                cell.canvas.coords(cell.cell)[1] + cell.cell_size / 2,
                                text=str(cell.near_mines), font=('Ubuntu ' + str(int(cell.cell_size / 2.5))), fill=colors[str(cell.near_mines)])

def identify_status(event, cell, coord, field):
    global game_over
    if not game_over and not check_win():
        if not cell.activated and not cell.flag_placed:
            if cell.mined:
                game_over = True
                print('Game_over')
                for y in range(field_y_size):
                    for x in range(field_x_size):
                        if field[y][x].mined and field[y][x].flag_placed:
                            field[y][x].canvas.itemconfig(field[y][x].cell, fill='#F08080')
                        elif field[y][x].mined:
                            field[y][x].canvas.itemconfig(field[y][x].cell, fill='red')
            else:
                if cell.near_mines == 0:
                    near_zeros = []
                    near_zeros.append({'x':coord['x'], 'y':coord['y']})
                    while len(near_zeros) > 0:
                        for zero_coord in near_zeros:
                            for y in range(zero_coord['y'] - 1, zero_coord['y'] + 2):
                                if y >= 0 and y < field_y_size:
                                    for x in range(zero_coord['x'] - 1, zero_coord['x'] + 2):
                                        if x >= 0 and x < field_x_size:
                                            if not field[y][x].activated and not field[y][x].flag_placed:
                                                show_status(field[y][x])
                                                if field[y][x].near_mines == 0:
                                                    near_zeros.append({'x':x, 'y':y})
                            near_zeros.remove(zero_coord)                          
                else:
                    show_status(cell)
            if check_win():
                print('Minesweeper comlete in ' + str(timeit.default_timer() - timer) + ' seconds')

def place_flag(event, cell, mines):
    global game_over
    if not game_over and not check_win() and not cell.activated:
        if not cell.flag_placed:
            cell.canvas.itemconfig(cell.cell, fill='green')
            cell.flag_placed = True
        else:
            cell.canvas.itemconfig(cell.cell, fill='#%02x%02x%02x' % (200, 200, 200))
            cell.flag_placed = False
        if check_win():
            print('Minesweeper complete in ' + str(timeit.default_timer() - timer) + ' seconds')

field = []

for y in range(field_y_size):
    coord_y = []
    for x in range(field_x_size):
        cell = Cell(canvas, x, y, canvas_width, canvas_height, field_x_size, field_y_size)
        cell.canvas.tag_bind(cell.cell, '<Button-1>', lambda event, cell=cell, coord={'y':y, 'x':x}, field=field: identify_status(event, cell, coord, field))
        cell.canvas.tag_bind(cell.cell, '<Button-2>', lambda event, cell=cell, mines=mines: place_flag(event, cell, mines))
        coord_y.append(cell)
    field.append(coord_y)



mine_coords = []

for i in range(mines):
    coord = {'x':random.randint(0, field_x_size - 1), 'y':random.randint(0, field_y_size - 1)}
    while coord in mine_coords:
        coord = {'x':random.randint(0, field_x_size - 1), 'y':random.randint(0, field_y_size - 1)}
    mine_coords.append(coord)
    field[coord['y']][coord['x']].mined = True
    for y in range(coord['y'] - 1, coord['y'] + 2):
        if y >= 0 and y < field_y_size:
            for x in range(coord['x'] - 1, coord['x'] + 2):
                if x >= 0 and x < field_x_size:
                    if not field[y][x].mined:
                        field[y][x].near_mines += 1

timer = timeit.default_timer()

root.update()
root.mainloop()
