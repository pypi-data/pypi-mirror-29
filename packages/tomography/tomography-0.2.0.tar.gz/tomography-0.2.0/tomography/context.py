from tomography.checkpoint import Checkpoint


class Context(object):

    def __init__(self,
                 file_name,
                 code_name,
                 enter_handler=lambda frame, event, args: None,
                 leave_handler=lambda frame, event, args: None):
        self.validators = []
        self.checkpoints = []

        self.file_name = file_name
        self.code_name = code_name
        self.enter_handler = enter_handler
        self.leave_hanlder = leave_handler

    def add_validator(self, validator):
        self.validators.append(validator)
        return self

    def add_checkpoint(self, checker, handler):
        self.checkpoints.append(Checkpoint(checker, handler))
        return self

    def equals(self, frame):
        if frame.f_code.co_filename.endswith(self.file_name) and \
                frame.f_code.co_name == self.code_name:
            for validator in self.validators:
                if not validator(frame):
                    return False
            return True
        return False

    def on_enter(self, frame, event, args):
        return self.enter_handler(frame, event, args)

    def on_leave(self, frame, event, args):
        return self.leave_hanlder(frame, event, args)

    def make_tracer(self, probe):
        def on_trace(frame, event, args):
            probe.evaluate(frame, event, args)
            for checkpoint in self.checkpoints:
                if checkpoint.check(frame, event, args):
                    checkpoint.handle(frame, event, args)
            if event == 'return':
                self.on_leave(frame, event, args)
            return on_trace
        return on_trace
