import sys

class StdioLogger:
    def debug(self, *args):
        print("[DEBUG]", *args, sep=" ", file=sys.stdout)
    
    def warn(self, *args):
        print("[WARN]", *args, sep=" ", file=sys.stderr)
    
    def error(self, *args):
        print("[ERROR]", *args, sep=" ", file=sys.stderr)

    def info(self, *args):
        print("[info]", *args, sep=" ", file=sys.stderr)

