import logging
from collections import namedtuple

from sqlalchemy import inspect as sainsp
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy_jsonio.exceptions import NoMapperFound

KeyValuePair = namedtuple('KeyValuePair', ["key", "value"])
PropertyDescriptor = namedtuple('PropertyDescriptor', ["name", "values", "required"])


def convert_inspection_to_nomapper_error(f):
    """ Decorator function to replace NoInspectionAvailable errors with NoMapperFound """

    def function_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except NoInspectionAvailable:
            logging.getLogger(__name__).exception(
                "No SQLA inspection available on target means there is no mapper available.")
            raise NoMapperFound("Provided object/class is not a mappable entity.")

    return function_wrapper


def is_mappable_class(cls):
    try:
        retrievable = sainsp(cls).mapper
        return True
    except NoInspectionAvailable:
        return False
