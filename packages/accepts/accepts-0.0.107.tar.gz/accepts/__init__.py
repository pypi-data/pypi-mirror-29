#!/usr/bin/env python
from objectname import objectname
from public import public
from tolist import tolist


def err_msg(func, args, pos, required_types):
    name = objectname(func, fullname=True)
    lines = [
        "%s() argument #%s is not instance of %s" %
        (name, pos, required_types)]
    lines += ["args: %s" % str(list(args))]
    lines += ["arg#%s: %s" % (pos, args[pos])]
    msg = "\n".join(lines)
    raise TypeError(msg)


@public
def accepts(*types):
    def check_accepts(f):
        # assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwargs):
            for pos, (arg, required_types) in enumerate(zip(args, types), 0):
                # isinstance() arg 2 must be a type or tuple of types
                # fix: type(None)
                if not isinstance(arg, required_types):
                    msg = err_msg(f, args, pos, required_types)
                    raise TypeError(msg)
            return f(*args, **kwargs)
        try:  # python2
            new_f.func_name = f.func_name
        except AttributeError:  # python3
            new_f.__name__ = f.__name__
        return new_f
    return check_accepts
