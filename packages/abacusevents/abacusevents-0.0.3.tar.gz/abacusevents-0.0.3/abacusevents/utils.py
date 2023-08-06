import os


def env(variable: str, default=None):
    return os.environ.get(variable, default)


def curry(fn):
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= fn.__code__.co_argcount:
            return fn(*args, **kwargs)
        return (lambda *args2, **kwargs2:
                curried(*(args + args2), **dict(kwargs, **kwargs2)))
    return curried


class singleton:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


def lowercase_first(string: str) -> str:
    return string[:1].lower() + string[1:] if type(string) == str else ''
