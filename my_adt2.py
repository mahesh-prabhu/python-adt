import dataclasses
import inspect
import copy

#
# ADT class decorator should do the below.
#
# 0. Make each subclass definition a data-class.
# 1. Make top class uninstantiatable. -- Not sure how to do this? Over-ride init? Make the top class an abstract base class (using abc python module) ?
# 2. Top class should not have any members other than class definitions? Not sure how to achieve this?
# 3. Add dynamic type checking into the sub-class constructors.
# 4. Note: Looks like we can't call the constructors of other subclasses even though they are defined. This is not allowed by python compiler, which might be a good thing.

# def __my_eq__( self, other):
#     self_istype  = (isinstance(self,type))
#     other_istype = (isinstance(self,type))

#     if ( self_istype and other_istype):
#         return ( self.__orig__eq(other))

def _get_nested_class_defs(cls):
    for k, v in vars(cls).items():
        if inspect.isclass(v):
            yield k, v
            #print(k)

def deepcopy_subcls(cls, new_subcls_name, subcls_handle):
    #
    # Prepare bases and force the top class to be a parent of the subclass
    #
    child_bases = inspect.getmro(subcls_handle)
    parent_bases = inspect.getmro(cls)
    bases = tuple([item for item in parent_bases if item not in child_bases]) + child_bases
    copy_subcls = type(new_subcls_name, bases, dict(subcls_handle.__dict__))
    #
    # deepcopy attrs that are mutable
    #
    for name, attr in subcls_handle.__dict__.items():
        try:
            hash(attr)
            # todo: what about attributes that are non-mutable/hashable?
        except TypeError:
            # Assume lack of __hash__ implies mutability. This is NOT
            # a bullet proof assumption but good in many cases.
            setattr(copy_subcls, name, copy.deepcopy(attr))
    return copy_subcls
            
def register_as_adt_subclass( cls, subcls_handle):
    #
    # todo: Typechecks on subclass, ex. should have type annotation?
    #
    new_subcls_name = cls.__name__ + '.' + subcls_handle.__name__
    new_subcls_handle = deepcopy_subcls( cls, new_subcls_name, subcls_handle)
    #
    # Make a dataclass out of the new subclass
    #
    new_subcls_handle = dataclasses.dataclass()(new_subcls_handle)
    #
    # replace existing subclass handle with new handle
    #
    setattr(cls, subcls_handle.__name__, new_subcls_handle)
    return

def ADT(cls):
    """
    A class decorator that converts a class into a algebraic-data-type/sumtype.
    """
    
    #
    # todo: Typechecks on parent class. ex.no members allowed.
    #
    for subcls_name, subcls_handle in _get_nested_class_defs(cls):
        register_as_adt_subclass( cls, subcls_handle)
    return cls
        
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

register_as_adt_subclass( Tree, empty_2)

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
