from tracemalloc import stop
import pygame
from pygame.locals import *
from sys import exit
import time
from random import *
from animation_config import *
from cell import motor_Cell,food
from filed import Filed

class game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('EvoSim')

        self.playground = Filed([motor_Cell() for i in range(INDIVIDUAL_NUM)],
                            [food() for i in range(GEN_FOOD_RATE)])

        self.screen=pygame.display.set_mode(FRAME_SIZE, 0, FRAME_RATE)
        self.font = pygame.font.SysFont('Times',20)
        self.stop=False
        self.era = 0
        self.era_step = 0
        self.steps=0
        self.liv_cell_num = 0
        self.predator_num = 0
        self.gene_pool_top10_text = []
        self.survive_sum = 0
    


    def __draw_sidebar(self,playground:Filed):
        steps_text = self.font.render('step '+str(self.steps),True,(0,0,0),(255,255,255))
        self.screen.blit(steps_text,(FRAME_SIZE[1]+20,20))
        liv_cell_num_text = self.font.render('living cell '+str(self.liv_cell_num),
                                            True,(0,0,0),(255,255,255))
        self.screen.blit(liv_cell_num_text,(FRAME_SIZE[1]+20,40))
        pred_num_text = self.font.render('predator '+str(self.predator_num),
                                            True,(0,0,0),(255,255,255))
        self.screen.blit(pred_num_text,(FRAME_SIZE[1]+180,40))

        eras_text = self.font.render('era '+str(self.era),True,(0,0,0),(255,255,255))
        self.screen.blit(eras_text,(FRAME_SIZE[1]+20,60))
        eras_steps_text = self.font.render('era_steps '+str(self.era_step),True,(0,0,0),(255,255,255))
        self.screen.blit(eras_steps_text,(FRAME_SIZE[1]+180,20))
        gene_length_text = self.font.render('gene length: '+str(RAND_GENE_LENGTH),True,(0,0,0),(255,255,255))
        self.screen.blit(gene_length_text,(FRAME_SIZE[1]+20,FRAME_SIZE[1]-40))
        deadzone_text = self.font.render('dead zone: '+str(LEFTTOP)+' '+str(RIGHTBOTTOM),True,(0,0,0),(255,255,255))
        self.screen.blit(deadzone_text,(FRAME_SIZE[1]+25,FRAME_SIZE[1]-60))
        if REFRESH_MODE:
            if self.era==1:
                mean_survival_text = self.font.render('average survive rate: '+'%',True,(0,0,0),(255,255,255))
                self.screen.blit(mean_survival_text,(FRAME_SIZE[1]+180,40))
            else:
                mean_survival_text = self.font.render('average survive rate: '+str(self.survive_sum/(self.era-1)*100)+'%',True,(0,0,0),(255,255,255))
                self.screen.blit(mean_survival_text,(FRAME_SIZE[1]+180,40))
            survival_text = self.font.render('survive rate: '+str(playground.survival*100)+'%',True,(0,0,0),(255,255,255))
            self.screen.blit(survival_text,(FRAME_SIZE[1]+180,60))
            era_text = self.font.render('era_length: '+str(ERA_LENGTH),True,(0,0,0),(255,255,255))
            self.screen.blit(era_text,(FRAME_SIZE[1]+180,FRAME_SIZE[1]-40))

        hight = 80
        for i in self.gene_pool_top10_text:
            hight += 20
            self.screen.blit(i,(FRAME_SIZE[1]+20,hight))
        
        pass



    def __update_sidebar(self,playground:Filed):
        self.predator_num = 0
        for obj in playground.cells:
            if obj.is_pred:
                self.predator_num+=1

        gl = playground.gene_lst
        self.gene_pool_top10_text=[]
        for i in range(len(gl)):
            text = self.font.render(gl[i],True,(0,0,0),(255,255,255))
            self.gene_pool_top10_text.append(text)
        
        if REFRESH_MODE:
            if self.era_step==1:
                self.survive_sum+=playground.survival
                #print(self.survive_sum)

        pass



    def draw_frame(self,screen:pygame.Surface,playground:Filed):
        screen.fill((255, 255, 255))
        cells = playground.cells
        foods = playground.foods
        for r in foods:
            rc = r.get_color()
            (x,y) =r.get_position()
            rp = (x-ENLARGE_RATE,y-ENLARGE_RATE)
            rs = r.get_size()
            pygame.draw.rect(screen, rc, Rect(rp, rs))
        for r in cells:
            rc = r._color
            (x,y) =r.get_position()
            rp = (x-ENLARGE_RATE,y-ENLARGE_RATE)
            rs = r.get_size()
            f = r._facing
            pygame.draw.rect(screen, rc, Rect(rp, rs))

            # draw facing direction
            if f==0:
                pygame.draw.rect(screen,(0,0,0),Rect(rp,(ENLARGE_RATE,2)))
            if f==1:
                pygame.draw.rect(screen,(0,0,0),Rect((rp[0],rp[1]+ENLARGE_RATE-2),(ENLARGE_RATE,2)))
            if f==2:
                pygame.draw.rect(screen,(0,0,0),Rect(rp,(2,ENLARGE_RATE)))
            if f==3:
                pygame.draw.rect(screen,(0,0,0),Rect((rp[0]+ENLARGE_RATE-2,rp[1]),(2,ENLARGE_RATE)))

        self.__draw_sidebar(playground)

    def __refresh_world(self,playground:Filed):
        playground.respread()
        return playground

    def update_frame(self,playground:Filed):

        if REFRESH_MODE and self.era_step>ERA_LENGTH:
            self.steps-=1
            self.era_step=0
            self.era += 1
            self.playground = self.__refresh_world(self.playground)

        self.liv_cell_num = len(playground.cells)
        self.steps+=1
        self.era_step+=1
        playground.update(self.steps)
        pass



        self.__update_sidebar(playground)



    def manuplate_frame(self,playground:Filed):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if self.stop and event.type == KEYDOWN and event.key==K_c:
                print('continue')
                self.stop=False
            elif event.type == KEYDOWN and event.key==K_c:
                print('stop')
                self.stop=True
            
            # print brain of clicked cell
            if event.type == MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()

                # click in grid
                if mpos[0]<GRID_SIZE[0]*ENLARGE_RATE:
                    # mouse grid position 
                    mpos = [int(mpos[0]/ENLARGE_RATE)+1,int(mpos[1]/ENLARGE_RATE)+1]
                    
                    for obj in playground.cells:
                        (x,y)=obj.get_grid_position()
                        if x==mpos[0] and y==mpos[1]:
                            # print(x,y)
                            print(obj.gene)

                elif mpos[1]>100 and mpos[1]<300:
                # click in rank bar
                    h = 80
                    rank = 0
                    for i in range(11):
                        h += 20
                        if mpos[1]<h:
                            rank=i
                            break             
                    playground.mark_cells(rank)


    
    def start_animation(self):
        screen = self.screen
        
        screen.fill((255, 255, 255))

        while True:
            start_time = time.time()

            # auto restart
            if AUTO_RESTART and self.liv_cell_num==0:
                self.era+=1
                self.era_step=0
                self.playground = Filed([motor_Cell() for i in range(INDIVIDUAL_NUM)],
                                    [food() for i in range(GEN_FOOD_RATE)])

            if not self.stop:
                self.update_frame(self.playground)

            self.manuplate_frame(self.playground)

            if self.steps%STEP_UPDATE_RATE==0:
                self.draw_frame(screen,self.playground)

            
            # input()
            # time.sleep(1)
            pygame.display.update()

            end_time = time.time()
            #print(end_time-start_time)

game().start_animation()