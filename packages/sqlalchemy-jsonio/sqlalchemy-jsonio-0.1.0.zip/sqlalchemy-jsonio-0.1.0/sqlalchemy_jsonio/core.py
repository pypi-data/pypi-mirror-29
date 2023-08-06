import json
import logging

import jsonschema
from jsonschema import ValidationError
from sqlalchemy import inspect as sainsp
from sqlalchemy_jsonio.exceptions import MultipleSchemaMatches, NoSchemaFound
from sqlalchemy_jsonio.registry import SchemaRegistry
from sqlalchemy_jsonio.util import convert_inspection_to_nomapper_error

_logger = logging.getLogger(__name__)


def _filter_none(entity, column):  # Return true if entity has value for column
    return getattr(entity, column.key) is not None


def _filter_primary(entity, column):  # Return true if column is not primary
    if column.primary_key:
        return False
    return True


def _filter_foreign(entity, column):  # Return true if column is not foreign
    if column.foreign_keys:
        return False
    return True


class JsonIO(object):
    def __init__(self, schema_registry=None):
        self._registry = schema_registry or SchemaRegistry()

    @convert_inspection_to_nomapper_error
    def entity_as_dict(self, entity, ignore_primary=False, ignore_none=False, ignore_foreign=False):
        entity_dict = {}
        _logger.info("Creating dictionary from {}".format(entity))
        for column in sainsp(entity).mapper.columns:
            if ignore_primary and not _filter_primary(entity, column):
                _logger.debug("Ignoring {}. Primary key.".format(column.name))
                continue
            if ignore_none and not _filter_none(entity, column):
                _logger.debug("Ignoring {}. 'None' value.".format(column.name))
                continue
            if ignore_foreign and not _filter_foreign(entity, column):
                _logger.debug("Ignoring {}. Foreign key.".format(column.name))
                continue
            entity_dict[column.key] = getattr(entity, column.key)
        return entity_dict

    def entity_as_json(self, entity, ignore_primary=False, ignore_none=False, ignore_foreign=False, compact=False):
        entity_dict = self.entity_as_dict(entity, ignore_primary, ignore_none, ignore_foreign)
        if compact:
            return json.dumps(entity_dict, sort_keys=True, separators=(",", ":"))
        else:
            return json.dumps(entity_dict, sort_keys=True, indent=2)

    def entity_from_dict(self, entity_dict, target_class=None):
        _logger.info("Creating entity from {}".format(entity_dict))
        if target_class:
            self._validate_entity_dict_against_target(entity_dict, target_class)
        else:
            target_class = self._find_target_class(entity_dict)
        return target_class(**entity_dict)  # Will error if there is a key that does not correspond with a field!

    def entity_from_json(self, entity_json, target_class=None):
        entity_dict = json.loads(entity_json)
        return self.entity_from_dict(entity_dict, target_class)

    def register_class(self, cls, custom_schema=None):
        self._registry.register_class(cls, custom_schema)

    def register_module(self, module_, depth=0):
        self._registry.register_module(module_, depth)

    def _find_target_class(self, entity_dict):
        _logger.info("Searching for unique matching schema.")
        class_matches = []
        for cls, schema in iter(self._registry.items()):
            try:
                jsonschema.validate(entity_dict, schema)
                _logger.info("Dictionary matches schema for '{}'".format(cls))
                class_matches.append(cls)
            except ValidationError:
                pass
        if len(class_matches) == 0:
            raise NoSchemaFound("Provided dictionary didn't match against any schema in the registry.")
        if len(class_matches) > 1:
            raise MultipleSchemaMatches("""Provided dictionary matched against more than one schema. 
            Matched {} classes: {}.""".format(len(class_matches), class_matches))
        return class_matches[0]

    def _validate_entity_dict_against_target(self, entity_dict, target_class):
        try:
            schema = self._registry[target_class]
            jsonschema.validate(entity_dict, schema)
            _logger.debug("Dictionary matches schema for provided target '{}'".format(target_class))
        except KeyError:
            raise NoSchemaFound("No schema was found for class '{}'".format(target_class))
        # except ValidationError as ve:
        #     raise ve  # To_do: Custom error to clarify
