from pynput.keyboard import Listener, KeyCode


class KeyboardManager(object):
    _callbacks = {}
    _listener = None

    def __init__(self):
        pass
        self._listener = Listener(on_press=self._on_press)
        self._listener.start()

    def _on_press(self, key):
        if isinstance(key, KeyCode):
            key = key.char
        self._execute(key)

    def _execute(self, key):
        callback = self._callbacks.get(key)
        if callback is None:
            return
        try:
            callback()
        except:
            # catch-all for keyboard reactions
            pass

    def register(self, key, callback):
        """
        Register the callback 'callback' on the key 'key'.
        """
        if isinstance(key, list):
            map(lambda k: self._callbacks.update({k: callback}), key)
        else:
            self._callbacks.update({key: callback})


class KeyboardBuffer:
    _buffer = []

    def bufferize(self, key):
        """
        Bufferize the key 'key'.
        """
        self._buffer.insert(0, key)

    def next(self):
        """
        :return: The next buffered key.
        """
        if len(self._buffer) == 0:
            return None
        return self._buffer.pop()


keyboardManager = KeyboardManager()
keyboardBuffer = KeyboardBuffer()
