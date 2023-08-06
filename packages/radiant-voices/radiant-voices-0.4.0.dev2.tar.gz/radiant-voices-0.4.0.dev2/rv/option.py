class Option:
    """Defines a boolean option attached to a module.

    Options are different from on/off controllers in that options cannot
    be changed during playback using the SunVox DLL.

    In Module classes, define controllers in the order they are
    enumerated in the SunVox file format, so they receive the correct index.
    """

    _next_order = 0

    name = None
    index = None

    def __init__(self, default, range=None, inverted=False):
        self.default = default
        self.range = range
        self.inverted = inverted
        self._order = Option._next_order
        Option._next_order += 1

    def __get__(self, instance, owner):
        value = instance.option_values[self.name]
        if self.inverted:
            return not value
        else:
            return value

    def __set__(self, instance, value):
        if self.range is None:
            value = bool(value)
            if self.inverted:
                value = not value
        else:
            value = max(self.range[0], min(self.range[1], value))
        instance.option_values[self.name] = value
        callback = getattr(instance, 'on_{}_changed'.format(self.name), None)
        if callable(callback):
            callback(value)
