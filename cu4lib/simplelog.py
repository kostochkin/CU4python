import sys


class EmptyLogger:
    def debug(self, *args):
        pass
    
    def warn(self, *args):
        pass
    
    def info(self, *args):
        pass

    def error(self, *args):
        pass


class StdioLogger:
    """ Simple logger

        Constructor parameters
            take : int
                Truncate log record to corresponding size

    """
    def __init__(self, take=None):
        self._strip = take

    def debug(self, *args):
        self._print(sys.stdout, "DEBUG", *args)
    
    def warn(self, *args):
        self._print(sys.stderr, "WARN", *args)
    
    def error(self, *args):
        self._print(sys.stderr, "ERROR", *args)

    def info(self, *args):
        self._print(sys.stdout, "INFO", *args)

    def _print(self, file, type, *args):
        print("[{}]".format(type), *self._strip_all(args), sep=" ", file=file)

    def _strip_all(self, args):
        if self._strip is None:
            return args
        else:
            return list(map(self._strip_one, args))
    
    def _strip_one(self, arg):
        if type(arg) == bytes and len(arg) > self._strip:
            return arg[:self._strip] + b' <<<stripped'
        elif type(arg) == str and len(arg) > self._strip:
            return arg[:self._strip] + ' <<<stripped'
        return arg


class StdioErrorLogger(StdioLogger):
    def debug(self, *args):
        pass
    
    def warn(self, *args):
        pass
    
    def error(self, *args):
        self._print(sys.stderr, "ERROR", *args)

    def info(self, *args):
        pass


