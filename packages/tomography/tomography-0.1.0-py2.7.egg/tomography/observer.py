import traceback


class Observer(object):

    def __init__(self, probe, token, accessor):
        self.probe = probe
        self.token = token
        self.accessor = accessor
        self.current_value = self.accessor()
        self.previous_file_name = None
        self.previous_line_no = None
        self.previous_code_name = None
        self.previous_stack = None

    def evaluate(self, frame):
        newer_value = self.accessor()
        evaluation = newer_value == self.current_value

        if not evaluation:
            self.probe.recorder.record_change(
                self.token,
                self.current_value,
                newer_value,
                self.previous_file_name,
                self.previous_line_no,
                self.previous_code_name,
                self.previous_stack
            )
            self.current_value = newer_value

        self.previous_file_name = frame.f_code.co_filename
        self.previous_line_no = frame.f_lineno
        self.previous_code_name = frame.f_code.co_name
        self.previous_stack = traceback.format_stack(frame)

        return evaluation
