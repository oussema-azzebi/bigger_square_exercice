import re
import sys

def checkPlanFile(filePath):
    
    try:
        file = open(filePath, 'r')
        plan = file.read()
    except:
        print('Map Error', end='')
        exit()

	# check topline
    topLine = plan.split('\n')[0]
    if len(topLine) < 4:
        print('Map Error', end='')
        exit()
    
    #get all elements from the top line
    try:        
        nLine = int(re.search(r'\d+', topLine).group())
        if 0 == nLine:
            print('Map Error', end='')
            exit()
    except AttributeError:
        print('Map Error', end='')
        exit()
                
    emptyElement = topLine[-3]
    obstacleElement = topLine[-2]
    squareX = topLine[-1]
    
    #check line numbers / lenght in the map
    Counter = 0
    CoList = plan.split("\n")  
    for i in CoList: 
        if i: 
            Counter += 1
    
    if Counter - 1 != nLine:
        print('Map Error', end='')
        exit()
    
    CoList = CoList[1:]
    for line in CoList:
        if line == CoList[-1]:
            break
        if len(line) != len(CoList[0]):
            print('Map Error', end='')
            exit()
        for character in line:
            if character != emptyElement and character != obstacleElement and character != squareX:
                print('Map Error', end='')
                exit()
    
    # get the number of columns of our map
    nCol = len(CoList[0])
    
    # get the plan without first line and without the back to the line
    plan = "".join(CoList)
    
    #fill obstacle list
    obstacleList = []            
    for n, character in enumerate(plan, 0):             
        if obstacleElement == character:
            obstacleList.append(n)
            
    return plan, nCol, obstacleList, squareX
            

       
def find_bigger_square(filePath):
    
    #first we check the map if it is correct or not and we return the parameters we need
    plan, nCol, obstacleList, squareX = checkPlanFile(filePath)
        
    #init
    leftTopCorner = 0
    rightTopCorner = 0
    leftBottomCorner = 0
    rightBottomCorner = 0
    
    counter = 0
    i = 0
    
    #dictionary containing information on our bigger square (begin point and size)
    bigger_square = {'begin_square': 0, 'size_square': 0}   
    
    #The approach is to enlarge the square by 1*1 until you come across an obstacle   
    #When we find an obstacle, we recreate another square of 1*1 and we enlarge it again    
    #We do the same operation on the whole map.
    
    #The variable "bigger_square" will contain the biggest square when found
       
    #At the end we browse the map and insert the "square" elements in the right places
    
    while i < len(plan):
        
        if (leftTopCorner + counter) % nCol == 0:
            leftTopCorner += counter
            counter = 0
        
        #compute rightTopCorner, leftTopCorner, leftBottomCorner and rightBottomCorner
        rightTopCorner = leftTopCorner + counter
        leftBottomCorner = leftTopCorner + nCol * counter
        
        if leftBottomCorner > len(plan):
            break
        rightBottomCorner = leftBottomCorner + counter
        
        topPoints = []
        downPoints = []
        obstaclePoints = []        
        
        #fill topPoints list
        for point in range(rightTopCorner, rightBottomCorner + 1, nCol):
            if point in obstacleList:
                topPoints.append(point)
        
        #fill downpoints list        
        for point in range(leftBottomCorner, rightBottomCorner + 1):
            if point in obstacleList:
                downPoints.append(point)
                
        # get the list of the obstacles ponits
        obstaclePoints = topPoints + downPoints
        
        # check if an obstacle is present in the list of obstacles
        if len(obstaclePoints) == 0:
            counter += 1
            if counter > bigger_square['size_square']:
                bigger_square = {'begin_square': leftTopCorner, 'size_square': counter}
        
        else:
            leftTopCorner = (leftTopCorner // nCol) * nCol + (obstaclePoints[0] % nCol + 1)
            counter = 0
            
        i += 1
                
    # print our big square
    output = ''
    pos = []
        
    for i in range(0, bigger_square['size_square']):
        for x in range(bigger_square['begin_square'], bigger_square['begin_square'] + bigger_square['size_square']):
            pos.append(x + (nCol * i))
    
    for index, element in enumerate(plan):
        if index in pos:
            output += squareX
        else:
            output += element
            
        if (index + 1) % nCol == 0 and index + 1 != len(plan):
            output += '\n'

    print(output, end='')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing Entry File !!')
        exit()

    for i in range(1, len(sys.argv)):
        try:
            find_bigger_square(sys.argv[i])
        except:
            pass
        
        if i != len(sys.argv) - 1:
            print('\n')
        else:
            print('')