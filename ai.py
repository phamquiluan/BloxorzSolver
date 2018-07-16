# -*- coding: utf-8 -*- 
# AI Assignment 1 - Server playing game Bloxorz
# Author: Thanh Hung & Luan Pham & Hoang Gas

# Some clarify
# 0: None
# 1: Normal
# 2: Đo đỏ
# 3: Chữ X  (T C O)
# 4: Cục tròn đặc (only đóng).
# 5: Cục tròn đặc (T C O)
# 6: Cục tròn đặc (only mở)
# 7: Cục phân thân
# 8: Chữ X  (only mở)
# 9: Lỗ chiến thắng

import copy
import sys
import queue as Q

def readMap(fileMap):
    with open(fileMap) as f:
        MAP_ROW, MAP_COL, xStart, yStart = [int(x) for x in next(f).split()] # read first line
        sourceMap = []
        countMapLine = 1
        for line in f: # read map
            countMapLine += 1
            sourceMap.append([int(x) for x in line.split()])
            if countMapLine > MAP_ROW: break

        # read managedBoard
        manaBoa = []
        for line in f: # read manaBoa
            # 2 2 4 4 4 5
            manaBoa.append([int(x) for x in line.split()])

    print("\nYOUR MAP LOOK LIKE THIS:")
    for item in sourceMap:
        print(item)
    print("Start at (",xStart, ",", yStart,")")
    print("ManaBoa:")
    for item in manaBoa:
        print(item)
    print("======================================")
    return MAP_ROW, MAP_COL, xStart, yStart, sourceMap, manaBoa


