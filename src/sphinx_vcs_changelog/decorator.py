# -*- coding: utf-8 -*-
"""Decorator utils for project classes"""


def use_option(option_name: str, option_spec: type) -> callable:
    """Decorate class with option spec parameters

    Inserts option <option_name> with expected class
    into directive class definition. Defines option_spec class attribute if
    not defined in original class.

    :param option_name: directive option name
    :type option_name: str
    :param option_spec: directive option type, like six.text_type or int
    :type option_spec: type

    :returns: class decorator
    :rtype: callable
    """

    def use_option_internal(original_class):
        """Actual class decorator
        :param original_class: class to decorate
        :type original_class: type

        :return: Decorated class
        :rtype: type
        """
        _spec = getattr(original_class, 'option_spec', {})
        _spec = isinstance(_spec, dict) and _spec or {}
        _spec[option_name] = option_spec
        original_class.option_spec = _spec
        return original_class

    return use_option_internal
