from tomography.checkpoint import Checkpoint


class Context(object):

    def __init__(self,
                 file_name,
                 code_name,
                 on_enter=lambda frame, event, args: None,
                 on_leave=lambda frame, event, args: None):
        self.file_name = file_name
        self.code_name = code_name
        self.on_enter = on_enter
        self.on_leave = on_leave

        self.validators = []
        self.checkpoints = []

    def add_validator(self, validator):
        self.validators.append(validator)
        return self

    def add_checkpoint(self, checker, handler):
        self.checkpoints.append(Checkpoint(checker, handler))
        return self

    def equals(self, frame, event, args):
        if frame.f_code.co_filename.endswith(self.file_name) and \
                frame.f_code.co_name == self.code_name:
            for validator in self.validators:
                if not validator(frame, event, args):
                    return False
            return True
        return False

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
