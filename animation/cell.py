from xml.etree.ElementTree import PI
from pygame.locals import *
from sys import exit
import time
import random
from math import pi
from animation_config import *
from Bio_Cell import bio_Cell
import math
import numpy as np



class Cell(bio_Cell):
    def __init__(self,gene=None,x=0,y=0,
                size=(ENLARGE_RATE,ENLARGE_RATE),
                rand_gene=True,rand_pos = True, facing=-1):

        super().__init__(gene,rand_gene)

        # self._color=self.__get_color()

        if rand_pos:
            self._x = random.randint(1,GRID_SIZE[0])*ENLARGE_RATE
            self._y = random.randint(1,GRID_SIZE[1])*ENLARGE_RATE
            #print(str(self.x)+'  '+str(self.y))
        else:
            self._x =x*ENLARGE_RATE
            self._y =y*ENLARGE_RATE
        self._size = size
        if facing==-1:
            self._facing = random.randint(0,3)
            # 0:up
            # 1:down
            # 2:left
            # 3:right
        if self._facing == 0:
            self._next = (-1,0)
        if self._facing == 1:
            self._next = (1,0)
        if self._facing == 2:
            self._next = (0,-1)
        if self._facing == 3:
            self._next = (0,1)

        self.grid = []

        pass

    def __hash_gene(self):
        pass

    def __get_color(self):
        # get color from gene

        pass

    def update_grid(self,grid):
        self.grid = grid
    
    def get_position(self):
        return (self._x,self._y)
    
    def get_grid_position(self):
        return (int(self._x/ENLARGE_RATE),int(self._y/ENLARGE_RATE))
    
    def get_color(self):
        return self._color
    
    def get_size(self):
        return self._size
    
    def detect_next_pixel_type(self):
        (x,y) = self.get_grid_position()
        ele = self.grid[x+self._next[0]][y+self._next[1]]
        # if ele==0.5 or ele==-0.5:
        #     return 0
        return ele

    def detect_next_pixel_cell_or_pred(self):
        (x,y) = self.get_grid_position()
        ele = self.grid[x+self._next[0]][y+self._next[1]]
        if ele==1 or ele==-1:
            return 0
        return ele
    
    def detect_last_pixel(self):
        (x,y) = self.get_grid_position()
        return self.grid[x-self._next[0]][y-self._next[1]]
    
    def detect_west_pixel(self):
        (x,y) = self.get_grid_position()
        return self.grid[x-1][y]
    
    def detect_east_pixel(self):
        (x,y) = self.get_grid_position()
        return self.grid[x+1][y]
    
    def detect_south_pixel(self):
        (x,y) = self.get_grid_position()
        return self.grid[x][y+1]
    
    def detect_north_pixel(self):
        (x,y) = self.get_grid_position()
        return self.grid[x][y-1]

    def set_position(self,x,y):
        self._x = x
        self._y = y

    # def set_size(self,size):
    #     self.__size = size
    
    # def set_size(self,hight, width):
    #     self.__size = (hight, width)

    # def set_color(self,color):
    #     self.color = color

    # def set_color(self,r,g,b):
    #     self.color = (r,g,b)

