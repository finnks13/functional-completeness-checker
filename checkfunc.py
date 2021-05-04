from codecs import open
from pprint import pprint
import json

import tatsu
from tatsu.ast import AST

import logictables
import parsers


def test_parse():
    grammar = open('grammar/logic.ebnf').read()

    parser = tatsu.compile(grammar)

    test = 'x1 -> (x2 v x3)'

    name = "tester"

    out = create_new_junctor(name,test,grammar)

    add_new_junctor(out)
    #juncList = setup_junctors()

    #print(check_functionally_complete([juncList[0],juncList[1]]))

def setup_junctors():
    # Loads the junctors stored in the text file and bungs them into a list
    file = open("statements.txt", "r")
    junctors = []
    for line in file:
        s = line.strip()
        junctors.append(json.loads(s))

    file.close()
    return junctors

def add_new_junctor(junctorToWrite):
    # Storing as a json string in a text file because its easy
    file = open("statements.txt", "a")
    toWrite = "{0}\n".format(json.dumps(junctorToWrite))
    file.write(toWrite)
    file.close()    

def create_new_junctor(inputName,inputStatement,grammar):
    # Returns the dictionary containing the info of a new junctor
    values = create_truth_table(inputStatement, grammar)
    
    newJunctor = {
        "name": inputName,
        "formula": inputStatement,
        "noVars": values[0],
        "inputVals": values[1],
        "truthVals": values[2],
    }

    conditions = check_truth_classes(newJunctor)

    newJunctor.update({"truthClasses": conditions})

    return newJunctor


def test_new_junctor(inputStatement,grammar):
    # Checks to see if a formula is valid.
    parser = tatsu.compile(grammar)
    try:
        parser.parse(inputStatement, semantics = parsers.VarCounter())
    except:
        return True
    
    return False

def check_functionally_complete(junctors):
    output = [True,True,True,True,True]
    for junctor in junctors:
        for i in range(0,5):
            if junctor["truthClasses"][i] == False:
                output[i] = False
    
    return output

def find_operators_for_functional_complete(classes,juncList):
    out = []
    for i in range(0,len(juncList)):
        # Finds an operator which can make the set functionally complete.
        for j in range(0,5):
            noCorrect = 0
            if classes[j] == True and juncList[i]["truthClasses"][j] == False:
                noCorrect += 1
            
            if noCorrect == sum(classes):
                out.append(juncList[i])
                break
        # Make sure we don't give too many examples.
        if len(out) >= 3:
            break
    return out

def create_truth_table(logicStatement,grammar):
    parser = tatsu.compile(grammar)
    # Get a table containing all the variables inside the given statement
    varTable = parser.parse(logicStatement, semantics = parsers.VarCounter())
    noVars = len(varTable)

    
    # Get a table of truth values to input to the truth table generator
    # These tables are hard-coded because it's quicker for what I need this to do
    if noVars == 1:
        inputValues = logictables.return1()
    elif noVars == 2:
        inputValues = logictables.return2()
    elif noVars == 3:
        inputValues = logictables.return3()
    elif noVars == 4:
        inputValues = logictables.return4()
    elif noVars == 5:
        inputValues = logictables.return5()
    else:
        inputValues = logictables.return1()

    tval = []
    for i in range(0, len(inputValues)):
        temp = logicStatement
        for j in range(0, noVars):
            # Replace the variables with 1s or 0s
            temp = temp.replace(str(varTable[j]), str(inputValues[i][j]))
        output = parser.parse(temp, semantics = parsers.LogicSemantics())
        tval.append(output)   

    return [noVars,inputValues,tval]

def check_truth_classes(operator):
    classes = []
    classes.append(check_closed_under_T(operator))
    classes.append(check_closed_under_F(operator))
    classes.append(check_counting_function(operator))
    classes.append(check_monotonic(operator))
    classes.append(check_self_dual(operator))
    return classes

def check_closed_under_T(operator): # Condition 1
    # The last line in the truth tables in this program is always the "all True" line for inputs
    # so I just need to return that last line for this to work   
    return bool(operator["truthVals"][-1])

def check_closed_under_F(operator): # Condition 2
    # The first line in the truth tables is always the "all False" line for inputs
    # since I want to see if this line remains false, I just invert the value here
    return not(bool(operator["truthVals"][0]))

def check_counting_function(operator): # Condition 3
    dummies = check_dummy_variables(operator)
    tVals = operator["truthVals"]
    iVals = operator["inputVals"]

    for j in range(0, len(dummies)):
        if dummies[j] == True:
            continue
        else:
            for i in range(0, len(iVals)):
                if iVals[i][j] == False:
                    # Check to see if the value we're going to check is valid
                    if pow(2, len(dummies) - (j+1)) <= len(iVals):
                        # We check to see if the truth values where the only difference
                        # is that the non-dummy variable we are checking has had its
                        # value changed. If this does not result in a change in the output
                        # then this condition fails.
                        if tVals[i] == tVals[i + pow(2, len(dummies) - (j+1))]:
                            return False
    return True

def check_monotonic(operator): # Condition 4
    # Returns False if there exists an output of False in the Truth Table where the
    # 'truthiness' of the input is greater than a position with an output of True
    tVals = operator["truthVals"]
    iVals = operator["inputVals"]
    lowSum = None

    # Sets lowSum to the 'truthiness' value of the first output that is True
    # Since we are iterating starting from the lowest truthiness value going to the
    # highest, we can then check to see if there are any False outputs for inputs
    # which have a lower truthiness value than lowSum.
    for i in range(0, len(tVals)):
        if lowSum is None:
            if tVals[i] == True:
                lowSum = sum(iVals[i])
        else:            
            if (sum(iVals[i]) > lowSum) and (tVals[i] == False):
                return False
    return True    

def check_self_dual(operator): # Condition 5
    # Get the list of truth values and reverse it
    vals = operator["truthVals"]
    rVals = vals[::-1]

    # Invert the truth values in the reversed list
    for i, element in enumerate(rVals):
         rVals[i] = not(bool(element))
    
    # Check if the inverted reversed list is the same as the regular list
    if (vals == rVals):
        return True
    else:
        return False

def check_dummy_variables(operator):
    dummies = []
    tVals = operator["truthVals"]
    iVals = operator["inputVals"]
    for i in range(0, len(iVals[0])):
        dummies.append(True)

    for j in range(0, len(dummies)):
        for i in range(0, len(iVals)):
            # If the variable we are checking is equal to False
            if iVals[i][j] == False:
                # Check to see if the value we're going to check is valid
                if pow(2, len(dummies) - (j+1)) <= len(iVals):
                    # Check to see if the outputs, where the only difference is
                    # that the value of the variable we are checking has changed to
                    # be True, are the same.
                    # If they are different, we know that the variable we are checking
                    # is not a dummy variable as it has an impact on the value of the output
                    if tVals[i] != tVals[i + pow(2, len(dummies) - (j+1))]:
                        dummies[j] = False
                        break

    return dummies

def main():
    test_parse()

if __name__ == "__main__":
    main()
