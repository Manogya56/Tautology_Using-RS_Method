# Enter the input in variables of either a,b,c,d,p,q,r,s
# For operations like 'and' use &
# For operations like 'or' use |
# For operations like '->' use >>
# For operations like 'not' use ~
# For operations like <-> use <<


class Expression:
    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)

    def __lshift__(self, other):
        return Iff(self, other)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.eq(other)

    def call_func(self, left, right):
        while True:
            found = True
            for item in left:
                if item in right:
                    return None
                if not isinstance(item, Variable):
                    left.remove(item)
                    tup = item._tleft(left, right)
                    left, right = tup[0]
                    if len(tup) > 1:
                        v = self.call_func(*tup[1])
                        if v is not None:
                            return v
                    found = False
                    break
            for item in right:
                if item in left:
                    return None
                if not isinstance(item, Variable):
                    right.remove(item)
                    tup = item._tright(left, right)
                    left, right = tup[0]
                    if len(tup) > 1:
                        v = self.call_func(*tup[1])
                        if v is not None:
                            return v
                    found = False
                    break
            if found:
                return "expression is not tautology"

    def _call_func(self):
        return self.call_func([], [self])


class Bin_Op(Expression):
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return '(' + str(self.left_child) + ' ' + self.op + ' ' + str(self.right_child) + ')'

    def eq(self, other):
        return self.left_child == other.left_child and self.right_child == other.right_child


class And(Bin_Op):
    op = '^'

    def _tleft(self, left, right):
        print("And function", self.left_child, self.right_child)
        return (left + [self.left_child, self.right_child], right),

    def _tright(self, left, right):
        print("And function", self.left_child, self.right_child)
        return (left, right + [self.left_child]), (left, right + [self.right_child])


class Implies(Bin_Op):
    op = '->'

    def _tleft(self, left, right):
        print("Implies function", self.left_child, self.right_child)
        return (left + [self.right_child], right), (left, right + [self.left_child])

    def _tright(self, left, right):
        print("Implies function", self.left_child, self.right_child)
        return (left + [self.left_child], right + [self.right_child]),


class Iff(Bin_Op):
    op = '<->'

    def _tleft(self, left, right):
        print("Iff function", self.left_child, self.right_child)
        return (left + [self.left_child, self.right_child], right), (left, right + [self.left_child, self.right_child])

    def _tright(self, left, right):
        print("Iff function", self.left_child, self.right_child)
        return (left + [self.left_child], right + [self.right_child]), (left + [self.right_child], right + [self.left_child])


class Not(Expression):
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return '~' + str(self.child)

    def eq(self, other):
        return self.child == other.child

    def _tleft(self, left, right):
        return (left, right + [self.child]),

    def _tright(self, left, right):
        return (left + [self.child], right),


class Or(Bin_Op):
    op = 'V'

    def _tleft(self, left, right):
        print("Or function", self.left_child, self.right_child)
        return (left + [self.left_child], right), (left + [self.right_child], right)

    def _tright(self, left, right):
        print("Or function", self.left_child, self.right_child)
        return (left, right + [self.left_child, self.right_child]),


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    __repr__ = __str__

    def eq(self, other):
        return self.name == other.name


a = Variable('a')
b = Variable('b')
c = Variable('c')
d = Variable('d')
p = Variable('p')
q = Variable('q')
r = Variable('r')
s = Variable('s')

def rs_method(e):
    print("Formula: ", e)
    result = e._call_func()
    if result == None:
        print("Result: Expression is Tautology")
    else:
        print("Result: Expression is not a Tautology")


# input2 = 'a & b'
# input1 = '(a|b)|~b'
# input3 = "(((~a | (b >> p)) & (a | b)) >> b)"

inputString = input("Please enter the Propositional Formula:")

try:
    inputString = inputString.lower()
    e = eval(inputString)
    rs_method(e)
except NameError:
    print("Please enter the valid Propositional Formula!!!")