class motor_Cell(Cell):
    def __init__(self,gene=None, x=0, y=0, 
                c=(random.randint(69, 196), random.randint(69, 196), random.randint(196, 255)), 
                size=(ENLARGE_RATE, ENLARGE_RATE), 
                rand_gene=True,rand_pos=True, facing=-1,is_pred=False):
                
        super().__init__(gene,x, y, size, rand_gene, rand_pos, facing)
        self.is_pred = is_pred
        self.selected = False
        self._color=c
        self.color2 = (200,33,0)
        if self.is_pred:
            self._color=PRED_COLOR
    
    def switch(self):
        if self.is_pred is False:
            self.is_pred = True
            self._color = PRED_COLOR
        else:
            self._color = (random.randint(69, 196), random.randint(69, 196), random.randint(196, 255))

    def __facing_direction_ew(self):
        i = self._facing
        if i == 2:
            return 1
        if i == 3:
            return -1
        else:
            return 0

    def __facing_direction_ns(self):
        i = self._facing
        if i == 0:
            return 1
        if i == 1:
            return -1
        else:
            return 0

    def __normalize(self,num):
        return math.tanh(num)

    def __get_age(self):
        if REFRESH_MODE:
            return self.age/ERA_LENGTH
        return self.age/CELL_AGE
    
    def __get_ew_location(self):
        (x,y) = self.get_grid_position()
        return x/GRID_SIZE[0]
    
    def __get_sn_location(self):
        (x,y) = self.get_grid_position()
        return y/GRID_SIZE[1]
    
    def __get_random_input(self):
        return random.uniform(-1,1)
    
    def __get_random_input_2(self):
        return random.random()*2-1

    def __get_oscillation(self):
        return math.cos(self.age)
    
    def __get_next_pixel_food_or_wall(self):
        return self.detect_next_pixel_type()
    
    def __get_next_pixcel_cell_or_pred(self):
        return self.detect_next_pixel_cell_or_pred()
    
    def __see_pixel_type_and_distance(self):
        (x,y) = self.get_grid_position()
        f = self._facing
        target_pix = 0
        distance = 0
        while target_pix==0:
            distance += 1
            if f==0:
                y-=1
            if f==1:
                y+=1
            if f==2:
                x-=1
            if f==3:
                x+=1
            target_pix=self.grid[x][y]
        return target_pix,distance/GRID_SIZE[0]


    def _move_forward(self):
        self._x += self._next[0]*ENLARGE_RATE
        self._y += self._next[1]*ENLARGE_RATE
    
    def _move_backward(self):
        self._x -= self._next[0]*ENLARGE_RATE
        self._y -= self._next[1]*ENLARGE_RATE

    def _move_south(self):
        self._y += ENLARGE_RATE
    
    def _move_north(self):
        self._y -= ENLARGE_RATE
    
    def _move_west(self):
        self._x -= ENLARGE_RATE
    
    def _move_east(self):
        self._x += ENLARGE_RATE
    
    def _turn_left(self):
        if self._facing==0:
            self._facing=2
        elif self._facing==1:
            self._facing=3
        elif self._facing==2:
            self._facing=1
        elif self._facing==3:
            self._facing=0
    
    def _turn_right(self):
        if self._facing==0:
            self._facing=3
        elif self._facing==1:
            self._facing=2
        elif self._facing==2:
            self._facing=0
        elif self._facing==3:
            self._facing=1
    
    def __get_signals(self):
    # return a list with all the input signals that sensors can detect.
        (see_type,see_dis) = self.__see_pixel_type_and_distance()
        signals = [self.__get_random_input(),
        self.__get_oscillation(),
        self.__get_age(),
        self.__get_ew_location(),
        self.__get_sn_location(),
        self.__facing_direction_ew(),
        self.__facing_direction_ns(),
        self.__get_random_input_2(),
        1,
        self.__get_next_pixel_food_or_wall(),
        see_type,
        see_dis]
        return(signals)

    
    def __get_activation_function_id(self):
        # self.brain:Node.Brain() = self.brain

        a=self.brain.get_output(self.__get_signals())
        return a
    
    # def __eat_food(self,detect_food,actid):
    #     [f_f,b_f,s_f,w_f,n_f,e_f]=detect_food
    #     if actid==MF and f_f:
    #         self._move_forward()
    #     if actid==MB and b_f:
    #         self._move_backward()
    #     if actid==MN and n_f:
    #         self._move_north()
    #     if actid==MS and s_f:
    #         self._move_south()
    #     if actid==ME and e_f:
    #         self._move_east()
    #     if actid==MW and w_f:
    #         self._move_west()
        
    #     if actid==ST:
    #         # small number didn't trigger the activator
    #         pass

    #     pass

    def __take_action(self,facing_block=False,backing_block=False,w_b=False,e_b=False,s_b=False,n_b=False):
    # take input and activate one of the activation function
        actid = self.__get_activation_function_id()

        if actid==MF and not facing_block:
            self._move_forward()
        if actid==MB and not backing_block:
            self._move_backward()
        if actid==MN and not n_b:
            self._move_north()
        if actid==MS and not s_b:
            self._move_south()
        if actid==ME and not e_b:
            self._move_east()
        if actid==MW and not w_b:
            self._move_west()
        
        if actid==TR:
            self._turn_right()
        if actid==TL:
            self._turn_left()
        
        if actid==ST:
            # small number didn't trigger the activator
            pass
        
        pass
    
    def update(self):
        # the function is called every frame

        # update the age each frame
        self.age += 1

        if self.age>=CELL_AGE and self.is_pred is False:
            self.death = True
        
        if self.age>=PREDATOR_AGE and self.is_pred:
            self.death = True

        facing_block=False
        backing_block=False
        s_b=False
        w_b=False
        n_b=False
        e_b=False

        # f_f=False
        # b_f=False
        # s_f=False
        # w_f=False
        # n_f=False
        # e_f=False

        next_pixel = self.detect_next_pixel_type()
        last_pixel = self.detect_last_pixel()
        south_pixel = self.detect_south_pixel()
        north_pixel = self.detect_north_pixel()
        west_pixel = self.detect_west_pixel()
        east_pixel = self.detect_east_pixel()

        # if next_pixel == ELE_FOOD:
        #     f_f=True
        # if last_pixel == ELE_FOOD:
        #     b_f=True
        # if south_pixel == ELE_FOOD:
        #     s_f=True
        # if north_pixel == ELE_FOOD:
        #     n_f=True
        # if west_pixel == ELE_FOOD:
        #     w_f=True
        # if east_pixel == ELE_FOOD:
        #     e_f=True
        
        # detect_food = [f_f,b_f,s_f,w_f,n_f,e_f]
        if self.is_pred:
            if next_pixel == ELE_WALL or next_pixel == ELE_PRED:
                facing_block=True
            if last_pixel == ELE_WALL or last_pixel == ELE_PRED:
                backing_block=True
            if south_pixel == ELE_WALL or south_pixel == ELE_PRED:
                s_b=True
            if north_pixel == ELE_WALL or north_pixel == ELE_PRED:
                n_b=True
            if west_pixel == ELE_WALL or west_pixel == ELE_PRED:
                w_b=True
            if east_pixel == ELE_WALL or east_pixel == ELE_PRED:
                e_b=True
        else:
            if next_pixel == ELE_CELL or next_pixel == ELE_WALL:
                facing_block=True
            if last_pixel == ELE_CELL or last_pixel == ELE_WALL:
                backing_block=True
            if south_pixel == ELE_CELL or south_pixel == ELE_WALL:
                s_b=True
            if north_pixel == ELE_CELL or north_pixel == ELE_WALL:
                n_b=True
            if west_pixel == ELE_CELL or west_pixel == ELE_WALL:
                w_b=True
            if east_pixel == ELE_CELL or east_pixel == ELE_WALL:
                e_b=True
        
        # if next_pixel==ELE_EMPTY:
        #     self._move_forward()

        self.__take_action(facing_block,backing_block,w_b,e_b,s_b,n_b)


