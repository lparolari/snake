import keyboard


class KeyboardManager(object):
    _callbacks = {}

    def __init__(self):
        super().__init__()
        keyboard.on_press(self._on_press)

    def _on_press(self, key):
        self._execute(key.name)

    def _execute(self, key):
        try:
            callback = self._callbacks.get(key)
            if callback is None:
                return
            callback()
        except:
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
