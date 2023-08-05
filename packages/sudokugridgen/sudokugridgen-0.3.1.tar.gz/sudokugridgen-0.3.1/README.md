# Sudoku Grid generator  
### 
Published to pypi.org as sudokugridgen

From the root directory of the download
sudo pip3 install .

# Generate all sudoku grids of a given rank 
# MIT License
# Copyright 2018 (c) George Carder 2018

################################################
# A set of functions contributing to the task of
# generating all sudoku grids of a given rank.
################################################
# Use and Examples:
#

 B=buildAndFinalizeAllLimit(d,L) gives a list
 B where each entry is a d^2xd^2 sudoku grid
 with entris from a set of symbols {1,2,...,d^2}
 The limit is on the number of automorphisms
 applied to the base grid. This limit is useful
 when d is 'big'.. i.e. >2.

 B=buildAndFinalizeAllToFile(d) writes to file
 a list of d^2xd^2 sudoku grids with entries
 from the set of symbolds {1,2,...,d^2}
 Writing to file is useful when d is >2.
 Careful, this file accumulates to about 23GB.

 B=buildAndFinalizeAll(3) gives a list B where
 each entry is a distinct 9x9 sudoku grid with
 entries from set of symbols {1,2,..,9}

 CAUTION: buildAndFinalizeAll(d) computes in 
 under a second for d=2. But the computational
 complexity of this function is very steep. 
 As such, for d=3 prepare to wait. But the 
 quality of the output is worth it.

 B=buildAllBoards(3) gives a list B where each
 entry is a distinct 9x9 sudoku grid with
 entries from set of symbols 
 {[0,0],[1,0],..,[2,2]} i.e. the image
 of addition Z_3xZ_3 with Z_3xZ_3

 B=buildStandardBoard(3) gives a single 
 sudoku grid with entries as the previous
 example but the grid configuration arises
 from "standard" ordering of domain wrt
 addition.

 buildboard(gen1,gen2,d) builds a sudoku
 grid given generating lists and rank d

 buildGenerators(d) gives a pair of 
 'standard' generators for a given
 rank d
 permutations(d) gives a list (matrix)
 where each row is a distinct permutation
 of d symbols (indoarabic numerals)

 boardFinalizer(board,d) takes a board
 with rank d and entries the image 
 of addition (Z_nxZ_n)x(Z_nxZ_n)
 and converts the entries in a well-
 defined way to elements of 
 {1,2,..,n^2}
###############################################
################################################


