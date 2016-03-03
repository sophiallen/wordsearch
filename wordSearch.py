from random import randint


def mapLetters():
    #dict that tracks letter frequency
    ltrFreqs = {'a':8,'b':2,'c':3,'d':4,'e':13,'f':2,'g':3,'h':6,'i':7,'j':1,'k':1,'l':4,'m':2,'n':6,'o':6,'p':2,'q':1,'r':6,'s':6,'t':9,'u':3,'v':1,'x':1,'y':2,'z':1}
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

def initDict(dictFile):
    '''loads American English scrabble word list I downloaded from http://www.puzzlers.org/pub/wordlists/ospd.txt'''
    d = {}  #hash table for constant time lookup.
    infile = open(dictFile,'r')
    for line in infile:
            d[line[:-1]] = 0  #store in dictionary
    infile.close()
    return d

def loadMatrix(filename):
    infile = open(filename, 'r')
    matrix = []
    for line in infile:
        row = []
        L = line[:-1]
        lnth = len(row)
        for ltr in L:
            row.append(ltr)
        matrix.append(row)
    infile.close()
    return matrix

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

def miniDg(matrix, row, ndx):
    rows = len(matrix)
    columns = len(matrix[0])
    found = []
    wordlen = 1
    word = matrix[row][ndx]
    while wordlen + ndx < columns and wordlen + row < rows:
        newrow = wordlen + row
        newndx = wordlen + ndx
        word += matrix[newrow][newndx]
        wordlen += 1
        found.append(word)
    return found
        

def miniHz(matrix, row, ndx):
    word = matrix[row][ndx]
    found = []
    while ndx + 1 < len(matrix[row]):
        ndx += 1
        word += matrix[row][ndx]
        found.append(word)
    return found

def miniVt(matrix, rownum, ndx):
    word = matrix[rownum][ndx]
    found = []
    lng = len(matrix) - rownum
    for i in range(1,lng):
        word += matrix[rownum+i][ndx]
        found.append(word)
    return found
        
def wordSearchFromFile(dictionary, matrix):
    matrix = loadMatrix(matrix)
    Dict = initDict(dictionary)
    allFound = []
    wordsFound = []
    h = len(matrix)
    w = len(matrix[0])
    longest = ""
    for r in range(h): 
        for i in range(w):
            allFound += miniHz(matrix, r, i)
            allFound += miniVt(matrix, r, i)
            allFound += miniDg(matrix, r, i)
    for word in allFound:
        if word in Dict and word not in wordsFound:
            wordsFound.append(word)
            if len(word) > len(longest):
                longest = word
    print('longest word:', longest)
    print('words found:', len(wordsFound))
    return wordsFound

def autoWordSearch(n):
    matrix = initMatrix(n)
    Dict = initDict('ScrabbleDict.txt')
    allFound = []
    wordsFound = []
    h = len(matrix)
    w = len(matrix[0])
    longest = ""
    for r in range(h): 
        for i in range(w):
            allFound += miniHz(matrix, r, i)
            allFound += miniVt(matrix, r, i)
            allFound += miniDg(matrix, r, i)
    for word in allFound:
        if word in Dict and word not in wordsFound:
            wordsFound.append(word)
            if len(word) > len(longest):
                longest = word
    return len(wordsFound)

def avgWordsFound(strt, upto, times):
    sums = {}
    for i in range(strt, upto+1):
        for p in range(times):
            numFound = autoWordSearch(i)
            if i in sums:
                sums[i] += numFound
            else:
                sums[i] = numFound
    for key in sums:
        sums[key] /= times
    print(sums)              

def wordSearch(n):
    matrix = initMatrix(n)
    dictionary = initDict()
    wordsFound = []
    wordsFound += vtSearch(dictionary, matrix, n)
    wordsFound += hzSearch(dictionary, matrix, n)
    wordsFound += diagSearch(dictionary, matrix, n)
    print('words found:', len(wordsFound))
    print(wordsFound)
