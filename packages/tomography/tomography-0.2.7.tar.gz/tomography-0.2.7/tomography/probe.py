import sys


class Probe(object):

    def __init__(self):
        self.contexts = []
        self.observers = []

    def start(self):
        sys.settrace(self.on_trace)
        return self

    def stop(self):
        sys.settrace(None)
        return self

    def add_context(self, context):
        self.contexts.append(context)
        return self

    def add_observer(self, observer):
        self.observers.append(observer)
        return self

    def evaluate(self, frame, event, args):
        cancel_list = []
        for observer in self.observers:
            if observer(frame, event, args):
                cancel_list.append(observer)
        for observer in cancel_list:
            self.observers.remove(observer)

    def on_trace(self, frame, event, args):
        self.evaluate(frame, event, args)
        if event == 'call':
            for context in self.contexts:
                if context.equals(frame, event, args):
                    context.on_enter(frame, event, args)
                    return context.make_tracer(self)
        return self.on_trace

    def __del__(self):
        self.stop()
