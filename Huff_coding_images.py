"""
Created on Sun Jun 16 2019

@author: Ashwin
"""
#Python script to compress images using Huffman encoding technique.
#The input is a 2 dimensional ndarray
#openCV has been used to handle images.
#Here the encoding and decoding processes are carried out in the same script.
#If the user wants to perform these operations in two different scripts, the 
#encoded text AND the code dictionary can be saved in file (at transmitter), to
#be read from during the decoding process (at receiver). The coded o/p has to 
#be reshaped into a matrix and converted to decimal form before saving. 
#Otherwise size of the saved file exceeds the size of the original image.

import math
import cv2
import numpy as np
COUNT = 0
        
#Saves symbol information and position in binary tree         
class Node:
    def __init__(self, label = None, freq = None, parent = None, left = None, right = None):
        self.label = label
        self.freq = freq
        self.parent = parent
        self.left = left
        self.right = right
        
    def __add__(self,o):
        return self.freq + o.freq

#Sort a list with elements of the type Node            
def sortList(L):
    l = len(L)
    for i in range(0,l-1):
        for j in range(0,l-i-1):
            if(L[j].freq < L[j+1].freq):
                L[j],L[j+1] = L[j+1],L[j]           
           
#Print the details of a Node                
def printNodeList(L):    
    if isinstance(L,list):
        for i in L:
            print("%s:%d"%(i.label,i.freq), end=" ")            
        print("\n")
    else:
        print("Not a list\n")
    
#Print a list with elements of type Node            
def printNode(N):
    if(N==None):
        print("None\n")
    else:
        print("%s:%d\n"%(N.label,N.freq)) 

#Generate a dictionary with frequency of each symbol in the input                
def generateFrequencyVector(inp):
    Dict = {}
    for i in inp:
        if i in Dict:
            Dict[i] += 1
        else:
            Dict[i] = 1
    L = []
    for i in Dict:
        L.append(Node(i,Dict[i]))
    sortList(L)
    return L        
    
#Generate a new node combining two node with the least frequency               
def generateNode(T,count):    
    if(count==1):
        sortList(T)        
    A = T.pop()
    B = T.pop()
    C = Node()
    C.freq = A + B
    C.label = "N"+str(count)
    T.append(C)
    sortList(T)
    
#Updates the stack after creation of each new node. Useful for visualisation.        
def huffStack(T):
    global COUNT
    if(len(T)<2):
        printNode(T.pop())
        COUNT = 0
    else:        
        COUNT += 1
        generateNode(T,COUNT)
        printNodeList(T)
        huffStack(T)
        
#Generate new leaf node from 2 nodes with least frequencies             
def generateLeaf(T,count):
    if(count==1):
        sortList(T)        
    A = T.pop()
    B = T.pop()
    C = Node()
    C.freq = A + B
    C.label = "N"+str(count)
    if(A.freq <= B.freq):
        C.left = A
        C.right = B
    else:
        C.left = B
        C.right = A
    A.parent = C
    B.parent = C    
    T.append(C)
    sortList(T)   
     
#Generate the Binary tree        
def huffTree(T):
    global COUNT    
    if(len(T)==1):
        COUNT = 0                                
    else:
        COUNT += 1
        generateLeaf(T,COUNT)        
        huffTree(T)
        
#Generate a dictionary with the location of each symbol in the binary tree
def saveSymbolLocation(L):
    Dict = {}
    for i in L:
        Dict[i.label] = i
    return Dict
        
#Create an empty code dictionary
def generateEmptyCodeDict(L):
    Dict = {}
    for i in L:
        Dict[i.label] = []
    return Dict

#Generate variable length binary code for each symbol by traversing the binary 
#tree
def generateCodeDict(L,loc,codeDict):
    huffTree(L)
    root = L.pop()
    Keys = codeDict.keys() 
    for i in Keys:
        current = loc[i]    
        while(current != root):
            if(current == current.parent.left):
                codeDict[i].append(0)
            else:
                codeDict[i].append(1)            
            current = current.parent   
        codeDict[i] = codeDict[i][::-1]  
        codeDict[i] = "".join(str(j) for j in codeDict[i])                        
        
#Encode the input according to the encoding dictionary                
def huffmanEncoding(codeDict, inp):
    codedText = ""    
    for i in inp:
        codedText += codeDict[i]   
    print("Encoding complete...")
    return codedText  
      
#Parameters associated with the compression process
def compressionMetrics(inp,codeDict,codedText):
    n = math.ceil(math.log(len(codeDict),2))
    print("\n\nNo. of bits before compression: %d"%(n*len(inp)))      
    print("No. of bits after compression: %d"%(len(codedText)))    
    print("Compression Ratio: %.4f\n\n"%((n*len(inp))/len(codedText)))

#Interchange the key value pair in a dictionary
def swapDict(Dict):
    return dict([(value, key) for key, value in Dict.items()]) 

#Decode encoded binary text using the code dictionary
def huffmanDecoding(codeDict,codedText):
    decodeDict = swapDict(codeDict)
    decodedText = []
    tempCode = ""    
    for i in codedText:
        tempCode += i
        if tempCode in decodeDict:
            decodedText.append((decodeDict[tempCode]))
            tempCode = ""
    print("Decoding complete...")
    return decodedText    
    
#Reshape the image vector to image matrix
def vector2Matrix(V,r,c):
    M = np.zeros((r,c))
    for i in range(0,r):
        for j in range(0,c):
            M[i][j] = V[c*i + j]            
    return M
    
#Driver function
def main():        
    image = cv2.imread("clouds.jpg")                                            #Read image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dims = gray_image.shape
    img_vector = gray_image.reshape(1,dims[0]*dims[1])                          #Convert to vector
    inp = img_vector[0]
    L = generateFrequencyVector(inp)                                            #Count frequency 
    elementLocations = saveSymbolLocation(L)
    codeDict = generateEmptyCodeDict(L)     
    generateCodeDict(L,elementLocations,codeDict)                               #Code dictionary
    print(codeDict)
    
    codedImgVec = huffmanEncoding(codeDict, inp)                                #Huffman encoding
    print("\nCoded o/p: ",end="")        
    print(type(codedImgVec)  )
    compressionMetrics(inp,codeDict,codedImgVec)                                #Compression metrics
    
    decodedImgVec = huffmanDecoding(codeDict,codedImgVec)                       #Huffman decoding
    decodedImg = vector2Matrix(decodedImgVec,dims[0],dims[1]).astype(np.uint8)  #Reshape vector to matrix
    cv2.imshow("Clouds_Original",gray_image)
    cv2.imshow('Clouds_Recovered',decodedImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  
        
main()    