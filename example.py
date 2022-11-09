from adt import ADT

@ADT
class Tree:

    class Empty:
        pass

    class Leaf:
        item : int = None

    class Node:
        item : int = None
        lhs : 'Tree' = None
        rhs : 'Tree' = None

    @staticmethod
    def print_tree(n):
        match n:
            case Tree.Empty():
                print('Empty')
            case Tree.Leaf(item):
                print('Leaf:' + str(item))
            case Tree.Node(item, lhs, rhs):
                print('Node:' + str(item))
                print(' visiting lhs ')
                Tree.print_tree(lhs)
                print('Node:' + str(item))
                print(' visiting rhs ')
                Tree.print_tree(rhs)
            case _:
                print('No Match')

    def print_tree_2(self):
        match self:
            case Tree.Empty():
                print(self)
            case Tree.Leaf(_):
                print(self.item)
            case Tree.Node(item, lhs, rhs):
                print(self)
                print(' visiting lhs ')
                lhs.print_tree_2()
                print(self)
                print(' visiting rhs ')
                rhs.print_tree_2()
            case _:
                print('No Match')

class empty_2:
    pass

#register_as_adt_subclass( Tree, empty_2)

a = Tree.Empty()

b = Tree.Leaf(1)

c = Tree.Leaf(2)

d = Tree.Leaf(2)

print(a == b)

print(a == c)

print(c == d)

root = Tree.Node( 1, Tree.Node(3, a,c), Tree.Node(5, b,d))


Tree.print_tree( root)

root.print_tree_2()
