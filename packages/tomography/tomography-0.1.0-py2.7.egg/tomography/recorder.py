from collections import namedtuple, defaultdict

Change = namedtuple('Change', [
    'older_value',
    'newer_value',
    'file_name',
    'line_no',
    'code_name',
    'stack',
])


class Recorder(object):

    def __init__(self):
        self.changes = defaultdict(lambda: [])

    def record_change(
        self,
        token,
        older_value,
        newer_value,
        file_name,
        line_no,
        code_name,
        stack
    ):
        self.changes[token].append(
            Change(
                older_value,
                newer_value,
                file_name,
                line_no,
                code_name,
                stack
            )
        )
