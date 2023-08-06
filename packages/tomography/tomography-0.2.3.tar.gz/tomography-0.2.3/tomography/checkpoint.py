class Checkpoint(object):

    def __init__(self, checker, handler):
        self.checker = checker
        self.handler = handler

    def check(self, frame, event, args):
        return self.checker(frame, event, args)

    def handle(self, frame, event, args):
        return self.handler(frame, event, args)
