def Evaluate(state):
    return 0

def isTerminal(state):
    return True

def getChildren(state):
    children = []
    for i in range(7):
        tmp = [row[:] for row in state]
        for j in range(6):
            if tmp[i][j] == 0:
                tmp[i][j] = 2
                children.append(tmp.copy())
    return children



def minimax(state, k, IsMaximizing):
    if( k == 0 or isTerminal(state)):
        return Evaluate(state)

    if(IsMaximizing):
        bestValue = int(float('-inf'))
        children = getChildren(state)
        for child in children:
            value = minimax(child,k-1,False)
            bestValue = max(value, bestValue)
        return bestValue

    else:
        bestValue = int(float('inf'))
        children = getChildren(state)
        for child in children:
            value = minimax(child,k-1,True)
            bestValue = min(value, bestValue)
        return bestValue
