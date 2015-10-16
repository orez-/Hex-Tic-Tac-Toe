class cached_property(object):
    """
    Decorate a class method to turn it into a cached, read-only
    property. Works by dynamically adding a value member that overrides
    the get method.

    **Warning:** Only works for read-only properties!

    Example::

        def very_expensive_function():
            print("called very_expensive_function")
            return 3.14159

        class MyClass(object):
            @cached_property
            def my_attribute(self):
                return very_expensive_function()

        >>> c = MyClass()
        >>> print(c.my_attribute)
        called very_expensive_function
        3.14159
        >>> print(c.my_attribute)
        3.14159
    """

    def __init__(self, fget):
        for name in ('__name__', '__module__', '__doc__'):
            setattr(self, name, getattr(fget, name))
        self._fget = fget

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__[self._fget.__name__] = self._fget(instance)
        return value
