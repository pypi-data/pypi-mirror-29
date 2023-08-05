#Copyright 2010 Skytap Inc.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import functools

"""
Unit test fixture framework.

Fixtures are used to create artifacts that unit tests depend on, but are not part of the unit test themselves. A typical
fixture are the service registrations for the hosting nodes the load balancer unit tests depend on.

  1) Clear separation of setup code from test code makes it easier to understand and maintain the unit tests by making
     it obvious what is actually being tested
  2) As the data model changes the fixtures will be updated with sane defaults, and only unit tests that those changes
     are relevant to will need to be updated, but all of the unit tests that use those fixtures will be updated and
     continue to work.
  3) A monolithic fixture shared by all unit tests is not desirable, and fixtures are a way to enable individual unit
     tests to indicate what the fixture they need should be. This improves the overall quality of the unit tests by
     lowering the barrier for specializing the fixture to unit tests and avoiding cruft in the fixture that may no
     longer be used.

Transactions and Fixtures:
At this level there is no support for transactions, but this is the only centralized documentation on fixtures, so it
is addressed here.

Fixtures that create database entries need to do so using transactions. Due to the pre-execute model for fixtures (they
are called and return before the decorated function is called), in general, it is not practical to share transactions
between fixtures. While this may seem like a shortcoming, it is offset by a few things:
  1) Fixtures should perform atomic operations with respect to the data model since the data model enforces this through
     constraints. Aligning the transactions and fixtures with this is actually a good thing.
  2) These are unit tests and the most efficient usage of transactions is not necessary.
  3) Fixtures can be decorated with "helpers" that allow sharing of transactions. For example, the configuration service
     fixtures need to create allocations and account associations. The association is easily factored to be shared by
     all of the allocation fixtures, but these should be done in the same transaction. The association was made into a
     non-fixture decorator that passes the transaction into the fixture.

Suitability for production code (even support code):
LH - As the author of this, I do not feel the fixture framework is suitable for use in a production environment, even
for support scripts. The primary reason for this is the loosy-goosy argument passing, default values, and absolutely
no checks that the arguments that are specified are meaningful in any way. For example, I can specify "cpus=10", and
expect it to do one thing (set the number of cpu resources a hosting node has), however, the actual name for this is
(currently) "vcpus". I will not get an error, and the default vcpus value will be used instead. In unit tests this is
OK since the test will fail if things get messed up. In production, we need more confidence that what we are doing is
correct, particularly when a value is specified. The formal APIs ensure this by requiring values, and not specifying
default values and checking that specified arguments are correct.

LH - yet another reason that fixtures aren't suitable for production code is that they do not necessarily follow the
well defined data access patterns that is required for safe usage in production:
  1) fixtures don't necessarily adhere to the reification/provisioning model
  2) fixtures "know" things outside of the data model (ids, etc) and may issue queries that are different than
     those that would be by the operations
  3) fixture tend to be record based (insert this one record) rather than following the transactions that are actually
     in the operations. This is useful for factoring the fixtures and creating interesting test cases, but can lead
     to states in the DB that would never exist in production. Using fixtures would conflict with the goal of
     minimizing the number of possible states in the db. For example, an operation may delete two records within
     a single transaction, and rely on that happening in its code. If fixtures (or manual manipulation for that
     matter) violate this by deleting only one of the records, the operation may fail the next time it's run.
</rant>
"""
import os
from functools import wraps
import unittest
from inspect import getargspec

# Global indicating whether a fixture function is currently being executed. This is useful for enabling/disabling
# diagnostics code (such as mysql slow query logging).
EXECUTING_FIXTURE = False

try:
    """
    Load the coverage module if it is available and define the decorators to turn coverage off when fixtures are 
    executing so the fixtures aren't included in the test coverage.
    """
    import coverage

    def with_coverage(func):
        """decorator to turn on coverage while executing the decorated method (not thread specific)"""
        @wraps(func)
        def _dec(*args, **kwargs):
            assert coverage.the_coverage.nesting == 0, "decorators don't support nested coverage"
            coverage.start()
            try:
                return func(*args, **kwargs)
            finally:
                coverage.stop()
        return _dec if os.environ.get('WITH_COVERAGE') is not None else func


    def without_coverage(func):
        """decorator to turn off coverage while executing the decorated method (not thread specific)"""
        @wraps(func)
        def _dec(*args, **kwargs):
            assert coverage.the_coverage.nesting <= 1, "decorators don't support nested coverage"
            if coverage.the_coverage.nesting:
                coverage.stop()
                try:
                    return func(*args, **kwargs)
                finally:
                    coverage.start()
            else:
                return func(*args, **kwargs)
        return _dec if os.environ.get('WITH_COVERAGE') is not None else func
