#!/usr/bin/env python3
'''
      Author: Genadi Shamugia
      Course: SY303
     Section: 4321
Program Name: Assembler.py
 Description: Program is written in python3 and is used assemble Hack assembly
              language code into machine instructions.
'''
import sys

def main():

    #Usage Statement
    if len(sys.argv)!=2:
        print("Usage: Assemly.py <file.asm>\n")
        print("Description:\n\tProgram is written in python3 and is used assemble Hack assembly\n\tlanguage code into machine instructions.")
        sys.exit()
        
    #Symbol table
    loopDict={}
    findLoops(loopDict)
    lineCount=0
    varOriginalLoc = 16
    varRegTable={"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576}
    
    #Read filename from Command line argument.
    fd = open(sys.argv[1],'r') #Open file to read
    file_read_full_line = fd.readline()
    fileNameSplit = str(sys.argv[1]).split(".")
    fileName = fileNameSplit[0]+".hack"
    outputfile = open(fileName,'w+') #Open output file

    DestIn=False
    JmpIn=False
    while file_read_full_line !="":
        if (file_read_full_line.strip()).startswith("//") or file_read_full_line=="\n" or (file_read_full_line.strip()).startswith("("): #Ignore comment lines, gobacks and empty lines
            file_read_full_line=fd.readline()
        else:
            file_read_withComments=file_read_full_line.split("//") #handle comments on same line as asm code
            file_read=file_read_withComments[0].strip()
            if file_read[0]=="@":
                value = file_read[1:]
                if value.isdigit(): #Value after @ is a number
                    binStr=str(bin(int(value)))
                    binVal=binStr[2:]
                    binLen=len(binVal)
                    numFillZeros=16-binLen
                    finalStr="0"*numFillZeros+binVal+'\n'
                    file_read_full_line = fd.readline()
                    outputfile.write(finalStr)
                    lineCount+=1
                    continue
                elif value in varRegTable: #Variable is defined already
                    binStr=str(bin(varRegTable[value]))
                    binVal=binStr[2:]
                    binLen=len(binVal)
                    numFillZeros=16-binLen
                    finalStr="0"*numFillZeros+binVal+'\n'
                    file_read_full_line = fd.readline()
                    outputfile.write(finalStr)
                    lineCount+=1
                    continue
                elif value in loopDict: #Variable is a special goto symbol
                    binStr=str(bin(loopDict[value]))
                    binVal=binStr[2:]
                    binLen=len(binVal)
                    numFillZeros=16-binLen
                    finalStr="0"*numFillZeros+binVal+'\n'
                    file_read_full_line = fd.readline()
                    outputfile.write(finalStr)
                    lineCount+=1
                else: #not yet defined variables.
                    varRegTable[value]=varOriginalLoc
                    binStr=str(bin(varOriginalLoc))
                    binVal=binStr[2:]
                    binLen=len(binVal)
                    numFillZeros=16-binLen
                    finalStr="0"*numFillZeros+binVal+'\n'
                    file_read_full_line = fd.readline()
                    outputfile.write(finalStr)
                    varOriginalLoc+=1
                    lineCount+=1

            #C instrcution
            #Dest bits
            else:
                if "=" in file_read:
                    DestIn=True
                    splits=file_read.split("=")
                    destPart=splits[0]
                    if destPart == "M":
                        destBits="001"
                    elif destPart == "D":
                        destBits="010"
                    elif destPart == "MD":
                        destBits="011"
                    elif destPart == "A":
                        destBits="100"
                    elif destPart == "AM":
                        destBits="101"
                    elif destPart == "AD":
                        destBits="110"
                    elif destPart == "AMD":
                        destBits="111"

                #Jmp bits
                if ";" in file_read:
                    JmpIn=True
                    splits=file_read.split(";")
                    JmpPart=splits[-1]
                    if JmpPart == "JGT":
                        JmpBits="001"
                    elif JmpPart == "JEQ":
                        JmpBits="010"
                    elif JmpPart == "JGE":
                        JmpBits="011"
                    elif JmpPart == "JLT":
                        JmpBits="100"
                    elif JmpPart == "JNE":
                        JmpBits="101"
                    elif JmpPart == "JLE":
                        JmpBits="110"
                    elif JmpPart == "JMP":
                        JmpBits="111"

                #Comp bits
                if "=" in file_read and ";" not in file_read:
                    splits=file_read.split("=")
                    compPart=splits[1].strip()
                elif "=" not in file_read and ";" in file_read:
                    splits=file_read.split(";")
                    compPart=splits[0].strip()
                elif "=" in file_read and ";" in file_read:
                    firstSplit=file_read.split("=")
                    secondSplit=(firstSplit[1]).split(";")
                    compPart=secondSplit[0]/strip()
                if compPart=="0":
                    abit="0"
                    compBits="101010"
                elif compPart=="1":
                    abit="0"
                    compBits="111111"
                elif compPart=="-1":
                    abit="0"
                    compBits="111010"
                elif compPart=="D":
                    abit="0"
                    compBits="001100"
                elif compPart=="A":
                    abit="0"
                    compBits="110000"
                elif compPart=="!D":
                    abit="0"
                    compBits="001101"
                elif compPart=="!A":
                    abit="0"
                    compBits="110001"
                elif compPart=="-D":
                    abit="0"
                    compBits="001111"
                elif compPart=="-A":
                    abit="0"
                    compBits="110011"
                elif compPart=="D+1":
                    abit="0"
                    compBits="011111"
                elif compPart=="A+1":
                    abit="0"
                    compBits="110111"
                elif compPart=="D-1":
                    abit="0"
                    compBits="001110"
                elif compPart=="A-1":
                    abit="0"
                    compBits="110010"
                elif compPart=="D+A":
                    abit="0"
                    compBits="000010"
                elif compPart=="D-A":
                    abit="0"
                    compBits="010011"
                elif compPart=="A-D":
                    abit="0"
                    compBits="000111"
                elif compPart=="D&A":
                    abit="0"
                    compBits="000000"
                elif compPart=="D|A":
                    abit="0"
                    compBits="010101"
                elif compPart=="M":
                    abit="1"
                    compBits="110000"
                elif compPart=="!M":
                    abit="1"
                    compBits="110001"
                elif compPart=="-M":
                    abit="1"
                    compBits="110011"
                elif compPart=="M+1":
                    abit="1"
                    compBits="110111"
                elif compPart=="M-1":
                    abit="1"
                    compBits="110010"
                elif compPart=="D+M":
                    abit="1"
                    compBits="000010"
                elif compPart=="D-M":
                    abit="1"
                    compBits="010011"
                elif compPart=="M-D":
                    abit="1"
                    compBits="000111"
                elif compPart=="D&M":
                    abit="1"
                    compBits="000000"
                elif compPart=="D|M":
                    abit="1"
                    compBits="010101"

                if DestIn==True:
                    compAndDest=compBits+destBits
                elif DestIn==False:
                    compAndDest=compBits+"000"
                if JmpIn==True:
                    compAndDestAndJmp = compAndDest+JmpBits
                elif JmpIn==False:
                    compAndDestAndJmp = compAndDest+"000"
                #Build the final C instruction machine code
                finalCinstr="111"+abit+compAndDestAndJmp+"\n"
                file_read_full_line = fd.readline()
                outputfile.write(finalCinstr)
                lineCount+=1
                DestIn=False
                JmpIn=False

def findLoops(loopDict): #Function finds all the goto loop symbols and creates
    counter=0            #a dictionary which has the symbol name as a key and
    filteredList = []    #the line it appears on as a value.
    fd = open(sys.argv[1],'r')
    listLines = fd.readlines()
    for item in listLines:
        if item.startswith("//") or item=="\n":
            continue
        else:
            filteredList.append(item)
    for item in filteredList:
        if item[0]=="(":
            loopDict[item.strip("(").strip(")\n")]=counter
        else:
            counter+=1
    return loopDict

if __name__=="__main__":
    main()
