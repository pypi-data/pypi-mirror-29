

def get_parameters(f, ignore_self=True):
    """Given a function f, return a list of variable names"""

    params = f.__code__.co_varnames

    if ignore_self:
        return tuple(p for p in params if p != 'self')

    return tuple(params)
