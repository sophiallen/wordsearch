from random import randint

def initMatrix(n):
    '''creates n arrays of n random letters'''
    matrix = []
    for i in range(n):
        L = []
        for i in range(n):
            ltr = randint(ord('A'),ord('Z'))
            L.append(chr(ltr))
        matrix.append(L)
    return matrix