# class decoder():
#     def __init__(self) -> None:
#         pass

#     def __normalize(self,num):
#         return math.tanh(num)

#     def __get_input_return(self,char,cell:motor_Cell):
#         if char=='a':
#             return random.uniform(-1,1)
#         pass

#     def get_response(self,neural:str,cell:motor_Cell):
#         # print(cell.get_grid_position())
#         if neural[0] in LOWER:
#             input = self.__get_input_return(neural[0],cell)
#         else:
#             input = self.__get_input_return



class food():
    def __init__(self,x=0,y=0,c=(138, 213, 138),size=(ENLARGE_RATE,ENLARGE_RATE),rand_pos=True):
        if rand_pos:
            self._x = random.randint(1,GRID_SIZE[0])*ENLARGE_RATE
            self._y = random.randint(1,GRID_SIZE[1])*ENLARGE_RATE
        else:
            self._x =x*ENLARGE_RATE
            self._y =y*ENLARGE_RATE
        self._color=c
        self._size=size
        self.eaten=False
        self.age=0
    
    def get_position(self):
        return (self._x,self._y)
    
    def get_grid_position(self):
        return (int(self._x/ENLARGE_RATE),int(self._y/ENLARGE_RATE))
    
    def get_color(self):
        return self._color
    
    def get_size(self):
        return self._size