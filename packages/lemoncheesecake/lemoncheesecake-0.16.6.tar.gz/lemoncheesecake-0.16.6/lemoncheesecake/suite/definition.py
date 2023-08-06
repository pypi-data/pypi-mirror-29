'''
Created on Sep 8, 2016

@author: nicolas
'''

import inspect
import copy

from lemoncheesecake.suite.loader import get_test_methods_from_class
from lemoncheesecake.suite.core import InjectedFixture
from lemoncheesecake.exceptions import ProgrammingError

__all__ = "add_test_in_suite", "add_tests_in_suite", "get_metadata", \
    "suite", "test", "tags", "prop", "link", "disabled", "conditional", "hidden", "inject_fixture"


class Metadata:
    _next_rank = 1

    def __init__(self):
        self.is_test = False
        self.is_suite = False
        self.name = None
        self.description = None
        self.properties = {}
        self.tags = []
        self.links = []
        self.rank = 0
        self.disabled = False
        self.condition = None


def get_metadata_next_rank():
    rank = Metadata._next_rank
    Metadata._next_rank += 1
    return rank


def add_test_in_suite(test, suite, before_test=None, after_test=None):
    # pre-checks
    if before_test and after_test:
        raise ProgrammingError("before_test and after_test are mutually exclusive")

    if hasattr(suite, test.name):
        raise ProgrammingError("Object %s has already an attribute named '%s'" % (suite, test.name))

    # build test func metadata
    md = test.callback._lccmetadata = Metadata()
    md.is_test = True
    md.name = test.name
    md.description = test.description
    md.tags.extend(test.tags)
    md.properties.update(test.properties)
    md.links.extend(test.links)
    md.disabled = test.disabled

    # set test func rank
    if before_test or after_test:
        ref_test_name = before_test if before_test else after_test
        test_methods = get_test_methods_from_class(suite)
        try:
            ref_test_obj = next(t for t in test_methods if t._lccmetadata.name == ref_test_name)
        except StopIteration:
            raise ProgrammingError("There is no base test named '%s' in class %s" % (ref_test_name, suite))

        if before_test:
            md.rank = ref_test_obj._lccmetadata.rank
            for test_method in filter(lambda t: t._lccmetadata.rank >= md.rank , test_methods):
                test_method._lccmetadata.rank += 1
        else: # after_test
            md.rank = ref_test_obj._lccmetadata.rank
            for test_method in filter(lambda t: t._lccmetadata.rank <= md.rank , test_methods):
                test_method._lccmetadata.rank -= 1
    else:
        md.rank = get_metadata_next_rank()

    # set test func and suite test method
    setattr(suite, test.name, test.callback.__get__(suite))


def add_tests_in_suite(tests, suite, before_test=None, after_test=None):
    if before_test and after_test:
        raise ProgrammingError("before_test and after_test are mutually exclusive")

    if after_test:
        previous_test = after_test
        for test in tests:
            add_test_in_suite(test, suite, after_test=previous_test)
            previous_test = test.name
    else:
        for test in tests:
            add_test_in_suite(test, suite, before_test=before_test)

_objects_with_metadata = []
def get_metadata(obj):
    global _objects_with_metadata

    if hasattr(obj, "_lccmetadata"):
        if obj not in _objects_with_metadata: # metadata comes from the superclass
            obj._lccmetadata = copy.deepcopy(obj._lccmetadata)
        return obj._lccmetadata
    else:
        obj._lccmetadata = Metadata()
        _objects_with_metadata.append(obj)
        return obj._lccmetadata


def suite(description, name=None, rank=None):
    """Decorator, mark a class as a suite class"""
    def wrapper(klass):
        if not inspect.isclass(klass):
            raise ProgrammingError("%s is not a class (suite decorator can only be used on a class)" % klass)
        md = get_metadata(klass)
        md.is_suite = True
        md.rank = rank if rank != None else get_metadata_next_rank()
        md.name = name or klass.__name__
        md.description = description
        return klass
    return wrapper


def test(description, name=None):
    """Decorator, make a method as a test method"""
    def wrapper(func):
        if not inspect.isfunction(func):
            raise ProgrammingError("%s is not a function (test decorator can only be used on a function)" % func)
        md = get_metadata(func)
        md.is_test = True
        md.rank = get_metadata_next_rank()
        md.name = name or func.__name__
        md.description = description
        return func
    return wrapper


def tags(*tag_names):
    """Decorator, add tags to a test or a suite"""
    def wrapper(obj):
        md = get_metadata(obj)
        md.tags.extend(tag_names)
        return obj
    return wrapper


def prop(key, value):
    """Decorator, add a property (key/value) to a test or a suite"""
    def wrapper(obj):
        md = get_metadata(obj)
        md.properties[key] = value
        return obj
    return wrapper


def link(url, name=None):
    """Decorator, set a link (with an optional friendly name) to a test or a suite"""
    def wrapper(obj):
        md = get_metadata(obj)
        md.links.append((url, name))
        return obj
    return wrapper


def disabled():
    """Decorator, disable a test or a suite"""
    def wrapper(obj):
        md = get_metadata(obj)
        md.disabled = True
        return obj
    return wrapper


def conditional(condition):
    """Decorator, the test or suite will only appear if the given condition callback return a true value"""
    def wrapper(obj):
        md = get_metadata(obj)
        md.condition = condition
        return obj
    return wrapper


def hidden():
    return conditional(lambda _: False)


def inject_fixture(fixture_name=None):
    return InjectedFixture(fixture_name)