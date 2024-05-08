# copied from Python 2.7 source code as plone testing uses __bases__
def _searchbases(cls, accum):
    # Simulate the "classic class" search order.
    if cls in accum:
        return
    accum.append(cls)
    for base in cls.__bases__:
        _searchbases(base, accum)


def getmro(cls):
    """Return tuple of base classes in method resolution order."""
    if hasattr(cls, "__mro__"):
        return cls.__mro__
    else:
        result = []
        _searchbases(cls, result)
        return tuple(result)
