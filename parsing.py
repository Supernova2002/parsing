import numpy as np
import nltk


def findNonTerm(aList, bList, productions):
    aTerms = aList.split(',')
    bTerms = bList.split(',')
    store = ""
    for aTerm in aTerms:
        for bTerm in bTerms:
            for production in productions:
                prodTokens = nltk.word_tokenize(production)
                if len(prodTokens) == 5:
                    if aTerm == prodTokens[3] and bTerm == prodTokens[4]:  #issue is it isn't checking the order
                        if store == "":
                            store = store + prodTokens[0]
                        else:

                            store = store + ","+ prodTokens[0]

    return store


print("Hello world")


cnfFile = open("./sampleGrammar.cnf",'r')
productions =  cnfFile.readlines()
while True:
    #test case is "book the flight through houston"
    
    sentence = input("Enter a sentence:\n")
    if(sentence == "quit"):
        quit()
    tokens = nltk.word_tokenize(sentence)
    offset = 0
    #parseMat = [ [""]*len(tokens) for i in range(len(tokens))]
    parseMat =  np.array([["" for i in range(len(tokens))] for i in range(len(tokens))], dtype = object)
    #print(parseMat)
    for token in tokens:
        for production in productions:
            prodTokens = nltk.word_tokenize(production)
            if token in prodTokens:
                if parseMat[offset,offset] == "":
                    parseMat[offset,offset] = prodTokens[0]
                else:
                    parseMat[offset,offset] = parseMat[offset,offset] + "," + prodTokens[0]
                #print(prodTokens[0])
        offset = offset + 1
        #printing goes from lowest row to hightest row
    #print(parseMat)
    productSize = 2
    #as product size increases, start of diagonal shifts one to the right, and you have one less check
    for productSize in range(1, len(tokens)):
        for colCount in range (productSize, len(tokens)):
           
            row = (colCount-productSize)
            #aMat and bMat are each productSize steps out in each direction from their given square
            aMat = parseMat[row,colCount-productSize:colCount]
            tempPos = row+productSize  
            bMat = parseMat[row+1:tempPos+1,colCount]
            for i in range(len(aMat)):
                output = findNonTerm(aMat[i], bMat[i], productions)
                if output != "":
                    if parseMat[row, colCount] == "":
                        parseMat[row,colCount] = output
                    else:
                        parseMat[row,colCount] = parseMat[row,colCount] + "," + output 
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
    print(parseMat)
        








                
    
