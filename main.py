def Evaluate(state):
    return 0

def isTerminal(state):
    return True

def getChildren(state):
    return 0
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
