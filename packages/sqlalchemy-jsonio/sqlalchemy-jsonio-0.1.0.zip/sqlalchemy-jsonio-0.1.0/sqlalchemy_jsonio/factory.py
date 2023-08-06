import logging
import sqlalchemy.types as satypes
from sqlalchemy import inspect as sainsp

from .exceptions import NoTypeMapping
from .util import convert_inspection_to_nomapper_error, PropertyDescriptor, KeyValuePair

_logger = logging.getLogger(__name__)

"""
Some types are not supported here. Like LargeBinary/Binary, Concatenable and more.
"""
default_type_mapping = {
    satypes.Integer: "integer",
    satypes.Numeric: "integer",
    satypes.Float: "number",
    satypes.SmallInteger: "integer",
    satypes.DateTime: "string",
    satypes.Date: "string",
    satypes.Time: "string",
    satypes.Boolean: "boolean",
    satypes.String: "string",
    satypes.Text: "string",
    satypes.Unicode: "string",
    satypes.UnicodeText: "string",
    satypes.Enum: "string"
}

"""
Additional property descriptions that are associated with types. Eg. max string length for string types. 
"""


def _datetime_fmt(column):
    return [KeyValuePair(key="format", value="date-time")]


def _date_fmt(column):
    return [KeyValuePair(key="format", value="date")]


def _time_fmt(column):
    return [KeyValuePair(key="format", value="time")]


def _string_length(column):
    ext = []
    if column.type.length:
        ext.append(KeyValuePair(key="maxLength", value=column.type.length))
    return ext


property_type_extensions = {
    satypes.DateTime: _datetime_fmt,
    satypes.Date: _date_fmt,
    satypes.Time: _time_fmt,
    satypes.String: _string_length,
    satypes.Text: _string_length,
    satypes.Unicode: _string_length,
    satypes.UnicodeText: _string_length
}


class SchemaFactory(object):
    def __init__(self, type_mapping=default_type_mapping, type_extensions=property_type_extensions,
                 ignore_primary=True, ignore_foreign_non_nullable=False, ignore_foreign_nullable=False):
        """
        :param type_mapping: Used to determine the jsonschema type from the SQLAlchemy mapped type. 
        :param ignore_primary: Ignore primary key columns.
        :param ignore_foreign_non_nullable: Ignore non nullable foreign key columns.
        :param ignore_foreign_nullable: Ignore nullable foreign key columns.
        """
        self.type_mapping = type_mapping
        self.type_extensions = type_extensions
        self.ignore_primary = ignore_primary
        self.ignore_foreign_non_nullable = ignore_foreign_non_nullable
        self.ignore_foreign_nullable = ignore_foreign_nullable

    @convert_inspection_to_nomapper_error
    def create_schema(self, cls):
        new_schema = {
            "properties": {},
            "title": cls.__name__,
            "source_class": cls.__name__,
            "source_module": cls.__module__,
            "type": "object"
        }
        for column in sainsp(cls).mapper.columns:
            if not self._is_ignored(column):
                _logger.debug("Creating property for '{1}'. ({0})".format(cls, column.name))
                descriptor = self._create_property(column)
                new_schema["properties"][descriptor.name] = descriptor.values
                if descriptor.required:
                    if "required" not in new_schema:
                        new_schema["required"] = []
                    new_schema["required"].append(descriptor.name)
            else:
                _logger.debug("Column '{1}' ignored. ({0})".format(cls, column.name))

        return new_schema

    def _is_ignored(self, column):
        if column.primary_key and self.ignore_primary:
            return True
        if column.foreign_keys:
            if column.nullable and self.ignore_foreign_nullable:
                return True
            if not column.nullable and self.ignore_foreign_non_nullable:
                return True
        return False

    def _create_property(self, column):
        col_type = type(column.type)  # Converts sql type string to sqlalchemy type
        if col_type not in self.type_mapping:
            raise NoTypeMapping("No mapping for SQLA type '{}' available.".format(col_type))
        property_values = {
            "type": self.type_mapping[col_type]
        }
        if col_type in self.type_extensions:
            for key_value_pair in self.type_extensions[col_type](column):
                property_values[key_value_pair.key] = key_value_pair.value
        return PropertyDescriptor(name=column.name, values=property_values, required=not column.nullable)
