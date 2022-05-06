import pygame
from pygame.locals import *
from sys import exit
import time
import random
from math import pi
from animation_config import *
from cell import *
import copy

class mutant():
    def __init__(self):
        pass

    def __copy(self,father:motor_Cell):
        gene = father.gene
        (x,y) = father.get_grid_position()
        if father.is_pred:
            return motor_Cell(gene,x,y,rand_gene=False,rand_pos=False,is_pred=True)
        return motor_Cell(gene,x,y,rand_gene=False,rand_pos=False)
    
    def _fix(self,gene):
        # fix the messy inner neural
        new_gene=[]
        an=-1
        bn=-1
        cn=-1

        conta=[0 for i in range(MAX_NEURAL_NUM)]
        contb=[0 for i in range(MAX_NEURAL_NUM)]
        contc=[0 for i in range(MAX_NEURAL_NUM)]
        # for i in range(len(gene)):
        #     g_piece = gene[i]
        #     if g_piece[3] == AND:
        #         conta[int(g_piece[4:6])]+=1
        #         if conta[int(g_piece[4:6])] >2:
        #             gene[i] = gene[i][:4]+'00'+gene[i][6:]
        #     if g_piece[3] == OR:
        #         contb[int(g_piece[4:6])]+=1
        #         if contb[int(g_piece[4:6])] >2:
        #             gene[i] = gene[i][:4]+'00'+gene[i][6:]
        #     if g_piece[3] == XOR:
        #         contc[int(g_piece[4:6])]+=1
        #         if contc[int(g_piece[4:6])] >2:
        #             gene[i] = gene[i][:4]+'00'+gene[i][6:]

        for i in range(len(gene)):
            g_piece = gene[i]
            if g_piece[3] == AND:
                gene[i] = gene[i][:4]+'00'+gene[i][6:]
            if g_piece[3] == OR:
                gene[i] = gene[i][:4]+'00'+gene[i][6:]
            if g_piece[3] == XOR:
                gene[i] = gene[i][:4]+'00'+gene[i][6:]


        for i in range(len(gene)):
            g_piece = gene[i]
            if g_piece[3]==AND:
                an+=1
            if g_piece[3]==OR:
                bn+=1
            if g_piece[3]==XOR:
                cn+=1
        am=int(an/2)+1
        bm=int(bn/2)+1
        cm=int(cn/2)+1
        for i in range(len(gene)):
            g_piece = gene[i]

            if g_piece[0] == AND and g_piece[1:3]=='00':
                g_piece=g_piece[0]+str(random.randint(1,am)).zfill(2)+g_piece[3:]
            if g_piece[3] == AND and g_piece[4:6]=='00':
                g_piece=g_piece[:4]+str(int(an/2)+1).zfill(2)+g_piece[6:]
                #print(g_piece)
                an-=1
            
            if g_piece[0] == OR and g_piece[1:3]=='00':
                g_piece=g_piece[0]+str(random.randint(1,bm)).zfill(2)+g_piece[3:]
            if g_piece[3] == OR and g_piece[4:6]=='00':
                g_piece=g_piece[:4]+str(int(bn/2)+1).zfill(2)+g_piece[6:]
                #print(g_piece)
                bn-=1
    
            if g_piece[0] == XOR and g_piece[1:3]=='00':
                g_piece=g_piece[0]+str(random.randint(1,cm)).zfill(2)+g_piece[3:]
            if g_piece[3] == XOR and g_piece[4:6]=='00':
                g_piece=g_piece[:4]+str(int(cn/2)+1).zfill(2)+g_piece[6:]
                #print(g_piece)
                cn-=1
            new_gene.append(g_piece)
        
        for i in range(len(new_gene)):
            g_piece:list[str] = new_gene[i]
            if int(g_piece[1:3])>MAX_NEURAL_NUM:
                new_gene[i]=g_piece[0].lower()+g_piece[1:]
            if int(g_piece[4:6])>MAX_NEURAL_NUM:
                new_gene[i]=g_piece[:3]+g_piece[3].lower()+g_piece[4:]

        return new_gene

    
    def mutate_link(self,father:motor_Cell):
        rand = random.random()
        (x,y) = father.get_grid_position()
        c = father._color
        if rand<LINK_MU_RATE:
            new_gene=[]
            in_table = SENSORS+NEURALS
            out_table = NEURALS+ACTIVATORS
            fgene = copy.deepcopy(father.gene)
            for fgene_piece in fgene:
                rand1 = random.random()
                rand2 = random.random()
                if rand2<PIECE_LINK_MU_RATE:

                    # start mutation
                    if rand1<0.5:
                        # mutate input part
                        fgene_piece=in_table[random.randint(0,len(in_table)-1)]+fgene_piece[1:]
                    else:
                        # mutate ouput part
                        fgene_piece=fgene_piece[:3]+out_table[random.randint(0,len(out_table)-1)]+fgene_piece[4:]
                new_gene.append(fgene_piece)

                # mutate the color
                c=[c[0]+(random.randint(0,20))-10,c[1]+(random.randint(0,6))-3,c[2]+(random.randint(0,6)-3)]
                if c[0]>255:
                    c[0]=255
                if c[1]>255:
                    c[1]=255
                if c[2]>255:
                    c[2]=255
                if c[0]<0:
                    c[0]=0
                if c[1]<0:
                    c[1]=0
                if c[2]<0:
                    c[2]=0
            if father.is_pred:
                return motor_Cell(self._fix(new_gene),x,y,c=c,rand_gene=False,rand_pos=False,is_pred=True)
            return motor_Cell(self._fix(new_gene),x,y,c=c,rand_gene=False,rand_pos=False)
        return self.__copy(father)


    def mutate_weight(self,father:motor_Cell):

        rand = random.random()
        if rand<WEIGHT_MU_RATE:
            return self.__copy(father)
        else:
            new_gene = []
            (x,y) = father.get_grid_position()
            gene = copy.deepcopy(father.gene)
            for i in range(len(gene)):
                g_piece = gene[i]
                rand2 = random.random()
                if rand2<PIECE_WEIGHT_MU_RATE:
                    weight = int(g_piece[6:])
                    weight += random.randint(-WEIGHT_MU_RADIUS,WEIGHT_MU_RADIUS)
                    if weight>99:
                        weight=99
                    if weight<-99:
                        weight=-99
                    str_weight = str(weight).zfill(2)
                    if str_weight[0]=='-':
                        str_weight = '-'+str_weight[1:].zfill(2)
                    if str_weight[0]!='-':
                        str_weight = '+'+str_weight

                    g_piece=g_piece[:6]+str_weight
                    
                new_gene.append(g_piece)
            
            if father.is_pred:
                return motor_Cell(new_gene,x,y,rand_gene=False,rand_pos=False,is_pred=True)
            return motor_Cell(new_gene,x,y,rand_gene=False,rand_pos=False)


