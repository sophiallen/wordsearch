from random import randint


def mapLetters():
    #dict that tracks letter frequency
    ltrFreqs = {'a':8,'b':2,'c':3,'d':4,'e':13,'f':2,'g':2,'h':6,'i':7,'j':1,'k':1,'l':4,'m':2,'n':6,'o':7,'p':2,'q':1,'r':6,'s':6,'t':9,'u':3,'v':1,'x':1,'y':2,'z':1}
    #dict to map numbers to letters, according to frequency. 
    maps = {}
    count = 1
    for key in ltrFreqs:
        for i in range(ltrFreqs[key]):
            maps[count] = key
            count += 1
    return maps

def initMatrix(n):
    '''creates n arrays of n random letters'''
    matrix = []
    letters = mapLetters()
    for i in range(n):
        L = []
        for i in range(n):
            num = randint(1,100)
            ltr = letters[num]
            L.append(ltr)
        matrix.append(L)
    return matrix

def initDict():
    '''loads American English scrabble word list I downloaded from http://www.puzzlers.org/pub/wordlists/ospd.txt'''
    d = {}  #hash table for constant time lookup.
    infile = open('scrabbledict.txt','r')
    for line in infile:
            d[line[:-1]] = 0  #store in dictionary
    infile.close()
    return d

def buildWord(L):
    word = ''
    for ltr in L:
        word += ltr
    return word

def hzSearch(dictionary, matrix, n):
    '''searches rows horizontally for words'''
    wordsFound = []
    for row in matrix:
        for i in range(n): #each letter in the row 
            wordlen = 2  #keep track to the word length, which must be at least two letters long. 
            while wordlen+i <= n: #while the length is less than the length of the row
                word = buildWord(row[i:i+wordlen])
                if word in dictionary and word not in wordsFound:
                    wordsFound.append(word)
                wordlen += 1
    return wordsFound
            

def vtSearch(dictionary, matrix, n):
    wordsFound = []
    for r in range(n): #for each row in matrix
        for i in range(n): #for each letter in row
            wordlen = 1
            word = matrix[r][i]
            while r + wordlen <= n-1:
                word += matrix[r+wordlen][i]
                if word in dictionary and word not in wordsFound:
                    wordsFound.append(word)
                wordlen += 1
    return wordsFound

def diagSearch(dictionary, matrix, n):
    wordsFound = []
    for r in range(n):
        for i in range(n):
            wordlen = 1
            word = matrix[r][i]
            while wordlen+i < n:
                word += matrix[i+wordlen][i+wordlen]
                if word in dictionary and word not in wordsFound:
                    wordsFound.append(word)
                wordlen += 1
    return wordsFound
        

def wordSearch(n):
    matrix = initMatrix(n)
    dictionary = initDict()
    print(matrix)
    wordsFound = []
    wordsFound += vtSearch(dictionary, matrix, n)
    wordsFound += hzSearch(dictionary, matrix, n)
    wordsFound += diagSearch(dictionary, matrix, n)
    print('words found:', len(wordsFound))
    print(wordsFound)
