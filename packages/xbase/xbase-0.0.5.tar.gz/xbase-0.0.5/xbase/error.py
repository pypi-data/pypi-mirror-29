def xassert(expr, *args, **kwargs):
    if not expr:
        assert False
    return expr


def xthrow(err, *args, **kwargs):
    raise err
