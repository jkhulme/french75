class Sink:

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            pass
        return _missing
