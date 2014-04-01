class Sink:

    """
    rpc server and client are initialised to this.  It prevents a need to check
    if the server and client have been initialised before every call.
    If they have not been initialised then this swallows the error
    """

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            pass
        return _missing
