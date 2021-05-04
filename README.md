# Functional Completeness Checker
This program checks a set of propositional logic operators for functional completeness, there are a set of operators here by default, but additional ones can be specified by the user.


## Setting the program up
The program can be run directly from the command line. Before running the program, you will need to install the module TatSu if you do not already have it, this can be done by running the command:

`pip install tatsu`

When you have done this, to check that the program has downloaded correctly, run the command:

`python funccomp.py -h`

This should return the following:

![Help Message. The top row should state "usage: funccomp.py" (-h) {lv,add,fc,reset} ..."](https://user-images.githubusercontent.com/25661481/117032439-6538fd80-acf9-11eb-913e-2f97e41d4050.png)


---
## Commands the program can be issued
The program has four modes of operation: Listing the operators stored in the table, Adding a new operator to the table, Resetting the table of operators, and Checking a set of operators for functional completeness.

The List Operators – “lv” – and Reset Table – “reset” – commands take no mandatory arguments, so can be ran by the commands:

`python funccomp.py lv`

and

`python funccomp.py reset`

The Add Operator command takes two mandatory arguments, the name of the operator and the formula of the operator (formatted as detailed in the section below). If the name, or formula you are specifying involve a dash “-”, then put these in quotation marks or the command prompt will not run the command. The format of this command is:

`python funccomp.py add <name> <formula>`
  
The Check Functional Completeness command requires at least one argument but can take as many as you require. These are the names of all of the operators in the set that you would like to check for functional completeness separated by spaces, again if any of these names involve a dash then put them in quotation marks. The format of this command is:

`python funccomp.py fc <operator 1> <operator 2> ... <operator n>`
 
 ---
## Specifying Formulas for Operators correctly
The grammar used to interpret logical formulas operates on the following rules:

- Variables must be in the format: `xi`, where `i` is an integer.
- The logical values for true and false are represented by 1 and 0, respectively.
- The operators that can be used in formulas are and, or, not, implication and bi-implication.
- The binary operators require brackets around the formula and should have spaces in between each side and the operator.
- The not operator does not require brackets if it is being applied to a single variable, but if it is being applied to a whole formula, then it, and the formula must be contained in brackets.
- The outer-most layer of the formula does not need to be in brackets.

Examples of valid formulas are the following:
-	`x1 v x2`
-	`(x1 -> x2) ^ (!x1 -> x3)`
-	`!(x1 -> x2)`
- `((!(x1 <-> x2)) v (!(x1 <-> x3))) v (!(x2 <-> x3))`

If you are having trouble defining an operator, I would recommend specifying it with every operator contained in brackets and removing the outermost layer at the end. The grammar works best when specifying pairs of operators, so if there is a version of your formula that is specified in pairs of variable I would try to use that here.
