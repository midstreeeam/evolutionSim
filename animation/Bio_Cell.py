from pygame.locals import *
from sys import exit
import time
import random
from math import pi
from animation_config import *
import Node

class ini_Cell():
    def __init__(self):
        self.max_neural_num = MAX_NEURAL_NUM
        self.death=False
        pass

    def __get_gene_pair(self):
        table1 = SENSORS+NEURALS
        randid1=random.randint(0,len(table1)-1)
        table2 = NEURALS+ACTIVATORS
        randid2=random.randint(0,len(table2)-1)
        return [table1[randid1],table2[randid2]]

    def __generate_gene_piece(self):
        # generate gene structure with only two letters represent the direction
        # e.g. (a,C) means from a to C.
        # doesn't allow loops here
        # doesn't allow too much inner neural
        isloop=True
        
        while(isloop):
            isloop=False
            [n1,n2]=self.__get_gene_pair()
            if n1 in UPPER and n2 in UPPER and n1==n2:
                isloop=True

        return [n1,n2]
    
    def __cut_inner_neural(self,gene_pieces):
        num_exceed=False
        an=0
        bn=0
        cn=0
        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            if pair[1]=="A":
                an+=1
            if pair[1]=="B":
                bn+=1
            if pair[1]=="C":
                cn+=1
        if max(an,bn,cn)>MAX_NEURAL_NUM:
            num_exceed=True

        while(num_exceed):
            num_exceed=False
            an=0
            bn=0
            cn=0
            for i in range(len(gene_pieces)):
                pair = gene_pieces[i]
                if pair[1]=="A":
                    an+=1
                    if an>2:
                        [pair[0],pair[1]]=self.__get_gene_pair()
                if pair[1]=="B":
                    bn+=1
                    if bn>2:
                        [pair[0],pair[1]]=self.__get_gene_pair()
                if pair[1]=="C":
                    cn+=1
                    if cn>2:
                        [pair[0],pair[1]]=self.__get_gene_pair()
            if max(an,bn,cn)>MAX_NEURAL_NUM:
                num_exceed=True
        
        return gene_pieces
            
    
    def __get_weight(self,gene_pieces):
        # take gene-pair list as input
        # get random weight
        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            rd=random.random()
            weight=str(random.randint(1,99)).zfill(2)
            if rd>0.5:
                pair.append('+'+weight)
            else:
                pair.append('-'+weight)
        
        return gene_pieces

    
    def __get_id(self,gene_pieces):
        # take gene-pair list as input

        # sensors and activators
        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            if pair[0] in LOWER:
                pair[0] = pair[0]+'00'
            if pair[1] in LOWER:
                pair[1] = pair[1]+'00'
        
        # inner neurals
        # activator end
        # If an inner neural type has more than two activator connected,
        # each inner neural can only have up to two inputs.
        nums = [0,0,0] # represent the number of activators connect to A,B,C
        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            if pair[1]=='A':
                id_number=int(nums[0]/2)+1
                pair[1] = pair[1]+str(id_number).zfill(2)
                nums[0]+=1
                
            if pair[1]=='B':
                id_number=int(nums[1]/2)+1
                pair[1] = pair[1]+str(id_number).zfill(2)
                nums[1]+=1
                
            if pair[1]=='C':
                id_number=int(nums[2]/2)+1
                pair[1] = pair[1]+str(id_number).zfill(2)
                nums[2]+=1
                
        
        for i in range(len(nums)):
            if nums[i]!=0:
                nums[i]-=1

        # sensor end
        # random connect
        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            if pair[0]=='A':
                id_number=random.randint(1,int(nums[0]/2)+1)
                pair[0]=pair[0]+str(id_number).zfill(2)
            if pair[0]=='B':
                id_number=random.randint(1,int(nums[1]/2)+1)
                pair[0]=pair[0]+str(id_number).zfill(2)
            if pair[0]=='C':
                id_number=random.randint(1,int(nums[2]/2)+1)
                pair[0]=pair[0]+str(id_number).zfill(2)
            
        return gene_pieces



    def _delete_loop(self):
        # delete loops in genes
        pass
    
    def _rand_gene(self):
        # generate random gene with default length
        gene_pieces=[]
        for i in range(RAND_GENE_LENGTH):
            gene_pieces.append(self.__generate_gene_piece())
        
        gene_pieces = self.__cut_inner_neural(gene_pieces)
        
        # while self.__is_exceeded(gene_pieces):
        #     for i in range(RAND_GENE_LENGTH):
        #         gene_pieces.append(self.__generate_gene_piece())

        gene_pieces = self.__get_weight(self.__get_id(gene_pieces))

        for i in range(len(gene_pieces)):
            pair = gene_pieces[i]
            gene_pieces[i] = pair[0]+pair[1]+pair[2]
        
        return gene_pieces


    def _clean_gene(self):
        # delete hover neurals that exceed num in config file.
        pass

    def _shift_neurals(self):
        # if a neural have more than two inputs,
        # change the neural id for third connection.
        pass

# i=ini_Cell()
# for j in i._rand_gene():
#     print(j)


class bio_Cell(ini_Cell):
    def __init__(self,gene=None,rand_gene=True,rand_age=False):
        super().__init__()
        self.food_storage = 0
        self.cell_storage = 0

        # init age
        self.age = 0
        if RAND_AGE:
            self.age=random.randint(0,CELL_AGE-1)

        # init gene
        if rand_gene:
            self.gene = self._rand_gene()
        else:
            self.gene = gene
        # self.gene = ['a00c00+60','j00f00+40','h00a00+40','j00f00-40']
        # self.gene=['i00f00+20']
        self.matrix = self.__get_brain_matrix()

        self.brain:Node.Brain() = self.__construct_brain()
    
    
    def __letter_to_num(self,n_id,activator=False):
    # take an neural-id as input and return a number which is the index in matrix
        table1 = {'a':0,
                'b':1,
                'c':2,
                'd':3,
                'e':4,
                'f':5,
                'g':6,
                'h':7,
                'i':8,
                'j':9,
                'k':10,
                'l':11}

        table2 = {'A':NEURAL_TYPE_NUM,
                'B':NEURAL_TYPE_NUM+MAX_NEURAL_NUM,
                'C':NEURAL_TYPE_NUM+2*MAX_NEURAL_NUM}

        # sensor or activator
        if n_id[0] in LOWER:
            if activator:
                return table1[n_id[0]]+SENSOR_NUM
            return table1[n_id[0]]
        
        # inner neural
        return table2[n_id[0]]+int(n_id[1:3])-1

    
    def __update_matrix(self,matrix,gene):
    # take a sigle piece gene as input and update the brain_matrix
        input_num = self.__letter_to_num(gene[:3])
        output_num = self.__letter_to_num(gene[3:6],activator=True)
        try:
            matrix[input_num][output_num] = int(gene[6:])/100
        except:
            print(gene,input_num,output_num)
        matrix[input_num][output_num] = int(gene[6:])/100
        pass

    def __get_brain_matrix(self):
        matrix_length = NEURAL_TYPE_NUM + 3*MAX_NEURAL_NUM
        matrix = [[0 for i in range(matrix_length)] for i in range(matrix_length)]
        gene = self.gene

        for i in gene:
            self.__update_matrix(matrix,i)
        
        return matrix


    def __construct_brain(self):
    # decode gene to construct a brain

        matrix = self.__get_brain_matrix()
        brain = Node.Brain(matrix)
        # decode gene here


        return brain


# c = bio_Cell()
# print(c.brain.get_output([2,2,1,1,1,1,1,1,1,1]))