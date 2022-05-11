import sys
from dataclasses import dataclass

#import attr

PY3 = sys.version_info[0] == 3

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest


class _Constructor(object):
    def __init__(self, attrs):
        self._attrs = attrs


def constructor(*attrnames, **attribs):
    """
    Register a constructor for the parent sum type.
    Note that ``*attrnames`` and ``**attribs`` are mutually exclusive.
    :param attrnames: each argument should be either a simple string indicating
        the name of an attribute
    :param attribs: variables specified with `attr.ib`_ instances, from the
        `attrs package`_.
    .. _`attr.ib`:
       http://attrs.readthedocs.org/en/stable/api.html#attr.ib
    """
    if attribs and attrnames:
        raise TypeError(
            "Can't mix positional and keyword arguments in constructors")
    if attribs:
        # named args
        attrs = sorted(list(attribs.items()), key=lambda item: item[1].counter)
    else:
        # Positional args
        #attrs = [(name, attr.ib()) for name in attrnames]
        attrs = [(name, None) for name in attrnames]
        print("Error. Haven't fixed this. Hacked in arbitrary values above.")
    return _Constructor(attrs)


def _cmp_iterators(i1, i2):
    sentinal = object()
    return all(a == b for a, b in izip_longest(i1, i2, fillvalue=sentinal))


def _get_attrs(obj):
    return (getattr(obj, attr[0]) for attr in obj._sumtype_attribs)


def _get_constructors(klass):
    for k, v in vars(klass).items():
        if type(v) is _Constructor:
            yield k, v


def sumtype(*args, **kwargs):
    """
    A class decorator that treats the class like a sum type.
    Constructors should be wrapped/decorated with :obj:`constructor`.
    Note that this will overwrite ``__repr__``, ``__eq__``, and ``__ne__`` on
    your objects. ``__init__`` is untouched, but it would be kind of weird to
    make something a sum type *and* have an ``__init__``, so I recommend
    against that.
    """
    if len(args) == 1 and len(kwargs) == 0 and type(args[0] is type):
        return _real_decorator(args[0], {})
    else:
        return lambda klass: _real_decorator(klass, kwargs)


def _real_decorator(klass, kwargs):
    constructor_names = []
    for cname, constructor in _get_constructors(klass):
        new_constructor = _make_constructor(
            cname, klass, constructor._attrs, kwargs
        )
        setattr(klass, cname, new_constructor)
        constructor_names.append(cname)
    klass._sumtype_constructor_names = constructor_names
    return klass


def _make_constructor(name, type_, attrs, kwargs):
    """Create a type specific to the constructor."""
    d = dict(attrs)
    d['_sumtype_attribs'] = [x for x in attrs]
    print(d)
    t = type(name, (type_,), d)
    #t = attr.s(t, repr_ns=type_.__name__, **kwargs)
    t = (dataclass(init=True, repr=True, eq=True, frozen=True))(t)
    print(t)
    return t


#### testing ####

@sumtype
class MyType(object):
    # constructors specify names for their arguments
    MyConstructor = constructor('x')
    AnotherConstructor = constructor('x', 'y')
