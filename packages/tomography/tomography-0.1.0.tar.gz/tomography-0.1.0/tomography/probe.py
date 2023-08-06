import sys

from tomography.recorder import Recorder
from tomography.observer import Observer


class Probe(object):

    def __init__(self):
        self.recorder = Recorder()
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

    def observe(self, token, accessor):
        self.observers.append(Observer(self, token, accessor))
        return self

    def evaluate_observers(self, frame):
        for observer in self.observers:
            observer.evaluate(frame)

    def on_trace(self, frame, event, args):
        self.evaluate_observers(frame)
        if event == 'call':
            for context in self.contexts:
                if context.equals(frame):
                    context.on_enter(frame, event, args)
                    return context.make_tracer(self)
        else:
            return self.on_trace

    def __del__(self):
        self.stop()
