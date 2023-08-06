"""
    Bind methods/properties to another objects method and properties.
"""
import ast
from PySide import QtGui
from widget_factory import get_widget_value, set_widget_value


def is_property(instance, property_name):
    """Return if the object has a class property of the given property_name."""
    try:
        return isinstance(getattr(instance.__class__, property_name), property)
    except (AttributeError, ValueError, TypeError):
        return False


class FunctionProxy(object):
    """FunctionProxy object gets the function and calls it at runtime.

    This class takes either a function name and method object

    Args:
        func (function/method/str): Function, Method, or function name
        obj (object): Object that the function name belongs to. Used by getattr(obj, func)(*args, **kwargs)
    """
    def __init__(self, func, obj=None):
        self.__name__ = "FunctionProxy"
        self.__doc__ = """Proxy for a function or method to later call getattr(func.__self__, func.__name__)
                          which allows monkey patching."""
        self.func = None
        self.obj = None

        if isinstance(func, FunctionProxy):
            self.func = func.func
            self.obj = func.obj
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            return

        elif callable(func):
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            if hasattr(func, "__self__"):
                # Try to get the method name to call the function later.
                try:
                    getattr(func.__self__, func.__name__)  # This is a weird issue maybe due to methods with "__name"?
                    if obj is None:
                        obj = func.__self__
                    func = func.__name__
                except AttributeError:
                    pass

        self.func = func
        self.obj = obj

    def get(self):
        """Return the value or function."""
        if self.obj is None:
            return self.func
        else:
            try:
                return getattr(self.obj, self.func)
            except AttributeError:
                return self.func

    def exists(self):
        """Return if a value or function exists"""
        return ((self.obj is not None and isinstance(self.func, str) and hasattr(self.obj, self.func)) or
                self.func is not None)

    def __call__(self, *args, **kwargs):
        """Return the value or call the function with the given arguments."""
        func = self.get()
        if callable(func):
            return func(*args, **kwargs)
        return func


def connect(widget, func, signal=None):
    """Connect a widgets change signal to a function."""
    def set_value(*args, **kwargs):
        val = get_widget_value(widget)
        func(val)

    # Set the given signal
    if signal is not None:
        signal.connect(set_value)
        return

    if isinstance(widget, QtGui.QAbstractButton):
        widget.toggled.connect(set_value)

    elif isinstance(widget, QtGui.QComboBox):
        try:
            # For selection box
            widget.value_selected.connect(set_value)
        except AttributeError:
            widget.currentIndexChanged.connect(set_value)
    elif isinstance(widget, QtGui.QAbstractSpinBox):
        widget.valueChanged.connect(set_value)

    elif hasattr(widget, 'editingFinished'):
        widget.editingFinished.connect(set_value)
    elif isinstance(widget, (QtGui.QTextEdit, QtGui.QPlainTextEdit)):
        widget.textChanged.connect(set_value)
    elif hasattr(widget, "valueChanged"):
        widget.valueChanged.connect(set_value)
# end connect


def connect_method(instance, method_name, connectd_method=None):
    """Connect the set and get methods with the given widget to bind when one or the other changes.

    This method assumes that the instance has a set_{property_name} method.
    """
    if method_name is None or connectd_method is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    connectd_method = FunctionProxy(connectd_method)

    # ===== Setter Method =====
    set_method = getattr(instance, method_name).__func__

    # Setter method
    def set_prop(self, *args, **kwargs):
        # Check for a change before calling the function
        set_method(self, *args, **kwargs)
        connectd_method(*args, **kwargs)

    # Set the method names
    setattr(instance, method_name, set_prop.__get__(instance, instance.__class__))
# end connect_method


def bind(instance, property_name, widget=None, setter=None, getter=None):
    """Bind a property to a widget or another objects setter and getter methods.

    Args:
        instance (object): Instance object to control with a widget.
        property_name (str): Property name to change values when the widget changes.
        widget (QWidget)[None]: Widget to control the property.
        setter (function)[None]: Function that sets the widget's value.
        getter (function)[None]: Function that returns the widget's value.

    Raises:
        ValueError: If not all of the right arguments are given.
            A widget should be given if you are binding to a widget. You can optionally give a setter
            and/or getter function with a widget. If a widget is not given then setter
            and getter functions must be given!
    """
    if widget is None and setter is None or widget is None and getter is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    if hasattr(instance, "set_" + property_name):
        connect_setter_with_widget(instance, property_name, widget, setter, getter)
    elif is_property(instance, property_name):
        connect_property_with_widget(instance, property_name, widget, setter, getter)
    elif hasattr(instance, property_name) and callable(getattr(instance, property_name)):
        connect_method(instance, property_name, setter or getter)
    elif hasattr(instance, property_name):
        create_property_from_attribute(instance, property_name, widget, setter, getter)
    else:
        create_property_from_other(instance, property_name, widget, setter, getter)
    # end
