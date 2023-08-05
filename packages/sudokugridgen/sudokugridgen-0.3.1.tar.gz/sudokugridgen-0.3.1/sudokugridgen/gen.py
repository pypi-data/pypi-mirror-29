#!/usr/bin/python

# Generate all sudoku grids of a given rank 
# MIT License
# Copyright 2018 (c) George Carder 2018

################################################
# A set of functions contributing to the task of
# generating all sudoku grids of a given rank.
################################################
# Use and Examples:
#
#
# B=buildAndFinalizeAllLimit(d,L) gives a list
# B where each entry is a d^2xd^2 sudoku grid
# with entris from a set of symbols {1,2,...,d^2}
# The limit is on the number of automorphisms
# applied to the base grid. This limit is useful
# when d is 'big'.. i.e. >2.
#
# B=buildAndFinalizeAllToFile(d) writes to file
# a list of d^2xd^2 sudoku grids with entries
# from the set of symbolds {1,2,...,d^2}
# Writing to file is useful when d is >2.
#
# B=buildAndFinalizeAll(3) gives a list B where
# each entry is a distinct 9x9 sudoku grid with
# entries from set of symbols {1,2,..,9}
#
# B=buildAllBoards(3) gives a list B where each
# entry is a distinct 9x9 sudoku grid with
# entries from set of symbols 
# {[0,0],[1,0],..,[2,2]} i.e. the image
# of addition Z_3xZ_3 with Z_3xZ_3
#
# B=buildStandardBoard(3) gives a single 
# sudoku grid with entries as the previous
# example but the grid configuration arises
# from "standard" ordering of domain wrt
# addition.
#
# buildboard(gen1,gen2,d) builds a sudoku
# grid given generating lists and rank d
#
# buildGenerators(d) gives a pair of 
# 'standard' generators for a given
# rank d
#
# factorial.. we all know what that is..
# factorial(d) gives the unary operator
# d!
#
# boardFinalizer(board,d) takes a board
# with rank d and entries the image 
# of addition (Z_nxZ_n)x(Z_nxZ_n)
# and converts the entries in a well-
# defined way to elements of 
# {1,2,..,n^2}
################################################
################################################

from itertools import permutations
import random

def buildAndFinalizeAllLimit(d,L): #ideal for d==3
    B=buildAllBoards(d)
    F=[]
    for b in B:
        F.append(boardFinalizer(b,d))
    ### here put Aut(n). revision for v0.2.0
    P=list(permutations(range(1,d**2+1)))
    FF=[]
    for r in range(L):
        for f in F:
            N=[]
            ran = random.randint(1, factorial(d**2)-1)
            for i in range(d**2):
                for j in range(d**2):
                    N.append(P[ran][f[j+i*(d**2)]-1])
            FF.append(N)
    return FF 


def buildAndFinalizeAllToFile(d):
    B=buildAllBoards(d)
    F=[]
    for b in B:
        F.append(boardFinalizer(b,d))
    ### here put Aut(n). revision for v0.2.0
    P=list(permutations(range(1,d**2+1)))
    FF.open('genfile.txt','wt')
    FF.write('[')
    for r in range(factorial(d**2)):
        for f in F:
            N=[]
            ran = random.randint(1, factorial(d**2)-1)
            for i in range(d**2):
                for j in range(d**2):
                    N.append(P[ran][f[j+i*(d**2)]-1])
            if r == 0:
                FF.write(repr(N))
            else:
                FF.write(','+repr(N))
    FF.write(']')
    FF.close(']')
    return 0 


def buildAndFinalizeAll(d): #ideal for d==2
    B=buildAllBoards(d)
    F=[]
    for b in B:
        F.append(boardFinalizer(b,d))
    ### here put Aut(n). revision for v0.2.0
    P=list(permutations(range(1,d**2+1)))
    FF=[]
    for r in range(factorial(d**2)):
        for f in F:
            N=[]
            ran = random.randint(1, factorial(d**2)-1)
            for i in range(d**2):
                for j in range(d**2):
                    N.append(P[ran][f[j+i*(d**2)]-1])
            FF.append(N)
    return FF 

def factorial(n): 
    if n==1:
        return 1
    else:
        return n*factorial(n-1)

def buildGenerators(d): 
    # called by buildAllBoards and buildStandarBoard
    gen1=[]
    gen2=[]
    for i in range(d):
        for j in range(d):
            gen1.append([j%d,i%d])
            gen2.append([i%d,j%d])
    return [gen1,gen2]

def permuteGenerator(gen,d):  
    # called by buildAllBoards
    f=factorial(d)
    P=list(permutations(range(1,d+1)))
    ALLGEN=[] # will have d*f rows... (d*d)*d*f length
    for i in range(d):
        for p in range(f):
            toPermute=gen[i*d:(i+1)*d]
            permuted=[]
            for j in range(d):
                permuted.append(toPermute[P[p][j]-1])
            genPermuted=gen[0:(d*d)]
            genPermuted[i*d:(i+1)*d]=permuted
            if (i==0) or (i>0 and p>0):
                ALLGEN.append(genPermuted)
    return ALLGEN

def buildStandardBoard(d): 
    dd=d*d
    gen=buildGenerators(d)
    gen1=gen[0] 
    gen2=gen[1]
    l=dd*dd
    B=[]
    for i in range(dd):
        for j in range(dd):
            B.append(list(map(lambda x,y: (x+y)%d,gen1[i],gen2[j])))
    return B

def buildAllBoards(d): 
    dd=d*d
    gen=buildGenerators(d)
    gen1=gen[0]
    gen2=gen[1]
    allgen1=permuteGenerator(gen1,d)
    allgen2=permuteGenerator(gen2,d)
    BOARDS=[]
    for gen1 in allgen1:
        for gen2 in allgen2:
            board=buildboard(gen1,gen2,d)
            BOARDS.append(board)
    return BOARDS


def buildboard(gen1,gen2,d): 
    # called by buildAllBoards
    dd=d*d
    board=[]
    for i in range(dd):
      for j in range(dd):
        board.append(list(map(lambda x,y: (x+y)%d,gen1[i],gen2[j])))
    return board

def boardFinalizer(board,d):
    gen=buildGenerators(d)
    FinalBoard=[]
    for b in board:
        FinalBoard.append(gen[0].index(b)+1)
    return FinalBoard

