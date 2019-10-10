class Broadcaster(object):

    _events = {}

    def event(self, e, *args):
        # TODO: catch exception, but... they are needed
        # The game terminates its execution with an exception and the exception is fired in the board.py file
        # during a callback invoked within this even notifier.
        # A solution could be: change the listen method in order to accept a callbackException, called in case
        # of exception with the proper object and catch all unintended exceptions.

        cs = self._events.get(e) if self._events.get(e) is not None else []
        for c in cs:
            c(args)

    def listen(self, to, callback):
        if self._events.get(to) is None:
            d = {to: [callback]}
        else:
            callbacks = self._events.get(to).copy()
            callbacks.append(callback)
            d = {to: callbacks}
        self._events.update(d)


broadcaster = Broadcaster()
