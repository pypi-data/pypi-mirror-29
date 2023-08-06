class StreamProcessor(object):

    def __init__(self, function):
        self.function = function

    def process(self, **kwargs):
        return self.function(**kwargs)
