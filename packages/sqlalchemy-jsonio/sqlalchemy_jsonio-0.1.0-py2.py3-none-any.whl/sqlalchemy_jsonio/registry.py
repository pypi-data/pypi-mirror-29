import inspect as pyinsp
import logging

from .factory import SchemaFactory
from .util import is_mappable_class

_logger = logging.getLogger(__name__)


class SchemaRegistry(object):
    def __init__(self, schema_factory=None):
        self._registry = {}
        self.factory = schema_factory or SchemaFactory()

    def __getitem__(self, cls):
        return self._registry[cls]

    def __setitem__(self, cls, schema):
        if cls in self:
            _logger.warn("Class '{}' already has an associated schema. This will be overridden with the new schema!")
        # Todo: Validate custom_schema against some metaschema?
        self._registry[cls] = schema

    def __contains__(self, key):
        return key in self._registry

    def __len__(self):
        return len(self._registry)

    def __iter__(self):
        return self._registry.__iter__()

    def items(self):
        return self._registry.items()

    def keys(self):
        return self._registry.keys()

    def register_class(self, cls, custom_schema=None):
        _logger.info("Registering class '{}'".format(cls.__name__))
        self[cls] = custom_schema or self.factory.create_schema(cls)

    def register_module(self, module_, depth=0):
        _logger.info("Registering module '{}'".format(module_.__name__))
        mappable_classes = self._retrieve_mappable_classes(module_, depth)
        _logger.debug("Retrieved set of mappable classes: {}".format(mappable_classes))
        for cls in mappable_classes:
            self.register_class(cls)

    def _retrieve_mappable_classes(self, module_, depth):
        _logger.info("Retrieve classes for module '{}'".format(module_))
        """ Recursively collect classes from submodules into a set and return it. """
        module_attrs = [getattr(module_, attr) for attr in dir(module_) if not attr.startswith('_')]
        mappable_classes = {cls for cls in module_attrs if is_mappable_class(cls)}
        _logger.debug("Mappable classes in '{}': {}".format(module_.__name__, mappable_classes))
        if depth > 0:
            for attr in module_attrs:
                if pyinsp.ismodule(attr):
                    # mappable_class |= self._retrieve_mappable_classes(attr, depth=depth - 1)
                    # Todo - Discussion: These are somewhat equivalent but the lower one seems more readable.
                    mappable_classes = mappable_classes.union(self._retrieve_mappable_classes(attr, depth=depth - 1))
        return mappable_classes
