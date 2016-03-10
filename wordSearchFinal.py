import random


def letterList():
    '''Creates a list of letters, where each letter appears according to
    its relative frequency in typical english writing.'''

    #dictionary of letters paired with their relative fequencies. 
    ltrFreqs = {'a':8,'b':2,'c':3,'d':4,'e':13,'f':2,'g':3,'h':6,'i':7,'j':1,'k':1,'l':4,'m':2,'n':6,'o':6,'p':2,'q':1,'r':6,'s':6,'t':9,'u':3,'v':1,'x':1,'y':2,'z':1}

    #empty list accumulator. 
    ltrs = []

    #for each letter, add it as many times to the list as its frequency suggests.
    for key in ltrFreqs:
        for i in range(ltrFreqs[key]):
            ltrs.append(key)
            
    #return the list of letters for use by later functions.  
    return ltrs



def initMatrix(n):
    '''creates an nXn matrix of (semi)random letters'''
    #starts with empty list accumulator to hold completed matrix, and list of letters.
    matrix = []
    letters = letterList()
    
    #for each row, create a list to represent that row. 
    for i in range(n):
        L = []
        #for each column, select a random letter from the list and add it to the row.
        for i in range(n):
            ltr = random.choice(letters)
            L.append(ltr)
        #append the completed row to the matrix. 
        matrix.append(L)
        
    #return completed matrix for later use.    
    return matrix

def loadDict(dictFile):
    '''loads American English dictionary from file. I downloaded one
    from http://www.puzzlers.org/pub/wordlists/ospd.txt'''
    #starts by creating an empty dictionary to hold loaded words,
    #and opening the dictionary file.
    d = {}
    infile = open(dictFile,'r')
    #since each word is on its own line, add the word (sans the \n) to the dictionary acccumulator. 
    for line in infile:
            d[line[:-1]] = 0  
    #close the file and return the dictionary of words. 
    infile.close()
    return d

def loadMatrix(filename):
    '''loads a pre-built matrix from a file'''
    #open the file for reading, initialize matrix as an empty list accumulator.
    infile = open(filename, 'r')
    matrix = []
    #for each line of letters in the file: 
    for line in infile:
        #create empty row as a list accumulator, read the letters from file (except line break)
        row = []
        L = line[:-1]
        #for each letter in the line, append it as an item in row. 
        for ltr in L:
            row.append(ltr)
        #add completed rows to the matrix
        matrix.append(row)
    #close the file and return loaded matrix. 
    infile.close()
    return matrix

def hzSearch(matrix, row, ndx):
    '''Given starting coordinates within a matrix, searches for possible words
    horizontally, returns list of possibilities'''
    #start with base letter, at the coordinates given. 
    word = matrix[row][ndx]
    #create empty list to hold possible words. 
    found = []
    
    #while there's at least one letter to the right of that letter
    while ndx + 1 < len(matrix[row]):
        #shift the index to point to next letter
        ndx += 1
        #add that letter to the prior base word
        word += matrix[row][ndx]
        #add that word to the list of possibilities. 
        found.append(word)
        
    #return list of possible words. 
    return found

def vtSearch(matrix, row, ndx):
    '''Given starting coordinates within a matrix, searches for possible
    words vertically, returns list of possibilities'''
    #again, start with letter at given coordinates, and initialize list to hold possible words. 
    word = matrix[row][ndx]
    found = []
    
    #based on the row given, find out how many rows are beneath it.
    lng = len(matrix) - row

    #for each row beneath the starting row,
    for i in range(1,lng):
        #add the letter that's in the same column from that row to the base word
        word += matrix[row+i][ndx]
        #append that word to the list. 
        found.append(word)
        
    #return list of possible words. 
    return found

def dgSearchRt(matrix, row, ndx):
    '''given starting coordinates within a matrix, searches for possible words
    diagonally to the right and down, returns list of possible words.'''
    #start by figuring out how many rows and columns are in the matrix as a whole. 
    num_rows = len(matrix)
    num_columns = len(matrix[0])
    #initialize list accumulator, counter to track word size, and base word.
    found = []
    wordlen = 1
    word = matrix[row][ndx]

    #while there are columns to the right, and rows beneath:
    while wordlen + ndx < num_columns and wordlen + row < num_rows:
        
        #set new row and column coordinates by shifting down and right by distance of wordlen.
        newrow = row + wordlen 
        newndx = ndx + wordlen
        
        #add the letter at the new coordinates to the base word. 
        word += matrix[newrow][newndx]
        
        #increase the shift distance by one. 
        wordlen += 1
        
        #add word to the list of possibilities. 
        found.append(word)
        
    return found


def dgSearchLt(matrix, row, ndx):
    '''given starting coordinates within a matrix, searches for possible
    words diagonally to the left and down, returns list of possible words.'''
    num_rows = len(matrix)
    num_columns = len(matrix[0])
    found = []
    wordlen = 1
    word = matrix[row][ndx]
    #Main difference from right diag search:
    ##This one checks for space remaining to the left of the letter
    while ndx - wordlen >= 0 and wordlen + row < num_rows:
        newrow = row + wordlen
        #and moves ndx left after shifting to row below. 
        newndx = ndx - wordlen
        word += matrix[newrow][newndx]
        wordlen += 1
        found.append(word)
    return found