# end bind


def connect_property_with_widget(instance, property_name, widget=None, setter=None, getter=None):
    """Connect a property and setter to the given widget.

    This method assumes that the instance has a property named {property_name}.
    """
    if widget is None and setter is None or widget is None and getter is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    if setter is None:
        def setter(value):
            return set_widget_value(widget, value)
    else:
        setter = FunctionProxy(setter)

    if getter is None:
        def getter():
            return get_widget_value(widget)
    else:
        getter = FunctionProxy(getter)

    # Check for an existing property to manipulate the value and create the setter
    old_prop = getattr(instance.__class__, property_name)
    doc = old_prop.__doc__

    # ===== Getter method =====
    get_prop = old_prop.fget

    # ===== Setter method =====
    def set_prop(self, value):
        # Check for a change before calling the function
        if value != get_prop(self):
            old_prop.fset(self, value)
        new_val = get_prop(self)
        if new_val != getter():
            setter(new_val)
    set_prop.__doc__ = """Set the """ + property_name + """ value and widget."""

    # ===== Default Value =====
    try:
        default_value = get_prop(instance)
    except AttributeError:
        default_value = None
    setter(default_value)

    # Set the method names
    setattr(instance, "set_"+property_name, set_prop.__get__(instance, instance.__class__))
    setattr(instance, "get_"+property_name, get_prop.__get__(instance, instance.__class__))

    # Connect the widget to the property value change.
    if widget:
        connect(widget, getattr(instance, "set_"+property_name))

    # Set the property
    setattr(instance.__class__, property_name, property(get_prop, set_prop, doc=doc))
# end connect_property_with_widget


def connect_setter_with_widget(instance, property_name, widget=None, setter=None, getter=None):
    """Connect the set and get methods with the given widget to bind when one or the other changes.

    This method assumes that the instance has a set_{property_name} method.
    """
    if widget is None and setter is None or widget is None and getter is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    if setter is None:
        def setter(value):
            return set_widget_value(widget, value)
    else:
        setter = FunctionProxy(setter)

    if getter is None:
        def getter():
            return get_widget_value(widget)
    else:
        getter = FunctionProxy(getter)

    # Underscore property name for get/set methods
    sub_name = "_" + property_name

    # ===== Getter method =====
    get_prop = None
    get_attr = None
    for attr in ["get"+sub_name, "is"+sub_name, "has"+sub_name]:
        try:
            get_prop = getattr(instance, attr).__func__  # Get the unbound method (self not given automatically)
            get_attr = attr
            break
        except:
            pass

    if get_prop is None:
        def get_prop(self):
            return getattr(self, sub_name)
        if not hasattr(instance, sub_name):
            setattr(instance, sub_name, None)  # Create the instance variable.
        get_prop.__doc__ = "Return the %s value" % property_name
        get_attr = "get" + sub_name

    # ===== Setter Method =====
    set_attr = "set"+sub_name
    set_method = getattr(instance, set_attr).__func__

    # Setter method
    def set_prop(self, value):
        # Check for a change before calling the function
        if value != get_prop(self):
            set_method(self, value)
        new_val = get_prop(self)
        if new_val != getter():
            setter(get_prop(self))

    # ===== Default value =====
    try:
        default_value = get_prop(instance)
    except AttributeError:
        default_value = None
    setter(default_value)

    # Set the method names
    setattr(instance, set_attr, set_prop.__get__(instance, instance.__class__))
    setattr(instance, get_attr, get_prop.__get__(instance, instance.__class__))

    # Connect the widget to the property value change.
    if widget:
        connect(widget, getattr(instance, set_attr))
# end connect_setter_with_widget


