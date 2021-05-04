class LogicSemantics(object):
    # This will return the truth value of a given logical statement
    def factor(self,ast):
        return bool(int(ast.atom))

    def variable(self,ast):
        # FOR NOW JUST RETURN FALSE
        return False

    def subexpression(self,ast):
        return bool(int(ast.sub))

    def _and(self,ast):
        return ast.left and ast.right

    def _or(self,ast):
        return ast.left or ast.right
    
    def _not(self,ast):
        return not(ast.atom)

    def _inter(self,ast):
        return (not(ast.left) or ast.right)

    def _biinter(self,ast):
        if ast.left == ast.right:
            return True
        else:
            return False

class VarCounter(object):
    # This returns an array containing all the variables in the logical statement
    def __init__(self):
        self.vars = []

    def variable(self,ast):
        if ast.atom not in self.vars:
            self.vars.append(ast.atom)
        return ast

    def expression(self,ast):
        return self.vars