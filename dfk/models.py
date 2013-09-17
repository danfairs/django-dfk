

class DeferredForeignKey(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', None)
        self.args = args
        self.kwargs = kwargs
