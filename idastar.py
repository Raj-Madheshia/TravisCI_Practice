"""
The Heuristic function is defined as given below
    Distance between goal and goal car  +
        number of car in between goal and goal car  +
            Number of car which is obstacle for movement of car present between
            goal and goalcar
"""
import numpy as np
from collections import Counter
listOfCar = []
needExpansion = True
pathNodes =[]
new_fscore=[]

def Heuristic(node):
    """Will return heuristic value of the present matrix"""
    n = np.array(node)
    a = np.where(n==9)
    blockingCar=[]
    x= a[0][0]
    y2=a[1][1]
    dummy = y2+1
    while (dummy < n.shape[-1]):
        if n[x][dummy]!=0:
            blockingCar.append(n[x][dummy])
        dummy+=1
    count=0
    for i in blockingCar:
        a = np.where(n==i)
        y = a[1][0]
        x1 = a[0][0]
        x2 = a[0][1]
        if x1 ==0:
            count+=1
        if x2 == n.shape[0]-1:
            count+=1
        if x1>0:
            d  = n[x1-1][y]
            if d !=0:
                count +=1
                #print("1")
        if x2 < n.shape[0]-1:
            d = n[x2+1][y]
            if d!=0:
                count+=1
                #print("2")
    total = (n.shape[1]-1-y2) + len(blockingCar) +count
    return total
    
def main(node):
    """The program will start from here"""
    global listOfCar
    global pathNodes
    global new_fscore
    g=0 # for depth of root node is zero
    new_node = np.array(node)
    reshape = new_node.reshape(-1)
    listOfCar.extend(Counter(reshape).keys())
    heuristic = Heuristic(new_node)
    f_score = g+heuristic
    node = np.array(node).tolist()
    while(needExpansion):
        pathNodes=[]
        rushhour(list(node),0,f_score)
        if needExpansion == True:
            f_score = min(new_fscore)
            new_fscore =[]
    

def checkForMatrix(parent, x,y):
        if parent[x][y] != 0:
            return False
        else:
            return True

def pathClear(parent, x, y):
    chk = 0
    for i in parent[x][y+1:]:
        if i!=0:
            chk =1
        #print("i from check",i)
    if chk ==0:
        return True
    else:
        return False

def rushhour(node,level,f_score):
    
    global needExpansion
    if needExpansion == False:
        return
    h = Heuristic(node)
    if (f_score < (level+h)):
        new_fscore.append(level+h)
        return
    pathNodes.append(node)
    
    current = np.array(node)
    for i in listOfCar:
        if i ==0:
            continue
        pos = np.where(current ==i)
        if i ==9:
            x =pos[0][0]
            y1 = pos[1][0]
            y2=pos[1][1]
            
            if pathClear(current,x,y2):
                parent = np.array(current)
                shp = parent.shape
                parent[x][y2]=0
                parent[x][y1]=0
                parent[x][shp[-1]-1]=9
                parent[x][shp[-1]-2]=9
                new_node = np.array(parent).tolist()
                pathNodes.append(new_node)
                needExpansion = False
                print("Path to Goal is: ")
                printTraverse(pathNodes)
                return
        
        if pos[0][0] == pos[0][1]:
            x=pos[0][0]
            y1=pos[1][0]
            y2=pos[1][1]
            
            new_node = np.array(current.copy())
            if y1>0:
                isPossible = checkForMatrix(current, x, y1-1)
                if isPossible:
                    
                    new_node[x][y1-1]=i
                    new_node[x][y2]=0
                    new_node = np.array(new_node).tolist()
                    rushhour(new_node, level+1, f_score)
            new_node = np.array(current.copy())
            if y2<(new_node.shape[-1]-1):
                isPossible = checkForMatrix(new_node, x, y2+1)
                if isPossible:
                    new_node[x][y2+1]=i
                    new_node[x][y1]=0
                    new_node = np.array(new_node).tolist()
                    rushhour(new_node, level+1, f_score)
                    
        elif pos[1][0] == pos[1][1]:
            y = pos[1][0]
            x1 = pos[0][0]
            x2 = pos[0][1]
            new_node = np.array(current.copy())
            if x1 > 0:
                isPossible = checkForMatrix(new_node, x1-1, y)
                if isPossible:
                    new_node[x1-1][y]=i
                    new_node[x2][y]=0
                    new_node = np.array(new_node).tolist()
                    rushhour(new_node, level+1, f_score)

            new_node = np.array(current.copy())
            if x2<(new_node.shape[0]-1):
                isPossible = checkForMatrix(new_node, x2+1, y)
                if isPossible:
                    new_node[x2+1][y]=i
                    new_node[x1][y]=0
                    new_node = np.array(new_node).tolist()
                    rushhour(new_node, level+1, f_score)
    pathNodes.pop()


def printTraverse(value):
    start = 0
    end = np.array(value).shape[-1]-1
    if end >=len(value):
        new = value[start:len(value)]
        for i in list(zip(*new)):
            print(i)
        print("\n")
    while(end<len(value)):
        new = value[start:end]
        for i in list(zip(*new)):
            print(i)
        print("\n")
        start = end
        end +=5
        if end >=len(value):
            end = len(value)
            new = value[start:len(value)]
            for i in list(zip(*new)):
                print(i)
            print("\n")                      

start = [[0,0,0,3,5],
         [9,9,2,3,5],
         [0,0,2,4,4],
         [0,1,1,0,0]]

main(start)