except ImportError as ie:
    # Coverage should not be a dependency, so make the decorators that rely on it no-ops

    def with_coverage(func):
        return func

    def without_coverage(func):
        return func

PASS_SELF = '__pass_self'

def pass_self(func):
    """
    Decorate func such that when used as a fixture self will be provided.

    Basically, decorating instance methods with this makes them able to be used as fixtures:

    class Foo(object):

        @default_fixture_name('foo')
        @pass_self
        def _foo(self, **kwargs):
            return 'foo'

        @fixture(_foo)
        def bar(self, foo):
            print foo
    """

    setattr(func, PASS_SELF, True)
    return func

def _clone_function(func, name):
    """
    Clone of a function with a new name so that the new name will appear
    in a stack trace.
    """
    from types import CodeType, FunctionType

    code = func.__code__
    if hasattr(code, 'co_kwonlyargcount'):
        code = CodeType(code.co_argcount, code.co_kwonlyargcount, code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code, code.co_consts, code.co_names,
                        code.co_varnames, code.co_filename, name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)
    else:
        code = CodeType(code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code, code.co_consts, code.co_names,
                        code.co_varnames, code.co_filename, name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)

    ret = FunctionType(code, func.__globals__, name, func.__defaults__, func.__closure__)
    ret.__doc__ = func.__doc__
    return ret

def fixture(fixture_func, *fixture_args, **fixture_kwargs):
    """
    Decorator which calls fixture_func to create a fixture for a test.

    fixture_func - the function that produces the fixture
    fixture_args - the args to pass to the fixture_func
    """
    def dec(func):
        """the decorator function"""

        fixture_name = fixture_kwargs.pop('fixture_name', getattr(fixture_func, 'default_fixture_name', None))
        cleanup_func = fixture_kwargs.pop('fixture_cleanup', getattr(fixture_func, 'default_fixture_cleanup', None))
        
        @without_coverage
        @wraps(func)
        def wrap(*args, **kwargs):
            """call the fixture function, then the wrapped function"""
            global EXECUTING_FIXTURE
            # build the kwargs to pass into the fixture func. These are different from fixture_kwargs
            # since we need to remove the fixture_name from them, but can't modify fixture_kwargs when
            # doing that. Also, we need to pass the kwargs for the function in to the fixture to
            # enable fixture chaining. So, we build a new kwargs dict for each invocation.
            per_call_fixture_kwargs = {}
            per_call_fixture_kwargs.update(kwargs)  # Merge the kwargs into the fixture_kwargs to allow fixture dependencies
            per_call_fixture_kwargs.update(fixture_kwargs)

            if getattr(fixture_func, PASS_SELF, False):
                _fixture_args = args[:1] + fixture_args
            else:
                _fixture_args = fixture_args

            # print "fixture:", fixture_name, fixture_args, per_call_fixture_kwargs
            EXECUTING_FIXTURE = True
            try:
                fixture = fixture_func(*_fixture_args, **per_call_fixture_kwargs)
            finally:
                EXECUTING_FIXTURE = False
            if fixture_name:
                kwargs[fixture_name] = fixture
            try:
                ret = with_coverage(func)(*args, **kwargs)
            except TypeError:
                # This likely indicates a problem between the fixtures and the decorated function (fixtures don't
                # provide all the parameters or function doesn't accept all fixtures). Provide more details to assist
                # with resolving the problem.
                # t, e, tb = sys.exc_info()

                analysis = {}
                arg_spec = getargspec(func)
                args = set(arg_spec.args[len(args):])
                analysis['unsatisfied args'] = sorted(args.difference(kwargs))
                analysis['available args'] = sorted(set(kwargs).difference(args))
                if not arg_spec.keywords:
                    analysis['**kwargs missing'] = True
                raise
            finally:
                # Lets try to cleanup for the rest of the cases
                if cleanup_func:
                    # The argument to the cleanup_func should always be the object
                    # the fixture returns.
                    cleanup_func(fixture)
            return ret
        # functools.partial doesn't have __name__ attribute, use the real function name instead
        return _clone_function(wrap, getattr(fixture_func, "__name__", func.__name__))

    return dec


def get_default_fixture_name(func):
    """get the default fixture name for a function"""
    return getattr(func, 'default_fixture_name', None)

def default_fixture_name(name):
    """decorator to give a fixture function a default fixture name"""
    def dec(func):
        """decorator function"""
        func.default_fixture_name = name
        return func
    return dec

def default_fixture_cleanup(cleanup_func):
    """decorator to give a fixture function a default cleanup function"""
    def dec(func):
        """decorator function"""
        func.default_fixture_cleanup = cleanup_func
        return func
    return dec

def set_fixture(value, **kwargs):
    """insert the value into the fixtures"""
    return value(**kwargs) if callable(value) else value

