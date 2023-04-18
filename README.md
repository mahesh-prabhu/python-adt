# python-adt
An implementation of Algebraic Data Type (ADT) in Python.

## What is an Algebraic Data Types(ADT) ?
ADTs are a type of composite data type that combine the features of union and enum data types. They are a very popular data type in functional programming languages.     
   
To better understand ADTs, lets first look at what union and enum data types offer.
A union allows you to capture different data types within a single type. An instance of the union will be an object of exactly one of the list of data types defined in the union. An enum allows you to define a set of named values, typically the values being integers. An ADT enables you to combine both of these features, i.e you can define a set of named data types. An instance of the ADT will be an object of exactly one of the named data types defined in the ADT.    

ADTs allow you to quickly and concisely define rich data structues. ADTs make the relationship between related data types self evident. The behaviors of the ADT objects can then be defined using pattern matching. Most functional programming languages come built in with pattern matching. Thankfully for us Pattern matching was introduced in python 3.10 in October'21.    

## Python based ADT

### Example

Let's look at python ADTs by working through an example of a tree data-structure. We'll define our tree data-structure to have three types of nodes; empty nodes, leaf nodes and intermediate nodes. The empty node does not have any value inside it, the leaf node has an item and the intermediate node has an item, and in addition has left and a right child 'pointer' inside it.

We can define this tree type as an ADT in python as below

```
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

```

Each of the member types of an ADT are defined as a [dataclass](https://docs.python.org/3/library/dataclasses.html), so we can use all the facilities provided by a dataclass like object initialization, equality checking and printing.

Let's create a root node with two leaf nodes of type *Tree* ADT.   

```
>>> root = Tree.Node( 1, Tree.Leaf(3), Tree.Leaf(5))
```

The newly created *root* is of type *Tree* and of type *Tree.Node*. Hence the members of ADT are polymorphic.    

```
>>> isinstance(root, Tree)
True
>>> isinstance(root, Tree.Node)
True
>>> isinstance(root, Tree.Leaf)
False
>>> isinstance(root, Tree.Empty)
False
```

In addition since our ADT is a class type we can define class methods.     

Below we extend our example *Tree* ADT with a class method and a static method for in order traversal of the tree. We also use pattern matching to define behavior.

```
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
```

Let's again create a new tree object.    

```
>>> # Creating an empty tree node
tree_empty = Tree.Empty()

# Create a leaf node with value 1
tree_leaf1 = Tree.Leaf(1)

# Create a leaf node with value 2
tree_leaf2 = Tree.Leaf(2)

# Create another leaf node with value 2
tree_leaf3 = Tree.Leaf(2)
>>> root = Tree.Node( 1, Tree.Node(3, tree_empty,tree_leaf2), Tree.Node(5, tree_leaf1,tree_leaf3))
```

Now, we can use our static class method.    

```
>>> Tree.print_tree_static_meth( root)
Node:1
 visiting lhs 
Node:3
 visiting lhs 
Empty
Node:3
 visiting rhs 
Leaf:2
Node:1
 visiting rhs 
Node:5
 visiting lhs 
Leaf:1
Node:5
 visiting rhs 
Leaf:2
```

We can also use our class method.    
```
>>> root.print_tree_class_meth()
Tree.Node(item=1, lhs=Tree.Node(item=3, lhs=Tree.Empty(), rhs=Tree.Leaf(item=2)), rhs=Tree.Node(item=5, lhs=Tree.Leaf(item=1), rhs=Tree.Leaf(item=2)))
 visiting lhs 
Tree.Node(item=3, lhs=Tree.Empty(), rhs=Tree.Leaf(item=2))
 visiting lhs 
Tree.Empty()
Tree.Node(item=3, lhs=Tree.Empty(), rhs=Tree.Leaf(item=2))
 visiting rhs 
2
Tree.Node(item=1, lhs=Tree.Node(item=3, lhs=Tree.Empty(), rhs=Tree.Leaf(item=2)), rhs=Tree.Node(item=5, lhs=Tree.Leaf(item=1), rhs=Tree.Leaf(item=2)))
 visiting rhs 
Tree.Node(item=5, lhs=Tree.Leaf(item=1), rhs=Tree.Leaf(item=2))
 visiting lhs 
1
Tree.Node(item=5, lhs=Tree.Leaf(item=1), rhs=Tree.Leaf(item=2))
 visiting rhs 
2
```

As mentioned earlier ADTs being dataclass under the hood, also support equality function.

```
>>> tree_empty == tree_leaf1
False
>>> tree_leaf1 == tree_leaf2
False
>>> tree_leaf2 == tree_leaf3
True

```

Equality applies for more complex ADT definitions as well. For our *Tree* example let's check equality on different tree structures.

```
>>> root1 = Tree.Node( 1, Tree.Leaf(3), Tree.Leaf(5))
>>> root2 = Tree.Node( 1, Tree.Leaf(3), Tree.Leaf(5))
>>> root3 = Tree.Node( 1, Tree.Leaf(3), Tree.Node(5, Tree.Empty(), Tree.Leaf(6)))
>>> root1 == root2
True
>>> root1 == root3
False
```

