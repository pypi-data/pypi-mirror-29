#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A plugin class used by the Pygalle framework.

---
This file is part of pygalle.core.base.klass
Copyright (c) 2018 SAS 9 Février.
Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
---
"""

# pylint: disable=too-many-public-methods

import inspect
import json
from typing import Any, ClassVar

from shortid import ShortId
from dotmap import DotMap


# @see: https://www.python.org/dev/peps/pep-0484


class PygalleBaseClass(object):
    """ The plugin class for Pigalle framework, strictly used by the derived modules. For example:

    `̀̀python

    class CustomClass(PygalleBaseClass):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def hello(self, name):
            return 'hello %s' % name

    ̀̀̀
    """

    __KEYS = DotMap(
        UID='uid',
        INTERNALS='internals',
        PUBLIC='public',
        CLASSNAME='className',
        CATEGORY='category'
    )

    def __init__(self, **kwargs) -> 'PygalleBaseClass':  # pylint: disable=unused-argument
        """ Create a new instance of :class:`PygalleBaseClass`

        Args:
            args:
            kwargs:

        Returns:
            PygalleBaseClass: An instance of :class:`PygalleBaseClass`
        """
        self.options = kwargs
        self.init_properties() \
            .set_uid() \
            .set_class_name() \
            .set_category()

    def init_properties(self) -> 'PygalleBaseClass':
        """ Initialize the Pigalle properties.

        Returns:
            PygalleBaseClass: The current instance.
        """
        self._pigalle = {
            PygalleBaseClass.__KEYS.INTERNALS: dict(),
            PygalleBaseClass.__KEYS.PUBLIC: dict()
        }
        return self

    def get_pigalle(self, key: str) -> dict:
        """ Return value of a Pigalle property.

        Args:
            key(str): The key of looked up Pigalle property.

        Returns:
            object: The value of the Pigalle property.
        """
        return self._pigalle.get(key)

    def internals(self) -> dict:
        """ Return Pigalle containing internals properties of the Pigalle instance.

        :return:
        """
        return self.get_pigalle(PygalleBaseClass.__KEYS.INTERNALS)

    def public(self) -> dict:
        """ Return an object containing public properties of the Pigalle instance.

        :return:
        """
        return self.get_pigalle(PygalleBaseClass.__KEYS.PUBLIC)

    def set_internal(self, key, value) -> 'PygalleBaseClass':
        """ Define an internal property.

        :param key:
        :param value:
        :return:
        """
        self.internals()[key] = value
        return self

    def get_internal(self, key) -> Any:
        """

        :param key:
        :return:
        """
        return self.internals().get(key)

    def set(self, key: str, value: Any) -> 'PygalleBaseClass':
        """ Define a public property.

        :param key:
        :param value:
        :return:
        """
        self.public()[key] = value
        return self

    def get(self, key: str) -> Any:
        """ Return a public property corresponding to the provided key.

        :param key:
        :return:
        """

    def get_uid(self) -> str:
        """ Return the identifier of class instance.

        :return:
        """
        return self.get_internal(PygalleBaseClass.__KEYS.UID)

    def uid(self) -> str:
        """ Return the identifier of class instance.

        :return:
        """
        return self.get_uid()

    def set_uid(self) -> 'PygalleBaseClass':
        """

        :return:
        """
        return self.set_internal(PygalleBaseClass.__KEYS.UID, PygalleBaseClass.generate_uid())

    @staticmethod
    def generate_uid() -> str:
        """ Static helper method to generate an identifier.

        :return:
        """
        return ShortId().generate()

    def set_class_name(self) -> 'PygalleBaseClass':
        """ Store the class name of the current instance of
        :class:`PygalleBaseClass` into internal property.

        Returns:
            PygalleBaseClass: An instance of :class:`PygalleBaseClass`
        """
        return self.set_internal(PygalleBaseClass.__KEYS.CLASSNAME, self.__class__.__name__)

    def get_class_name(self) -> str:
        """ Returns """
        return self.get_internal(PygalleBaseClass.__KEYS.CLASSNAME)

    def set_category(self, category: str = None) -> 'PygalleBaseClass':
        """ Define the category of the class.

        Args:
            category: The name of category.

        Returns:
            PygalleBaseClass: An instance of :class:`PygalleBaseClass`
        """
        return self.set_internal(PygalleBaseClass.__KEYS.CATEGORY, category)

    def get_category(self) -> str:
        """ Returns the class category

        Returns:
            str: The class category.
        """
        return self.get_internal(PygalleBaseClass.__KEYS.CATEGORY)

    def category(self) -> str:
        """ Returns the class category.

        __Alias to :method:`get_category`__

        Returns:
            str: The class category.
        """
        return self.get_category()

    def to_dict(self) -> dict:
        """  Returns a `dict` representation of current instance.

        Returns:
            dict: The `dict` representation of the current instance.
        """
        return {'$pigalle': self._pigalle, 'options': self.options}

    def to_object(self) -> dict:
        """  Returns a `dict` representation of current instance.

        __Alias of :method:`to_object`.__

        Returns:
            dict: The `dict` representation of the current instance.
        """
        return self.to_dict()

    # @todo: not really JSON is returned, but a stringified JSON...
    def to_json(self) -> str:
        """ Returns a representation as JSON of the current instance.

        Returns:
            str: A JSON string.
        """
        return json.dumps(self.to_object(), ensure_ascii=False)

    def instance_of(self, kls: Any) -> bool:
        """ Return true if the current object is an instance of passed type.

        Args:
            kls: The class.

        Returns:
            bool:
              * Return true if the current object is an instance of passed type.
              * False else.
        """
        if not kls:
            raise ValueError
        return isinstance(self, kls)

    @staticmethod
    def is_pigalle_instance(obj: Any) -> bool:
        """ Return true if the passed object as argument is an instance
        of class being to the Pigalle framework.

        Args:
            obj: The object to check.

        Returns:
            bool:
                * True if object is Pigalle.
                * False else.
        """
        return isinstance(obj, PygalleBaseClass)

    @staticmethod
    def is_pigalle_class(kls: ClassVar) -> bool:
        """ Return true if the passed object as argument is a class being to the Pigalle framework.

        Args:
            kls: The class to check.

        Returns:
            bool:
                * True if class is Pigalle.
                * False else.
        """
        return (kls is PygalleBaseClass) or (issubclass(type(kls), PygalleBaseClass))

    @staticmethod
    def is_pigalle(obj: Any) -> bool:
        """ Return true if the passed object as argument is a class or an
        instance of class being to the Pigalle framework.

        Args:
            obj: The class or object to test.

        Returns:
            bool:
                * True if class or object is Pigalle.
                * False else.

        """
        return PygalleBaseClass.is_pigalle_class(obj) or PygalleBaseClass.is_pigalle_instance(obj)

    @classmethod
    def is_parent_class_of(cls, obj: Any) -> bool:
        """ Check if the provided object is a children of the current class.

        Args:
            obj: The object to check.

        Returns:
            bool:
                * True if the current class is a parent of provided object.
                * False else.
        """
        return issubclass(cls, obj.__class__)

    def has_method(self, key: str) -> bool:
        """ Return if a method exists for the current instance.

        Args:
            key: The method name.

        Returns:
            bool:
                * True if the current instance has the provided method.
                * False else.

        """
        return hasattr(self.__class__, key) and callable(getattr(self.__class__, key))

    @classmethod
    def factory(cls, **kwargs) -> 'PygalleBaseClass':
        """ A static factory method to create a new instance of {PigalleBaseClass}.
            If method is called from a derived class, create a new instance of this class.

        Args:
            *args:
            **kwargs:

        Returns:
            PygalleBaseClass: An instance of class or derived class.
        """
        return cls(**kwargs)

    @staticmethod
    def get_class(obj: Any) -> Any:
        """ A static helper to get the class of the passed object.

        Args:
            o: An object.
        """
        return obj.__class__

    @staticmethod
    def class_name(obj: Any) -> str:
        """ A static helper to get the class name of the passed object.

        Args:
            o: An object.

        Returns:
            str: The class name of provided object.
        """
        return PygalleBaseClass.get_class(obj).__name__

    @staticmethod
    def is_class(obj) -> bool:
        """ Static helper method to check if the passed object is a class.

        Args:
            o: An object to test if is a class.

        Returns:
            bool:
                * True if the passed object is a class.
                * False else.
        """
        return inspect.isclass(obj)

    @staticmethod
    def i_am_pigalle() -> bool:
        """ Simple function to check if the class is a Pigalle class.

        Returns:
            bool: Always true.

        """
