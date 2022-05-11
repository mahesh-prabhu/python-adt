from adt import *


class haha:
    def __init__(self):
        self.a = 10

@adt
class Tree:
    EMPTY : Case[None]
    LEAF1 : Case[haha]
    LEAF2 : Case[int]
    NODE  : Case['Tree', 'Tree']
    #NODE : Case[namedtuple('NODE', 'lhs rhs')]

@adt
class Test:
    t1: Case[int]




a = Tree.EMPTY()
b = Tree.EMPTY()
c = Tree.LEAF2(2)
d = Tree.LEAF2(3)
e = Tree.LEAF2(4)
f = Tree.NODE(d,e)
g = Tree.NODE(c,f)
h = Tree.LEAF1(haha())

def handle_expression(e: Tree):
    def explore_tree(lhs: Tree, rhs:Tree):
        print('visiting lhs')
        handle_expression(lhs)
        print('visiting rhs')
        handle_expression(rhs)

    e.match(
        empty = lambda : (print("empty")),
        leaf  = lambda n: (print("leaf" + str(n))),
        node  = lambda lhs, rhs: (explore_tree(lhs, rhs))
    )

def print_match(item):
    match item:
        case (Tree.EMPTY()):
            print('Tree.EMPTY')
        case _:
            print('No match')
