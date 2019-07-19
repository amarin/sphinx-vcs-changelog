# -*- coding: utf-8 -*-
"""Decorator utils for project classes"""


def use_option(option_name, option_spec):
    """Decorate class with option spec"""

    def use_option_internal(original_class):
        """Actual class decorator"""
        _spec = getattr(original_class, 'option_spec', {})
        _spec = isinstance(_spec, dict) and _spec or {}
        _spec[option_name] = option_spec
        original_class.option_spec = _spec
        return original_class

    return use_option_internal