class Filed():

    def __init__(self,cells=None,foods=None):
        self.survival = 0
        self.forbidden = DeathArea()
        self.gene_pool = {}
        self.gene_lst = []
        self.mu = mutant()
        self.cells:list[motor_Cell] = cells
        self.foods:list[food] = foods
        self.grid = [[ELE_WALL for i in range(GRID_SIZE[0]+2)] for i in range(GRID_SIZE[1]+2)]

        for i in range(1,GRID_SIZE[0]+1):
            for j in range(1,GRID_SIZE[1]+1):
                self.grid[i][j]=ELE_EMPTY
        
        for obj in self.cells:
            obj.update_grid(self.grid)
        pass

    def __find_cell(self,grid_pos):
        # find cell(no predator)
        for i in range(len(self.cells)):
            obj = self.cells[i]
            if obj.is_pred:
                continue
            pos = obj.get_grid_position()
            if pos == grid_pos:
                return obj
        return False

    def mark_cells(self,rank):
        str_gene:str=self.gene_pool[rank-1][0]
        gene = str_gene.split()
        for obj in self.cells:
            if obj.gene==gene:
                obj._color,obj.color2 = obj.color2,obj._color


    def __reproduce(self):
        new_cells:list[motor_Cell] = []
        for i in range(len(self.cells)):
            obj = self.cells[i]
            if obj.is_pred:
                if obj.cell_storage>PREDATOR_REPRODUCE_THRESHOULD:
                    obj.cell_storage=0
                    rand = random.random()
                    if rand<0.5:
                        new_cells.append(self.mu.mutate_weight(obj))
                    else:
                        new_cells.append(self.mu.mutate_link(obj))
            else:
                if obj.food_storage>REPRODUCE_THRESHOULD:
                    obj.food_storage=0
                    rand = random.random()
                    if rand<0.5:
                        new_cells.append(self.mu.mutate_weight(obj))
                    else:
                        new_cells.append(self.mu.mutate_link(obj))
        
        has_pred=False
        for obj in self.cells:
            if obj.is_pred:
                has_pred=True
                
        for obj in new_cells:
            rd = random.random()
            if not has_pred:
                if rd<MU_PREDATOR_RATE:
                    obj.switch()
            self.cells.append(obj)

        # update the gene pool
        # for obj in new_cells:
        #     strgene=''
        #     for gene_piece in obj.gene:
        #         strgene+=str(gene_piece)+'_'
        #     try:
        #         self.gene_pool[strgene]+=1
        #     except:
        #         self.gene_pool[strgene]=1
        # pass
    
    def __clean_death(self):
        deaths = []
        for i in range(len(self.cells)):
            obj=self.cells[i]
            if obj.death:
                deaths.append(obj)
        for i in deaths:
            self.cells.remove(i)
        pass
    
    def __clean_eaten(self):
        deaths = []
        for i in range(len(self.foods)):
            obj=self.foods[i]
            if obj.eaten:
                deaths.append(obj)
        for i in deaths:
            self.foods.remove(i)
        pass

    def __gen_food(self,num=GEN_FOOD_RATE):
        for i in range(num):
            new_food = food()
            self.foods.append(new_food)
    
    def __gen_cell(self,num=GEN_CELL_RATE):
        c=(random.randint(69, 255), random.randint(0, 128), random.randint(69, 255))
        new_cell = motor_Cell(c=c)
        self.cells.append(new_cell)
    
    def __update_gene_pool(self):
        # update the gene pool

        self.gene_pool = {}
        self.gene_lst = []
        for obj in self.cells:
            strgene=''
            for gene_piece in obj.gene:
                strgene+=str(gene_piece)+' '
            try:
                self.gene_pool[strgene]+=1
            except:
                self.gene_pool[strgene]=1
            
        self.gene_pool = sorted(self.gene_pool.items(),key=lambda x:x[1],reverse=True)
        top = 11
        for i in self.gene_pool:
            top-=1
            if top == 0:
                break
            self.gene_lst.append(str(i[0][:SHOWN_GENE_LENGTH])+': '+str(i[1]))
        
        #print(self.gene_lst)
        pass

    def judge_death(self):
        for obj in self.cells:
            self.forbidden.judge(obj)
        self.__clean_death()
    
    def __refresh_mutate(self,cell:motor_Cell):
        rand1 = random.random()
        rand2 = random.random()
        if rand1<0.5:
            if rand2<WEIGHT_MU_RATE:
                return self.mu.mutate_weight(cell)
        else:
            if rand2<LINK_MU_RATE:
                return self.mu.mutate_link(cell)
        return copy.deepcopy(cell)
    
    def __shuffle_pos(self):
        positions = []
        for i in range(len(self.cells)):
            randx = random.randint(1,GRID_SIZE[0])*ENLARGE_RATE
            randy = random.randint(1,GRID_SIZE[1])*ENLARGE_RATE
            while (randx,randy) in positions:
                randx = random.randint(1,GRID_SIZE[0])*ENLARGE_RATE
                randy = random.randint(1,GRID_SIZE[1])*ENLARGE_RATE
            positions.append((randx,randy))
        
        for i in range(INDIVIDUAL_NUM):
            self.cells[i].set_position(positions[i][0],positions[i][1])

            
    
    def respread(self):
        # only activated in refresh mode

        # reset the grid to empty
        for i in range(1,GRID_SIZE[0]+1):
            for j in range(1,GRID_SIZE[1]+1):
                self.grid[i][j]=ELE_EMPTY
        
        self.judge_death()
        self.survival = len(self.cells)/INDIVIDUAL_NUM
        new_cells = []
        while len(self.cells)+len(new_cells)<INDIVIDUAL_NUM:
            rd = random.randint(0,len(self.cells)-1)
            randcell = self.cells[rd]
            new_cell = self.__refresh_mutate(randcell)
            new_cells.append(new_cell)

        for i in new_cells:
            self.cells.append(i)
        
        self.__shuffle_pos()


    def update(self,steps):
        
        # generate food
        if not REFRESH_MODE:
            self.__gen_food()

        # generate cell
        if steps%GEN_CELL_RATE==0:
            self.__gen_cell()

        # cell die due to enter death area
        if not REFRESH_MODE:
            self.judge_death()

        # update the cell position

        # the cells are very good at looking for bugs
        # they found that if more than one cells have the same pos next frame, they will overlap
        # so sometimes they are going to merge at the corner to let the corner store more cells
        # bug fixed anyway, but it is interesting

        for obj in self.cells:
            obj.update_grid(self.grid)
            (x,y) = obj.get_grid_position()
            self.grid[x][y] = ELE_EMPTY
            obj.update()
            (x,y) = obj.get_grid_position()
            if obj.is_pred:
                self.grid[x][y] = ELE_PRED
            else:
                self.grid[x][y] = ELE_CELL

        # cell eats food or food die due to age (update food)
        if not REFRESH_MODE:
            for i  in range(len(self.foods)):
                obj = self.foods[i]
                obj.age+=1
                if obj.age>FOOD_MAX_AGE:
                    # food die
                    obj.eaten=True
                (x,y) = obj.get_grid_position()
                if self.grid[x][y] == ELE_CELL:
                    # food been eatean
                    obj.eaten=True
        
        # predator eats cell
        if not REFRESH_MODE:
            for i in range(len(self.cells)):
                obj = self.cells[i]
                if obj.is_pred:
                    pos = obj.get_grid_position()
                    cell = self.__find_cell(pos)
                    if cell is not False:
                        cell.death=True
                        obj.age-=100
                        obj.cell_storage+=1

        
        # update foods position
        if not REFRESH_MODE:
            for obj in self.foods:
                (x,y) = obj.get_grid_position()
                self.grid[x][y] = ELE_FOOD
        
        # cell eats food (update cell)
        if not REFRESH_MODE:
            for i  in range(len(self.cells)):
                obj = self.cells[i]
                if obj.is_pred:
                    continue
                (x,y) = obj.get_grid_position()
                if self.grid[x][y] == ELE_FOOD:
                    # cell live longer
                    # obj.age -= 10
                    # obj.age = 0
                    obj.food_storage += 1
        
        # for i in self.grid:
        #     print(i)

        if not REFRESH_MODE:
            self.__reproduce()
            self.__clean_death()
            self.__clean_eaten()

        # update gene pool
        self.__update_gene_pool()

        for obj in self.cells:
            obj.update_grid(self.grid)
        pass

# t = mutant()
# gene=['A01C02+94', 'A01C02+94','C00C02+94','A01C00+94','C00C00+94']
# print(gene)
# print(t._fix(gene))


class DeathArea():
    def __init__(self):
        self.left_top_list = LEFTTOP
        self.right_bottom_list = RIGHTBOTTOM
    
    def judge(self,cell:motor_Cell):
        (x,y) = cell.get_grid_position()
        for i in range(0,len(self.right_bottom_list)):
            if x>=self.left_top_list[i][0] and x<=self.right_bottom_list[i][0] and y>=self.left_top_list[i][1] and y<=self.right_bottom_list[i][1]:
                cell.death = True