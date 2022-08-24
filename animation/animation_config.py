# mode config (default: life mode)
REFRESH_MODE = True

FRAME_RATE = 30
GRID_SIZE = (64,64)
ENLARGE_RATE = 10
INDIVIDUAL_NUM = 300
SIDEBAR_WIDTH = 800
FRAME_SIZE = (GRID_SIZE[0]*ENLARGE_RATE+SIDEBAR_WIDTH,GRID_SIZE[1]*ENLARGE_RATE)
SHOWN_GENE_LENGTH = 70
STEP_UPDATE_RATE = 1 # update screen every 1 frames

AUTO_RESTART=True
ERA_LENGTH = 32 # only avaliable in refresh mode

# math config
MAX_NUM = 65536

# grid element lable
ELE_WALL = -1
ELE_EMPTY = 0
ELE_CELL = 0.5
ELE_FOOD = 1
ELE_PRED = -0.5

GEN_FOOD_RATE = 21 # generate 15 foods each frame
GEN_CELL_RATE = 15  # generate a cell every 20 frames
GEN_CELL_RATE = MAX_NUM # not generate new cell

# death area config
# LEFTTOP = [(15,0),(0,15)] # unit is grid, not pixle
# RIGHTBOTTOM = [(49,64),(64,49)]
# LEFTTOP = [(0,0),(54,0),(10,0),(0,54)]
# RIGHTBOTTOM = [(10,64),(64,64),(64,10),(64,64)]
LEFTTOP = [(15,0)]
RIGHTBOTTOM = [(49,64)]
# LEFTTOP = [(0,0)]
# RIGHTBOTTOM = [(0,0)]


# bio config
RAND_AGE = True
CELL_AGE = 400
#MAX_AGE = MAX_NUM
PREDATOR_AGE = 600
REPRODUCE_THRESHOULD = 14 # food needed to reproduce
#REPRODUCE_THRESHOULD = MAX_NUM
PREDATOR_REPRODUCE_THRESHOULD = 2 # cell needed to repreduce
FOOD_MAX_AGE = 300
RAND_GENE_LENGTH = 36
MAX_NEURAL_NUM = 8
ALLOWED_HOVER_NEURAL_RATE = 0.25
ALLOWED_HOVER_NERUAL_NUM = int(MAX_NEURAL_NUM*ALLOWED_HOVER_NEURAL_RATE)

PRED_COLOR = (0,0,0)


# mutation config
WEIGHT_MU_RATE = 0.3 # mutation rate for each individual
PIECE_WEIGHT_MU_RATE = 0.2 # weight mutation rate for each gene in mutating individual
WEIGHT_MU_RADIUS = 25

LINK_MU_RATE = 0.3
PIECE_LINK_MU_RATE = 0.15 # link mutation rate for each gene in mutating individual

MU_PREDATOR_RATE = 0.02 # cell mutate to predator or predator mutate to cell



# Neural Types
# geno example: a00a00+53: from RD to MF with weight 53
# geno example: B01d00-08: from OR(id=01) to ME with weight -8


# input (sensor)
RD = 'a' # random input
OS = 'b' # oscillator
AGE = 'c' # age
EWL = 'd' # east/west location
NSL = 'e' # north/south location
FDEW = 'f' # facing direction east/west
FDNS = 'g' # facing direction north/south
RD2 = 'h' # random input 2
CST = 'i' # contant 1
NPFW = 'j' # next pixcel type
SEFW = 'k' # see type
SED = 'l' # see distance
NPCP = 'm' # next pixcel cell/predator
SECP = 'n' # see cell/predator


SENSORS=[RD,OS,AGE,EWL,NSL,FDEW,FDNS,RD2,CST,NPFW,SEFW,SED]
SENSOR_NUM=len(SENSORS)

# middle (inner neural)
AND = 'A'
OR = 'B'
XOR = 'C'
# EMP = 'D' # empty (ban)
FIL = 'E' # only value in certern range can pass

NEURALS=[AND,OR,XOR]
NUERAL_NUM=len(NEURALS)

NEURAL_INPUT = 0.5 # default neural input


# output (actuator)
MF = 'a' # move forward
MN = 'b' # move north
MS = 'c' # move south
ME = 'd' # move east
MW = 'e' # move west
MB = 'f' # move backward
TR = 'g' # trun right
TL = 'h' # turn left

ACTIVATORS=[MF,MN,MS,ME,MW,MB,TR,TL]
ACTIVATOR_NUM=len(ACTIVATORS)

NEURAL_TYPE_NUM = SENSOR_NUM+NUERAL_NUM+ACTIVATOR_NUM

# special output
ST = 'z' # don't do anything

# trigger num
TRIGGER_NUM = 0.15 # if the final weight of an activator less than tigger num, it won't execute




# other
UPPER = ['A','B','C','D']
LOWER = ['a','b','c','d','e','f','g','h','i','j','k','l']





if REFRESH_MODE:
    SIDEBAR_WIDTH = 700
    SHOWN_GENE_LENGTH = 60
    FRAME_SIZE = (GRID_SIZE[0]*ENLARGE_RATE+SIDEBAR_WIDTH,GRID_SIZE[1]*ENLARGE_RATE)
    RAND_AGE=False
    CELL_AGE=MAX_NUM
    GEN_CELL_RATE = MAX_NUM
    GEN_FOOD_RATE = 0