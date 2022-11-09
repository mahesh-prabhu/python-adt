import dataclasses
import inspect
import copy

def _get_nested_class_defs(cls):
    for k, v in vars(cls).items():
        if inspect.isclass(v):
            yield k, v

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
            # todo: what about attributes that are immutable/hashable?
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
        
