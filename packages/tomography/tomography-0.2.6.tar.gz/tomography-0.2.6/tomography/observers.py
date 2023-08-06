import traceback

from collections import namedtuple


Change = namedtuple('Change', [
    'older_value',
    'newer_value',
    'file_name',
    'line_no',
    'code_name',
    'stack'
])


class ChangeTracer(object):

    def __init__(self, accessor, recorder):
        self.accessor = accessor
        self.recorder = recorder

        self.older_value = accessor()

        self.previous_file_name = None
        self.previous_line_no = None
        self.previous_code_name = None
        self.previous_stack = None

    def __call__(self, frame, event, args):
        newer_value = self.accessor()

        if newer_value != self.older_value:
            self.recorder(Change(
                self.older_value,
                newer_value,
                self.previous_file_name,
                self.previous_line_no,
                self.previous_code_name,
                self.previous_stack
            ))
            self.older_value = newer_value

        self.previous_file_name = frame.f_code.co_filename
        self.previous_line_no = frame.f_lineno
        self.previous_code_name = frame.f_code.co_name
        self.previous_stack = traceback.format_stack(frame)


Error = namedtuple('Error', [
    'exception',
    'value',
    'traceback',
])


class ErrorCapturer(object):

    def __init__(self, exc_types, recorder):
        self.exc_types = exc_types
        self.recorder = recorder

    def __call__(self, frame, event, args):
        if event == 'exception':
            exception, value, traceback = args
            if isinstance(value, self.exc_types):
                self.recorder(Error(exception, value, traceback))
