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

    #
    # We can have static methods on the parent type
    #
    @staticmethod
    def print_tree_static_meth(n):
        """
        In-order Tree traversal
        """
        #
        # We can use structural pattern matching to process the subtypes
        #
        match n:
            case Tree.Empty():
                print('Empty')
            case Tree.Leaf(item):
                print('Leaf:' + str(item))
            case Tree.Node(item, lhs, rhs):
                print('Node:' + str(item))
                print(' visiting lhs ')
                Tree.print_tree_static_meth(lhs)
                print('Node:' + str(item))
                print(' visiting rhs ')
                Tree.print_tree_static_meth(rhs)
            case _:
                print('No Match')

    #
    # We can also have class methods on the parent type
    #
    def print_tree_class_meth(self):
        """
        In-order Tree traversal
        """
        #
        # We can use structural pattern matching to process the subtypes
        #
        match self:
            case Tree.Empty():
                print(self)
            case Tree.Leaf(_):
                print(self.item)
            case Tree.Node(item, lhs, rhs):
                print(self)
                print(' visiting lhs ')
                lhs.print_tree_class_meth()
                print(self)
                print(' visiting rhs ')
                rhs.print_tree_class_meth()
            case _:
                print('No Match')

# Creating an empty tree node
tree_empty = Tree.Empty()

# Create a leaf node with value 1
tree_leaf1 = Tree.Leaf(1)

# Create a leaf node with value 2
tree_leaf2 = Tree.Leaf(2)

# Create another leaf node with value 2
tree_leaf3 = Tree.Leaf(2)

# Checking equality between an empty node and a leaf node.
# This is False
print(tree_empty == tree_leaf1)

# Checking equality between an empty node and another leaf node.
# This is False
print(tree_empty == tree_leaf2)

# Checking equality between two leaf nodes with the same value.
# This is True
print(tree_leaf2 == tree_leaf3)

# Checking equality between two leaf nodes with different values.
# This is False
print(tree_leaf1 == tree_leaf2)

# Create a Tree
root = Tree.Node( 1, Tree.Node(3, tree_empty,tree_leaf2), Tree.Node(5, tree_leaf1,tree_leaf3))

# Traverse the tree in-order and print it using static method
Tree.print_tree_static_meth( root)

# Traverse the tree in-order and print it using class method
root.print_tree_class_meth()
