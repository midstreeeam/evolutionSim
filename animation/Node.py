import numpy as np
from pygame.locals import *
from sys import exit
import math
import copy
from math import pi
from animation_config import *
from numba.typed import List
from numba import njit

@njit
def neural_inputs(lst,signals):
    # return two inputs of the middle neural
    # 114514 means no input
    j=0
    num = np.array([114514,114514],dtype=np.float64)
    for i in range(len(lst)):
        if lst[i] != 0:
            temp=lst[i]*signals[i]
            num[j]=temp
            if signals[i]==0:
                num[j]=114514
            j+=1

    if num[0] != 114514:
        if num[1] == 114514:
            num=np.array([num[0],NEURAL_INPUT],dtype=np.float64)
    else:
        num=np.array([0,0],dtype=np.float64)
    return num

@njit
def normalize(num):
    # return num
    return math.tanh(num)

#@njit
def matrix_operation(temp_matrix,signals,input_list,shape0):
    # print(signals.tolist())
    # print('loop')
    for i in range(NEURAL_TYPE_NUM):
        dot_product = np.dot(temp_matrix[:,i],signals)
        input_list[i] = normalize(dot_product)
            
    # execute AND
    for i in range(NEURAL_TYPE_NUM,NEURAL_TYPE_NUM+MAX_NEURAL_NUM):
        inputs_weight = temp_matrix[:,i]
        nlst=neural_inputs(inputs_weight,signals)
        in1=nlst[0]
        in2=nlst[1]
        if in1>0 and in2>0:
            input_list[i] = normalize(in1+in2)
        else:
            input_list[i] = -normalize(abs(in1)+abs(in2))


    # execute OR
    for i in range(NEURAL_TYPE_NUM+MAX_NEURAL_NUM,NEURAL_TYPE_NUM+2*MAX_NEURAL_NUM):
        inputs_weight = temp_matrix[:,i]
        nlst= neural_inputs(inputs_weight,signals)
        in1=nlst[0]
        in2=nlst[1]
        if in1<0 and in2<0:
            input_list[i] = normalize(in1+in2)
        else:
            input_list[i] = normalize(abs(in1)+abs(in2))

    # execute XOR
    for i in range(NEURAL_TYPE_NUM+2*MAX_NEURAL_NUM,shape0):
        inputs_weight = temp_matrix[:,i]
        nlst= neural_inputs(inputs_weight,signals)
        in1=nlst[0]
        in2=nlst[1]
        if in1>0 and in2>0:
            input_list[i] = abs(normalize(in1+in2))
        elif in1<0 and in2<0:
            input_list[i] = abs(normalize(in1+in2))
        else:
            input_list[i] = -normalize(abs(in1)+abs(in2))   
    
    return temp_matrix,signals,input_list






class Node():
    def __init__(self,type):
        self.type=type
        self.next = []
        self.weights = []
        pass

    def link_to(self,next):
        next:list[Node]
        self.next = next
    
    def add_weight(self,weights:list):
        self.weights = weights

class Sensor(Node):
    def __init__(self, type='sensor'):
        super().__init__(type)
    pass

class Neural(Node):
    def __init__(self, type='neural'):
        super().__init__(type)
    pass

class Activator(Node):
    def __init__(self, type='activator'):
        super().__init__(type)
    pass



class Brain():
    def __init__(self,matrix):
        self.matrix = np.array(matrix)
        pass
    
    def set_sensors(self,sensors:list[Sensor]):
        self.sensors = sensors

    def __check_stop(self,input_list):
        # return False when need to stop
        for i in input_list:
            if i!=0:
                return True
        return False
    
    def __get_decision(self,weights):
        id=0
        maxw=-MAX_NUM
        for i in range(len(weights)):
            if weights[i]>maxw:
                maxw=weights[i]
                id=i
        table = [MF,MN,MS,ME,MW,MB,TR,TL]

        if maxw<=TRIGGER_NUM:
            return ST

        return table[id]
    
    def __get_output_from_matrix(self,input_signals:list):

        # t = self.matrix.tolist()
        # for i in t:
        #     print(i)

        temp_matrix = copy.deepcopy(self.matrix)
        signals = np.zeros(self.matrix.shape[0])
        for i in range(len(input_signals)):
            signals[i] = input_signals[i]
        input_list = np.zeros(self.matrix.shape[0])
        weights = [0 for i in range(ACTIVATOR_NUM)]

        stop=True
        while(stop):
            temp_matrix,signals,input_list=matrix_operation(temp_matrix,signals,input_list,self.matrix.shape[0])

            weights[0]+=input_list[SENSOR_NUM]
            weights[1]+=input_list[SENSOR_NUM+1]
            weights[2]+=input_list[SENSOR_NUM+2]
            weights[3]+=input_list[SENSOR_NUM+3]
            weights[4]+=input_list[SENSOR_NUM+4]
            weights[5]+=input_list[SENSOR_NUM+5]
            weights[6]+=input_list[SENSOR_NUM+6]
            weights[7]+=input_list[SENSOR_NUM+7]

            signals = copy.deepcopy(input_list)
            stop=self.__check_stop(signals)


        # print(weights)

        return self.__get_decision(weights)

    
    def get_output(self,input_signals:list):
    # input all the signals, but only those with matched sensor can be used
    # take input signal for every sensor, return the activation function id
    # every cell can only take one activation function each frame
    # only the activation with the highest weight is the final decision
        return self.__get_output_from_matrix(input_signals)



# n = [Activator() for i in range(3)]
# head = Sensor()
# head.link_to(n)
# print(head.next)
# print(str(type(head)))