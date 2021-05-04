import checkfunc,parsers,logictables

from codecs import open
from pprint import pprint
import json

import tatsu
from tatsu.ast import AST
import os
import argparse

def list_values(args,juncList):
    # prints the names of all the operators in the table and their formulas
    print("{0:16s} {1}".format('NAME','FORMULA'))
    for i in range(0,len(juncList)):
        print("{name:16s} {formula}".format(**juncList[i]))

def add_operator(args,juncList):
    grammar = open('grammar/logic.ebnf').read()
    # Check to see if the name being added already exists
    identical = False
    for junctor in juncList:
        if args.name == junctor["name"]:
            identical = True
            break
    
    invalid = checkfunc.test_new_junctor(args.formula,grammar)

    # Make sure we only add the formula if its actually valid.
    if invalid == True:
        print("The formula you have entered is invalid.")
        print("Make sure you have put spaces between any variables and operators, and that you have")
        print("between 1 and 5 operators. Check the README for more examples of valid formulas.")
    elif identical == True:
        print("The name of the operator you have entered already exists.")
        print("Try a different name.")
        print("To view a list of the operators already in the program, use the command 'python funccomp.py lv'.")
    else:
        newJunctor = checkfunc.create_new_junctor(args.name,args.formula,grammar)

        checkfunc.add_new_junctor(newJunctor)
    
        print("Successfully added the operator '{0}' with formula '{1}' to the table.".format(args.name,args.formula))
        print("To view a list of operators in the program, use the command 'python funccomp.py lv'.")

def func_complete(args,juncList):
    listToCheck = []
    # Check to see if every operator actually exists.
    for i in range(0,len(args.operators)):
        for j in range(0,len(juncList)):
            if args.operators[i] == juncList[j]["name"]:
                listToCheck.append(juncList[j])
                break
    if len(listToCheck) != len(args.operators):
        print("One or more of the operators you have entered doesn't seem to exist.")
        print("Check that you've spelt the names correctly, then try again.")
        print("To view a list of operators in the program, use the command 'python funccomp.py lv'.")
    else:
        output = checkfunc.check_functionally_complete(listToCheck)
        if sum(output) > 0:
           # Get the failed classes into a string because I need it for both
            failedClasses = ""
            for i in range(0,5):
                if output[i]:
                    failedClasses = failedClasses+" "+str(i+1)+","
            failedClasses = failedClasses[:-1]
             # Let the user choose if they want a more detailed explaination.
            if args.exp:
                for i in range(0,len(listToCheck)):
                    # Makes the output for each operator look nice.
                    out = ""
                    for j in range(0,5):
                        if (listToCheck[i]["truthClasses"][j]):
                            out = out+" "+str(j+1)+","
                    out = out[:-1]
                    print("The operator {name} is part of class(es)".format(**listToCheck[i])+out+".")
                
                print("Every operator in the set is part of class(es){0}.".format(failedClasses))
                print("Therefore, the set is not functionally complete.\n")
            else:
                print("The set {0} is not functionally complete.\n".format(args.operators))
            
            newJuncs = checkfunc.find_operators_for_functional_complete(output,juncList)
            if not newJuncs:
                print("Unfortunately, there are no operators stored in the system that will make this functionally complete on their own.")
            else:
                print("The following operators will make the set functionally complete:")
                for junctor in newJuncs:
                    print("{name:16s} ({formula})".format(**junctor))
                if args.exp:
                    print("As they are not part of the class(es){0}.".format(failedClasses))
            
        else:
            if args.exp:
                for i in range(0,len(listToCheck)):
                    # Makes the output for each operator look nice.
                    out = ""
                    for j in range(0,5):
                        if (listToCheck[i]["truthClasses"][j]):
                            out = out+" "+str(j+1)+","
                    out = out[:-1]
                    print("The operator {name} is part of class(es)".format(**listToCheck[i])+out+".")
                print("For each truth class, one or more operators in the set are not part of it.")
                print("Therefore, the set is functionally complete.")
            else:
                print("The set {0} is functionally complete.".format(args.operators))
            
def reset_statements(args,juncList):
    junc0 = '{"name": "false", "formula": "0", "noVars": 0, "inputVals": [], "truthVals": [false], "truthClasses": [false, true, true, true, false]}\n'
    junc1 = '{"name": "true", "formula": "1", "noVars": 0, "inputVals": [], "truthVals": [true], "truthClasses": [true, false, true, true, false]}\n'
    file = open("statements.txt", "w")
    file.write(junc0+junc1)
    file.close()
    oPL = [["or","x1 v x2"],["and","x1 ^ x2"],["not", "!x1"],["implication","x1 -> x2"],["bi-implication","x1 <-> x2"]]
    grammar = open('grammar/logic.ebnf').read()

    for operator in oPL:
        junc = checkfunc.create_new_junctor(operator[0],operator[1],grammar)
        checkfunc.add_new_junctor(junc)

    print("Successfully Reset the Operator File!")  


def setup_args():
    # Create the Top-Level Parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Pick which functionality you would like the program to use.')

    #Create the Parser for 'List Values'
    parser_list_values = subparsers.add_parser('lv', help='Lists all the formulas currently stored.')
    parser_list_values.set_defaults(func=list_values)

    #Create the parser for 'add value'
    parser_add_value = subparsers.add_parser('add',help='Add a new operator')
    parser_add_value.add_argument('name',help='The name of the operator to add.')
    parser_add_value.add_argument('formula',
    help='The formula of the operator to add. Put this in quote ("") marks, or the program will not recognise it.')
    parser_add_value.set_defaults(func=add_operator)

    #Create the parser for 'check functional completness'
    parser_functional = subparsers.add_parser('fc',help='Checks a set of operators to see if they are functionally complete.')
    parser_functional.add_argument('operators', nargs='+',help='The names of each of the operators you wish to check, separated by spaces.')
    parser_functional.add_argument('--exp','-e',action='store_true',help='Pass this for a more detailed explaination.')
    parser_functional.set_defaults(func=func_complete)

    parser_reset = subparsers.add_parser('reset',help='Reset the Operators file to its original state. Can not be undone!')
    parser_reset.set_defaults(func=reset_statements)

    args = parser.parse_args()
    return args

def main():
    args = setup_args()
    # Check if the file with the operators has been deleted or is empty
    noOps = True
    if not (os.path.isfile('statements.txt')):
        print("The file containing the operators has been deleted.")
        noOps = False
    elif os.stat('statements.txt').st_size == 0:
        print("The file containing the operators is empty.")
        noOps = False
    
    if noOps == False:
        resetFile = input("Would you like to reset the operator file? (Y/N)\n").upper()
        if resetFile == "Y":
            reset_statements("args","juncList")
    
    # Set up the operator database    
    juncList = checkfunc.setup_junctors()

    # Calls the function required for the functionality requested.
    args.func(args,juncList)

if __name__ == '__main__':
    main()
