
class DeferredForeignKey(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
