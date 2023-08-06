from functools import wraps


class presume:

    def __init__(self, exception, action, args):

        self.e = exception
        self.action = action
        self.args = args

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except self.e:
                self.action(*self.args)
                raise self.e from None

        return wrapper

