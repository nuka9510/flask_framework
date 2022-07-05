from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        super(RegexConverter, self).__init__(map, *args)
        self.regex = args[0]