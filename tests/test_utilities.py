# -*- coding: utf-8 -*-

import time

import pydash as _

from . import fixtures
from .fixtures import parametrize


@parametrize('case,expected', [
    ((lambda a, b: a / b, 4, 2), 2)
])
def test_attempt(case, expected):
    assert _.attempt(*case) == expected


@parametrize('case,expected', [
    ((lambda a, b: a / b, 4, 0), ZeroDivisionError)
])
def test_attempt_exception(case, expected):
    assert isinstance(_.attempt(*case), expected)


@parametrize('case', [
    'foo',
    'bar'
])
def test_constant(case):
    assert _.constant(case)() == case


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
    ({'name': 'fred'},
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [True, False]),
    (lambda obj: obj['age'],
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [40, 36]),
    (None,
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}])
])
def test_callback(case, arg, expected):
    getter = _.callback(case)
    assert _.map_(arg, getter) == expected


@parametrize('case', [
    _.iteratee
])
def test_callback_aliases(case):
    assert _.callback is case


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
    ('spouse.name',
     [{'name': 'fred', 'age': 40, 'spouse': {'name': 'wilma'}},
      {'name': 'barney', 'age': 36, 'spouse': {'name': 'betty'}}],
     ['wilma', 'betty'])
])
def test_deep_property(case, arg, expected):
    assert _.map_(arg, _.deep_property(case)) == expected


@parametrize('case', [
    _.deep_prop
])
def test_deep_property_aliases(case):
    assert _.deep_property is case


@parametrize('case,expected', [
    ((1,), 1),
    ((1, 2), 1),
    ((), None)
])
def test_identity(case, expected):
    assert _.identity(*case) == expected


@parametrize('case,arg,expected', [
    ({'age': 36}, {'name': 'barney', 'age': 36}, True),
    ({'age': 36}, {'name': 'barney', 'age': 40}, False),
])
def test_matches(case, arg, expected):
    assert _.matches(case)(arg) is expected


@parametrize('case,args,kargs,key', [
    ((lambda a, b: a + b,), (1, 2), {}, '(1, 2){}'),
    ((lambda a, b: a + b,), (1,), {'b': 2}, "(1,){'b': 2}"),
    ((lambda a, b: a + b, lambda a, b: a * b), (1, 2), {}, 2),
    ((lambda a, b: a + b, lambda a, b: a * b), (1,), {'b': 2}, 2),
])
def test_memoize(case, args, kargs, key):
    memoized = _.memoize(*case)
    expected = case[0](*args, **kargs)
    assert memoized(*args, **kargs) == expected
    assert memoized.cache
    assert memoized.cache[key] == expected


@parametrize('case,expected', [
    ((), None),
    ((1, 2, 3), None)
])
def test_noop(case, expected):
    assert _.noop(*case) == expected


def test_now():
    present = int(time.time() * 1000)
    # Add some leeway when comparing time.
    assert (present - 1) <= _.now() <= (present + 1)


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
])
def test_property_(case, arg, expected):
    assert _.map_(arg, _.property_(case)) == expected


@parametrize('case', [
    _.prop
])
def test_property_aliases(case):
    assert _.property_ is case


@parametrize('case,arg,expected', [
    ({'name': 'fred', 'age': 40}, ['name', 'age'], ['fred', 40]),
])
def test_property_of(case, arg, expected):
    assert _.map_(arg, _.property_of(case)) == expected


@parametrize('case', [
    _.prop_of
])
def test_property_of_aliases(case):
    assert _.property_of is case


@parametrize('case,minimum,maximum', [
    ((), 0, 1),
    ((25,), 0, 25),
    ((5, 10), 5, 10)
])
def test_random(case, minimum, maximum):
    for x in range(50):
        rnd = _.random(*case)
        assert isinstance(rnd, int)
        assert minimum <= rnd <= maximum


@parametrize('case,floating,minimum,maximum', [
    ((), True, 0, 1),
    ((25,), True, 0, 25),
    ((5, 10), True, 5, 10),
    ((5.0, 10), False, 5, 10),
    ((5, 10.0), False, 5, 10),
    ((5.0, 10.0), False, 5, 10),
    ((5.0, 10.0), True, 5, 10),
])
def test_random_float(case, floating, minimum, maximum):
    for x in range(50):
        rnd = _.random(*case, floating=floating)
        assert isinstance(rnd, float)
        assert minimum <= rnd <= maximum


@parametrize('case,expected', [
    ((10,), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ((1, 11), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ((0, 30, 5), [0, 5, 10, 15, 20, 25]),
    ((0, -10, -1), [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]),
    ((0,), []),
])
def test_range_(case, expected):
    assert _.range_(*case) == expected


@parametrize('case,expected', [
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'cheese'),
     'crumpets'),
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'stuff'),
     'nonsense'),
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'foo'),
     None),
    ((False, 'foo'), None),
    ((False, 'foo', 'default'), 'default'),
])
def test_result(case, expected):
    assert _.result(*case) == expected


@parametrize('case,expected', [
    ((5, lambda i: i * i), [0, 1, 4, 9, 16]),
])
def test_times(case, expected):
    assert _.times(*case) == expected


@parametrize('case,expected', [
    ((), '1'),
    (('foo',), 'foo2')
])
def test_unique_id(case, expected):
    assert _.unique_id(*case) == expected