def wordSearchFromFile(dictionary, matrix, outfile):
    '''given dictionary and matrix infiles, returns a list of English Words
    that can be built horizontally, vertically, and diagonally'''
    #First, loads matrix and dictionary from specified files. 
    matrix = loadMatrix(matrix)
    Dict = loadDict(dictionary)
    #initializes two lists, one for all possible letter combinations in each direction, and one for unique and valid english words. 
    allFound = []
    wordsFound = []

    #get the number of rows and columns (height and width) based on matrix loaded from infile. 
    height = len(matrix)
    width = len(matrix[0])

    #for each row in the matrix, 
    for row in range(height):
        #and each letter/column of each row:
        for col in range(width):
            #add possible letter combinations returned from searching in each direction. 
            allFound += hzSearch(matrix, row, col)
            allFound += vtSearch(matrix, row, col)
            allFound += dgSearchLt(matrix, row, col)
            allFound += dgSearchRt(matrix, row, col)
    #then go through the possible letter combinations, 
    for word in allFound:
        #and check if it's in the dictionary, and that it hasn't already been found. 
        if word in Dict and word not in wordsFound:
            #if both conditions are true, add it to the list of words found. 
            wordsFound.append(word)
    #sort the list of words found
    wordsFound = sorted(wordsFound)

    #create/open a file to write to with the specified name
    outfile = open(outfile, 'w')
    
    #add each word from the list of those found, on its own line.
    for item in wordsFound:
        outfile.write(item +'\n')

    #and close the file. 
    outfile.close()


def autoWordSearch(n):
    '''searches an automatically generated matrix of size nXn, returns list of
    all unique english words found.'''

    #create a matrix of size nXn, and use the standard scrabble library. 
    matrix = initMatrix(n)
    Dict = loadDict('ScrabbleDict.txt')

    #set up same list accumulators and starting values as when searching from a file. 
    allFound = []
    wordsFound = []
    #since height and width are both n, we can use it to keep count of both rows and columns. 
    for row in range(n): 
        for col in range(n):
            allFound += hzSearch(matrix, row, col)
            allFound += vtSearch(matrix, row, col)
            allFound += dgSearchLt(matrix, row, col)
            allFound += dgSearchRt(matrix, row, col)
    for word in allFound:
        if word in Dict and word not in wordsFound:
            wordsFound.append(word)
    #return list of unique english words. 
    return wordsFound

def avgWordsFound(strt, upto, times):
    '''returns average number of words found in matrixes ranging from
    starting size strt to end size upto, after times repetitions.'''
    #initialize dictionary to accumulate pairs of matrix size / words found later. 
    sums = {}
    #for each matrix size in the range specified: 
    for i in range(strt, upto+1):
        #repeat automatic word search for the specified number of times. 
        for p in range(times):
            #get the number of words found for each new search
            numFound = len(autoWordSearch(i))
            #and add to or create a key-value pair linking size to total number found.
            if i in sums:
                sums[i] += numFound
            else:
                sums[i] = numFound
    #after all repetitions and sizes tried, go through each key and divide total words found by the number of repetitions. 
    for key in sums:
        sums[key] /= times
    #return dictionary of averages linked to matrix sizes. 
    print(sums)

def maxValKey(D):
    '''takes a dictinary, returns key with highest value'''
    #create list of keys, and list of values
    keys = list(D.keys())
    vals = list(D.values())
    #get the key that has the same index as the largest value, and return it. 
    return keys[vals.index(max(vals))]
    

def mostCommonWordLen(mSize, times):
    '''finds the most common word and length of words found in matrix of size
    mSize after times repetitions.'''
    #two dictionaries: one to hold words found and number of times found, 
    wordOccurs = {}
    #and one to hold length of words found and number of words found with that length.
    lenOccurs = {}

    #for each of the number of specified repetitions: 
    for i in range(times):
        #get list of words returns from searching a matrix of mSize.
        wordSet = autoWordSearch(mSize)

        #and then go through each word in the set, and add its occurrence and length to appropriate dicitonary accumulators. 
        for word in wordSet:
            if word in wordOccurs:
                wordOccurs[word] += 1
            else:
                wordOccurs[word] = 1
            if len(word) in lenOccurs:
                lenOccurs[len(word)] += 1
            else:
                lenOccurs[len(word)] = 1
    #get the word with the highest number of times occurred. 
    mcWord = maxValKey(wordOccurs)
    #get the length with highest number of times occurred. 
    mcLen = maxValKey(lenOccurs)

    #return the most common word and length. 
    return mcWord, mcLen


def wordSearchStats(frm, upto, stepsz, times):
    '''prints a table of most common word size and lenth for square matrixes of
    size frm to size upto in steps of stepsz after times repetitions.'''

    #label for the table: 
    print('Matrix Size: ','Common Word: ','Common Length: ')
    print('-'*42)
    
    #loop through sizes in range and step size specified
    for i in range(frm, upto+1, stepsz):
        
        #get the most common word and length, with 'times' repetitions. 
        result = mostCommonWordLen(i, times)
        
        #print results to new line in the table, formatting for alignment. 
        print("{0:^10}{1:^20}{2:^10}".format(i, result[0], result[1]))
    
        
    