class Block:

    def __init__(self, x, y, rot, parent, board, x1=None,y1=None):
        self.x      = x
        self.y      = y
        self.rot    = rot  
        self.parent = parent
        self.board  = copy.deepcopy(board)
        self.x1     = x1
        self.y1     = y1
    
    def __lt__(self, block):
        return True
    def __gt__(self, block):
        return True

    def move_up(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board)

        if self.rot == "STANDING":
            newBlock.y -= 2 
            newBlock.rot = "LAYING_Y"

        elif newBlock.rot == "LAYING_X":
            newBlock.y -= 1
        
        elif newBlock.rot == "LAYING_Y":
            newBlock.y -= 1
            newBlock.rot = "STANDING"
        
        return newBlock 

    def move_down(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board)

        if newBlock.rot == "STANDING":
            newBlock.y += 1
            newBlock.rot = "LAYING_Y"

        elif newBlock.rot == "LAYING_X":
            newBlock.y += 1

        elif newBlock.rot == "LAYING_Y":
            newBlock.y += 2
            newBlock.rot = "STANDING"
        return newBlock 

    def move_right(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board)
    
        if newBlock.rot == "STANDING":
            newBlock.x += 1
            newBlock.rot = "LAYING_X"

        elif newBlock.rot == "LAYING_X":
            newBlock.x += 2
            newBlock.rot = "STANDING"

        elif newBlock.rot == "LAYING_Y":
             newBlock.x += 1
        return newBlock

    def move_left(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board)

        if newBlock.rot == "STANDING":
            newBlock.rot = "LAYING_X"
            newBlock.x -= 2

        elif newBlock.rot == "LAYING_X":
            newBlock.x -= 1
            newBlock.rot = "STANDING"

        elif newBlock.rot == "LAYING_Y":
            newBlock.x -= 1

        return newBlock 

    # FOR CASE SPLIT
    def split_move_up(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.y -= 1
        return newBlock 

    def split_move_down(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.y += 1
        return newBlock 


    def split_move_left(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.x -= 1
        return newBlock 


    def split_move_right(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.x += 1
        return newBlock 

    def split1_move_up(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.y1 -= 1
        return newBlock 

    def split1_move_down(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.y1 += 1
        return newBlock 

    def split1_move_left(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.x1 -= 1
        return newBlock 

    def split1_move_right(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.x1, self.y1)
        newBlock.x1 += 1
        return newBlock 

    def disPlayPosition(self):
        if self.rot != "SPLIT":
            print(self.rot, self.x, self.y)
        else:
            print(self.rot, self.x, self.y, self.x1, self.y1)
    
    def disPlayBoard(self):
        
        # local definition
        x   = self.x
        y   = self.y
        x1  = self.x1
        y1  = self.y1
        rot = self.rot
        board = self.board

        # let's go

        if rot != "SPLIT":
            
            for i in range(len(board)): # for ROW
                print("",end='  ')
                for j in range(len(board[i])): # for COL in a ROW

                    if (i==y and j==x and rot=="STANDING") or \
                            ((i==y and j==x) or (i==y and j==x+1) and rot=="LAYING_X") or \
                            ((i==y and j==x) or (i==y+1 and j==x) and rot=="LAYING_Y"):

                        print("x",end=' ')

                    elif(board[i][j]==0):
                        print(" ",end=' ')
                    else:
                        print(board[i][j], end=' ')
                print("")
        else: # CASE SPLIT
            for i in range(len(board)): # for ROW
                print("",end='  ')
                for j in range(len(board[i])): # for COL

                    if (i==y and j==x) or (i==y1 and j==x1):
                        print("x",end=' ')

                    elif(board[i][j]==0):
                        print(" ",end=' ')
                    else:
                        print(board[i][j], end=' ')
                print("")
            
    
# Case 3: Chữ X
def isNumberThree(block,x,y):
    board = block.board

    for item in ManaBoa:

        if (x,y) ==  (item[0], item[1]):

            # TOGGLEEEE

            numToggle = item[2]   # num toggle
            index = 2   # index to check more element

            for i in range(numToggle):    # traverse toggle array
                bX = item[2*i+3]
                bY = item[2*i+4]
                if board[bX][bY] == 0:
                    board[bX][bY] = 1
                else:
                    board[bX][bY] = 0
        
            index = index + 1 + 2 * numToggle

            # CLOSEEEE

            # check if "item" has more element
            if index < len(item):   # case has more

                # read num close
                numClose = item[index]

                # traverse list close if num > 0
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # OPEENNNN

            # check if "item" has more element
            if index < len(item):   # case also has more item
                # get num open
                numOpen = item[index]

                # traverse list open if num > 0
                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1



# Case 4: Cục tròn đặc (only đóng).
def isNumberFour(block,x,y):
    board = block.board
    
    #print("(x-y) = (", x,"-", y,")")

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 0

# Case 5: Cục tròn đặc (toggle)
def isNumberFive(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):


            numToggle = item[2]     # numtoggle
            index = 2   # index to check more element

            for i in range(numToggle):
                bX = item[2*i+3]
                bY = item[2*i+4]
                if board[bX][bY] == 0:
                    board[bX][bY] = 1
                else:
                    board[bX][bY] = 0
            
            index = index + 1 + 2 * numToggle

            # CLOSEEEE

            # check if "item" has more element
            if index < len(item):   # case has more

                # read num close
                numClose = item[index]
                    
                # traverse list close if num > 0
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # OPEENNNN

            # check if "item" has more element
            if index < len(item):   # case also has more item
                # get num open
                numOpen = item[index]

                # traverse list open if num > 0
                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1


# Case 6: Cục tròn đặc (only mở)
def isNumberSix(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1

# Case 7: Cục phân thân
def isNumberSeven(block,x,y):  
    board = block.board
    array = []    
    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            # format x7 y7 2 x y x1 y1
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                array.append([bX,bY])

    (block.y,block.x,block.y1,block.x1) = \
            (array[0][0],array[0][1],array[1][0], array[1][1])

    block.rot = "SPLIT"

# Case 8: Chữ X (only mở)
def isNumberEight(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):

            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1




# isValidBLock
def isValidBlock(block):
    
    if isFloor(block):
        
        # local definition
        x     = block.x
        y     = block.y
        x1    = block.x1
        y1    = block.y1
        rot   = block.rot
        board = block.board
        
        
        # Case 2: Đo đỏ
        if rot == "STANDING" and board[y][x] == 2:
            return False 

        # Case 3: Chữ X
        if rot == "STANDING" and board[y][x] == 3:
            isNumberThree(block,x,y)
        
        # Case 4: Cục tròn đặc (only đóng).
        if board[y][x] == 4:
            isNumberFour(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 4:
            isNumberFour(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 4:
            isNumberFour(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 4:
            isNumberFour(block,x1,y1)


        # Case 5: Cục tròn đặc (toggle)
        if board[y][x] == 5:
            isNumberFive(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 5:
            isNumberFive(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 5:
            isNumberFive(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 5:
            isNumberFive(block,x1,y1)

        # Case 6: Cục tròn đặc (only mở)
        if board[y][x] == 6:
            isNumberSix(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 6:
            isNumberSix(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 6:
            isNumberSix(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 6:
            isNumberSix(block,x1,y1)

        # Case 7: Phân thân 
        if rot == "STANDING" and board[y][x] == 7:
            isNumberSeven(block,x,y)
        # Case7_1: MERGE BLOCK
        if rot == "SPLIT": # check IS_MERGE
            # case LAYING_X: x first
            if y == y1 and x == x1 -1:
                block.rot = "LAYING_X"

            # case LAYING_X: x1 first
            if y == y1 and x == x1 + 1:
                block.rot = "LAYING_X"
                block.x   = x1

            # case LAYING_Y: y first
            if x == x1 and y == y1 - 1:
                block.rot = "LAYING_Y"
            
            # case LAYING_Y: y1 first
            if x == x1 and y == y1 + 1:
                block.rot = "LAYING_Y"
                block.y   = y1

        # Case 8: Chữ X (only mở)
        if rot == "STANDING" and board[y][x] == 8:
            isNumberEight(block,x,y)
            
        return True
    else:
        return False


def isFloor(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board
    
    if x >= 0 and y >= 0 and \
            y < MAP_ROW and x < MAP_COL and \
            board[y][x] != 0:

        if rot == "STANDING":
            return True
        elif rot == "LAYING_Y":
            if y+1 < MAP_ROW and board[y+1][x] != 0 :
                return True
        elif rot == "LAYING_X":
            if x+1 < MAP_COL and board[y][x+1] != 0 :
                return True
        else: # case SPLIT
            x1 = block.x1
            y1 = block.y1

            if x1 >= 0 and y1 >= 0 and \
                y1 < MAP_ROW and x1 < MAP_COL and \
                board[y1][x1] != 0:
                    return True

    else:
        return False


def isGoal(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board

    if rot == "STANDING" and  \
        board[y][x] == 9:
        return True
    else:
        return False


def isVisited(block):
    if block.rot != "SPLIT":

        for item in passState:
            if item.x == block.x     and item.y == block.y and \
                item.rot == block.rot and item.board == block.board:
                return True

    else: # case SPLIT
        for item in passState:
            if item.x  == block.x     and item.y  == block.y and \
               item.x1 == block.x1    and item.y1 == block.y1 and \
                item.rot == block.rot and item.board == block.board:
                return True

    return False

def move(Stack, block, flag):

    if isValidBlock(block):
        if isVisited(block):
            return None

        Stack.append(block)
        passState.append(block)
        #print(flag)
        return True 

    return False   

def printSuccessRoad(block):
    
    print("\nTHIS IS SUCCESS ROAD")
    print("================================")
    
    successRoad = [block]
    temp = block.parent
    
    while temp != None:
        
        if temp.rot != "SPLIT":
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board)
        else: # case SPLIT
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.x1, temp.y1)

        successRoad = [newBlock] + successRoad
        
        temp = temp.parent
    
    step = 0
    for item in successRoad:
        step += 1
        print("\nStep:", step, end=' >>>   ')
        item.disPlayPosition()
        print("=============================")
        item.disPlayBoard()

    print("COMSUME",step,"STEP!!!!")
    
# solve DFS
def DFS(block):

    board = block.board
    Stack = []
    Stack.append(block)
    passState.append(block)
    
    virtualStep = 0

    while Stack:
        current = Stack.pop()
        #current.disPlayPosition()
        #current.disPlayBoard()

        if isGoal(current):
            printSuccessRoad(current)
            print("COMSUME", virtualStep, "VIRTUAL STEP")
            print("SUCCESS")
            return True
        else:
            if current.rot != "SPLIT":
                virtualStep += 4

                move(Stack,current.move_up(), "up")
                move(Stack,current.move_right(), "right")
                move(Stack,current.move_down(), "down")
                move(Stack,current.move_left(), "left")
            else: 
                virtualStep += 8

                move(Stack,current.split_move_left(), "left0")
                move(Stack,current.split_move_right(), "right0")
                move(Stack,current.split_move_up(), "up0")
                move(Stack,current.split_move_down(), "down0")
                
                move(Stack,current.split1_move_left(), "left1")
                move(Stack,current.split1_move_right(), "right1")
                move(Stack,current.split1_move_up(), "up1")
                move(Stack,current.split1_move_down(), "down1")
    return False

# solve BFS
def BFS(block):

    board = block.board
    Queue = []
    Queue.append(block)
    passState.append(block)

    virtualStep = 0

    while Queue:
        current = Queue.pop(0)
        #current.disPlayPosition()
        #current.disPlayBoard()

        if isGoal(current):
            printSuccessRoad(current)
            print("SUCCESS")
            print("COMSUME", virtualStep, "VIRTUAL STEP")
            return True

        if current.rot != "SPLIT":
            virtualStep += 4

            move(Queue,current.move_up(), "up")
            move(Queue,current.move_right(), "right")
            move(Queue,current.move_down(), "down")
            move(Queue,current.move_left(), "left")
        else: 
            virtualStep += 8

            move(Queue,current.split_move_left(), "left0")
            move(Queue,current.split_move_right(), "right0")
            move(Queue,current.split_move_up(), "up0")
            move(Queue,current.split_move_down(), "down0")
            
            move(Queue,current.split1_move_left(), "left1")
            move(Queue,current.split1_move_right(), "right1")
            move(Queue,current.split1_move_up(), "up1")
            move(Queue,current.split1_move_down(), "down1")
    return False


def evalFunction(block):

    #  local definition
    x   = block.x
    y   = block.y
    x1  = block.x1
    y1  = block.y1
    rot = block.rot
    board = block.board

    # get goal
    (xGoal, yGoal) = (0, 0)
    for yG in range(len(board)):
        for xG in range(len(board[0])):
            if board[y][x] == '9':
                (xGoal, yGoal) = (xG, yG)

    # calc distance pos-goal
    distance = 0

    if rot == "SPLIT":

        distance1 = (x-xGoal)*(x-xGoal)+(y-yGoal)*(y-yGoal)
        distance2 = (x1-xGoal)*(x1-xGoal)+(y1-yGoal)*(y1-yGoal)
        distance = (distance1+distance2)/2

    else:
        # (x1 - x2)^2 + (y1 - y2) ^ 2
        distance = (x-xGoal)*(x-xGoal)+(y-yGoal)*(y-yGoal)

    return int(distance)

def moveBest(BestQueue, block, flag):
    
    if isValidBlock(block):
        if isVisited(block):            
            return False
        
        EvalCur = evalFunction(block)
        BestQueue.put((EvalCur, block))
        passState.append(block)

        return True
    return False
            

def BEST(block):
    
    # create priority queue
    BestQueue = Q.PriorityQueue()

    startEval = evalFunction(block)

    # insert start node
    BestQueue.put((startEval, block))
    passState.append(block)
    
    virtualStep = 0

    # until priority queue is empty
    while BestQueue.not_empty:

        item   = BestQueue.get()  # item = (block, distance)
        iDista = item[0]
        iBlock = item[1]

        # if goal
        if isGoal(iBlock):

            printSuccessRoad(iBlock)
            print("SUCCESS")
            print("COMSUME", virtualStep, "VIRTUAL STEP")

            return True

        # put all new operator to queue
        if iBlock.rot != "SPLIT":
            
            virtualStep += 4

            # try up
            moveBest(BestQueue, iBlock.move_up(), "up") 
            moveBest(BestQueue, iBlock.move_down(), "down") 
            moveBest(BestQueue, iBlock.move_right(), "right") 
            moveBest(BestQueue, iBlock.move_left(), "left") 
        else: 
           
            virtualStep += 8

            moveBest(BestQueue, iBlock.split_move_left(), "left0")
            moveBest(BestQueue, iBlock.split_move_right(), "right0")
            moveBest(BestQueue, iBlock.split_move_up(), "up0")
            moveBest(BestQueue, iBlock.split_move_down(), "down0")
            
            moveBest(BestQueue, iBlock.split1_move_left(), "left1")
            moveBest(BestQueue, iBlock.split1_move_right(), "right1")
            moveBest(BestQueue, iBlock.split1_move_up(), "up1")
            moveBest(BestQueue, iBlock.split1_move_down(), "down1")




# START PROGRAM HERE
passState = []

MAP_ROW, MAP_COL, xStart, yStart, sourceMap, ManaBoa \
                        = readMap('map/map'+sys.argv[1:][0]+'.txt')

block = Block(xStart, yStart, "STANDING", None, sourceMap)

if sys.argv[1:][1] == "DFS":
    print("Solve DFS")  
    DFS(block)

elif sys.argv[1:][1] == "BFS":
    print("Solve BFS")
    BFS(block)

elif sys.argv[1:][1] == "BEST":
    print("Solve Best")
    BEST(block)

else:
    print("Wrong algorithms argument!")

