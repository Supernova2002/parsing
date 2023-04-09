import numpy as np
import nltk


def printParse(inTuple, treeCheck,indent):
    temp = ""
    tree = ""
    #print(type(inTuple[1]))
    check = isinstance(inTuple[1], tuple)
    #print(str(check))
    if check is True:
        firstParse,firstTree = printParse(inTuple[1][0],treeCheck,indent+1)
        secondParse,secondTree = printParse(inTuple[1][1],treeCheck,indent+1)
        temp = "[" + inTuple[0] + " " + firstParse + secondParse + ']'
        tree = "[" + inTuple[0] + "\n" + firstTree + "\n " + secondTree + '\n'
        for i in range(indent):
            tree = tree + "\t"
        tree = tree + ']\n'
    else:
       
        temp = "[" + inTuple[0] + " " + inTuple[1] + " ]"
        tree = "[" + inTuple[0] + " " + inTuple[1] + " ]"
    if(indent>0):
        for i in range(indent):
            tree = "\t" + tree
    return temp,tree

def newFind(aCell,bCell,aMat, bMat, termMat):
    #print("in new")
    store = []
    for aTuple in aCell:
        for bTuple in bCell:
            aTerm = aTuple[0]
            bTerm = bTuple[0]
            indices = [i for i, x in enumerate(aMat) if x == aTerm]
            for index in indices:
                if bMat[index] == bTerm:
                    store.append((termMat[index], (aTuple,bTuple)))
    return store

def findNonTerm(aList, bList, aMat, bMat, termMat):
    aTerms = aList.split(',')
    bTerms = bList.split(',')
   
    store = ""
    for aTerm in aTerms:
        for bTerm in bTerms:
            indices = [i for i, x in enumerate(aMat) if x == aTerm]
            #print(indices)
            for index in indices:
                if bMat[index] == bTerm:
                    if store == "":
                        store = termMat[index]
                    else:
                        store = store + ","+ termMat[index]

    return store



#Instead of parseMat, instead maybe just store each rule in a tree as it is traversed, and from top right traverse down from the left
#
fileName = input("Enter relative location of cnf file:\n")
cnfFile = open(fileName, 'r')
treeIn = input("Do you want textual trees to be displayed [y/n] ?: ")
treeCheck = 0
if treeIn  == "y":
    treeCheck = 1

#cnfFile = open("./sampleGrammar.cnf",'r')
productions =  cnfFile.readlines()
nonTermList = []
aList = []
bList = []
for production in productions:
    prodTokens = nltk.word_tokenize(production)
    if len(prodTokens) == 5:
        nonTermList.append(prodTokens[0])
        aList.append(prodTokens[3])
        bList.append(prodTokens[4])
while True:
    #test case is "book the flight through houston"
    
    sentence = input("Enter a sentence:\n")
    if(sentence == "quit"):
        quit()
    tokens = nltk.word_tokenize(sentence)
    offset = 0
    #parseMat = [ [""]*len(tokens) for i in range(len(tokens))]
    parseMat = [[[] for i in range(len(tokens))] for i in range(len(tokens))]
    traceMat = [ [[] for i in range(len(tokens))] for i in range(len(tokens))]
    #traceMat[0][0].append((1,2))
    
    #print(traceMat)
    #parseMat =  np.array([["" for i in range(len(tokens))] for i in range(len(tokens))], dtype = object)
    #print(parseMat)
    for token in tokens:
        for production in productions:
            prodTokens = nltk.word_tokenize(production) 
            if token in prodTokens:
                parseMat[offset][offset].append((prodTokens[0],token))
                
        offset = offset + 1
        #printing goes from lowest row to hightest row
    #print(parseMat)
    productSize = 2
    callNum = 0
    #as product size increases, start of diagonal shifts one to the right, and you have one less check
    for productSize in range(1, len(tokens)):
        for colCount in range (productSize, len(tokens)):
            #print(colCount)
            row = (colCount-productSize)
            #aMat and bMat are each productSize steps out in each direction from their given square
            aMat = parseMat[row][colCount-productSize:colCount]
            tempPos = row+productSize  
            bMat = []
            for tempRow in range(row+1,tempPos+1):
                bMat.append(parseMat[tempRow][colCount])
            #bMat = parseMat[row+1:tempPos+1][colCount]
            for i in range(len(aMat)):
                if aMat[i] == [] or bMat[i] == []:
                    output = []
                else:
                    output = newFind(aMat[i], bMat[i], aList, bList, nonTermList)
                    #print("before call")
                    #print(callNum)
                    #output = findNonTerm(aMat[i], bMat[i], aList, bList, nonTermList)
                    #print("after call")
                    #callNum = callNum + 1
                if output != []:
                    for outTuple in output:
                        parseMat[row][colCount].append(outTuple) 
            #each value at a given index in aMat is followed by the value in the given index at bMat
            #parseMat[row][colCount] = parseMat[row][colCount] + "visited, "

        #k at 1 to start
        # j = i - k  where k is # of words to start, increment k by 1
        # j is from k to length of tokens
        #i is probably j-k
        #cannot go further down than k -1 
        #productOffset can never be more than # tokens - 1
        

        # good idea to break out all items to left of given square and below it into their own matrices, and just step through each of them in lockstep
       # while(localOffset<= len(tokens)-1-productSize):
        #    local
    
    #print(parseMat[0][len(tokens)-1])
    #print(traceMat)
    final = len(parseMat[0][len(tokens)-1])
    #final = len(parseMat[0][len(tokens)-1].split(','))
    if final == 0:
        print("No valid parses")
    else:
        print(str(final) + " valid parses")
    parseCount = 1
    for finalTuple in parseMat[0][len(tokens)-1]:
        parse,tree = printParse(finalTuple,0,0)
        print("Valid Parse # " +  str(parseCount) + ":\n" + parse)
        if(treeCheck):
            print(tree)
        parseCount = parseCount + 1







                
    
