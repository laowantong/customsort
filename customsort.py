#! /usr/bin/env python2.7

from collections import OrderedDict


def make_custom_sort(orders):
    """
    Sort in a specified order any dictionary nested in a complex structure.
    Especially useful for sorting a JSON file in a meaningful order.

    Args:
        orders: a list of lists of keys in the desired order.
    
    Returns:
        A new object with any nested dict sorted accordingly.
        See test-customsort.py for more details and edge cases.
    
    Example:
    >>> stuff = {
    ...     "Alice": 0,
    ...     "Bob": [1, 2, {"fizz": 4, "buzz": 6, "fizzbuzz": 7}],
    ...     "Eve": set("ABC"),
    ...     "Oscar": {"fizz": 3, "buzz": 5, "fizzbuzz": 15}
    ... }
    >>> custom_sort = make_custom_sort([["Oscar","Alice","Bob","Eve"], ["buzz","fizzbuzz","fizz"]])
    >>> sorted_stuff = custom_sort(stuff)
    >>> assert sorted_stuff == OrderedDict([
    ...     ('Oscar', OrderedDict([('buzz', 5), ('fizzbuzz', 15), ('fizz', 3)])),
    ...     ('Alice', 0),
    ...     ('Bob', [1, 2, OrderedDict([('buzz', 6), ('fizzbuzz', 7), ('fizz', 4)])]),
    ...     ('Eve', set(['A', 'C', 'B']))
    ... ])
    """
    orders = [{k: -i for (i, k) in enumerate(reversed(order), 1)} for order in orders]
    def process(stuff):
        if isinstance(stuff, dict):
            l = [(k, process(v)) for (k, v) in stuff.iteritems()]
            keys = set(stuff)
            for order in orders:
                if keys.issuperset(order):
                    return OrderedDict(sorted(l, key=lambda x: order.get(x[0], 0)))
            return OrderedDict(sorted(l))
        if isinstance(stuff, list):
            return [process(x) for x in stuff]
        return stuff
    return process