def create_property_from_attribute(instance, property_name, widget=None, setter=None, getter=None):
    """Suggested to just use bind. This creates a property for the given instance and attribute."""
    if widget is None and setter is None or widget is None and getter is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    if setter is None:
        def setter(value):
            return set_widget_value(widget, value)
    else:
        setter = FunctionProxy(setter)

    if getter is None:
        def getter():
            return get_widget_value(widget)
    else:
        getter = FunctionProxy(getter)

    # Underscore property name for get/set methods
    sub_name = "_" + property_name

    # Change the property value to _property_name
    setattr(instance, sub_name, getattr(instance, property_name))

    # ===== Getter method =====
    def get_prop(self):
        return getattr(self, sub_name)
    get_prop.__doc__ = doc = """Return the """ + property_name + """ value"""

    # ===== Setter method =====
    def set_prop(self, value):
        # Check for a change before calling the function
        if value != get_prop(self):
            setattr(self, sub_name, value)
        new_val = get_prop(self)
        if new_val != getter():
            setter(new_val)
    set_prop.__doc__ = """Set the """ + property_name + """ value and widget."""

    # ===== Default value =====
    try:
        default_value = get_prop(instance)
    except AttributeError:
        default_value = None
    setter(default_value)

    # Make a property with the widget
    setattr(instance.__class__, property_name, property(get_prop, set_prop, doc=doc))

    # Set the method names
    setattr(instance, "set"+sub_name, set_prop.__get__(instance, instance.__class__))
    setattr(instance, "get"+sub_name, get_prop.__get__(instance, instance.__class__))

    # Connect the widget to the property value change.
    if widget:
        connect(widget, getattr(instance, "set"+sub_name))
# end create_property_from_attribute


def create_property_from_other(instance, property_name, widget=None, setter=None, getter=None):
    """Suggested to just use bind. This creates a property for the given widget an assumes that the instance does not
    have the given property name.
    """
    if widget is None and setter is None or widget is None and getter is None:
        raise ValueError("Must either give a widget, give getter and setter, or give all inputs!")

    if setter is None:
        def setter(value):
            return set_widget_value(widget, value)
    else:
        setter = FunctionProxy(setter)

    if getter is None:
        def getter():
            return get_widget_value(widget)
    else:
        getter = FunctionProxy(getter)

    # Underscore property name for get/set methods
    sub_name = "_" + property_name

    # ===== Getter method =====
    def get_prop(self):
        return getter()
    get_prop.__doc__ = doc = """Return the """ + property_name + """ value"""

    # ===== Setter method =====
    def set_prop(self, value):
        setter(value)
    get_prop.__doc__ = doc = """Set the """ + property_name + """ value and widget."""

    # ===== Default Value =====
    try:
        setattr(instance, sub_name, getattr(instance, property_name))
    except AttributeError:
        setattr(instance, sub_name, None)

    # Make a property with the widget
    # Set the method names
    setattr(instance, "set"+sub_name, set_prop.__get__(instance, instance.__class__))
    setattr(instance, "get"+sub_name, get_prop.__get__(instance, instance.__class__))

    # Set the property
    setattr(instance.__class__, property_name, property(get_prop, set_prop, doc=doc))
# end create_property_from_other


def test_bind():
    """Test for how binding an instance property to a widget should work.

    NOTE:
        You can have no property or method! bind can work on the widget value itself!

        Leaving the widget focus causes a change too! The binder checks for the value to change too!
        If the value didn't change the set method will not be called!
    """
    class A(object):
        def __init__(self, x=0):
            self._x = x

        @property
        def x(self):
            print("get x", self._x)
            return self._x
        @x.setter
        def x(self, value):
            self._x = value
            print("set x", self._x)

        # def is_x(self):
        #     print("get x", self._x)
        #     return self._x
        # def has_x(self):
        #     print("get x", self._x)
        #     return self._x
        # def set_x(self, value):
        #     self._x = value
        #     print("set x", self._x)

    a = A()
    le = QtGui.QLineEdit()
    le.show()
    bind(a, "x", le)

    btn = QtGui.QPushButton("Set object value '0'")
    btn.show()

    def set_obj_val():
        if hasattr(A, 'x'):
            a.x = 0
        else:
            a.set_x(0)
    btn.clicked.connect(set_obj_val)

    # a.x = 3
    # a.set_x(True))

    return a, le, btn
# end test_bind


if __name__ == "__main__":
    QtGui.QApplication([])

    vars = test_bind()

    QtGui.qApp.exec_()
