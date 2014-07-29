#! /usr/bin/env python

import json

from customsort import *

# A typical Python data structure, mixing dicts and lists.
# Source: http://en.wikipedia.org/wiki/JSON
stuff = {
    "address": {
        "city": "New York",
        "streetAddress": "21 2nd Street",
        "postalCode": "10021-3100",
        "state": "NY",
    },
    "age": 25,
    "firstName": "John",
    "height_cm": 167.6,
    "isAlive": True,
    "lastName": "Smith",
    "phoneNumbers": [
        {
            "number": "212 555-1234",
            "type": "home"
        },
        {
            "number": "646 555-4567",
            "type": "office"
        }
    ]
}

# Specify a sorting order for the keys of some nested dicts.
orders = [
    ["firstName", "lastName", "isAlive", "age", "height_cm", "address", "phoneNumbers"],
    ["streetAddress", "city", "state", "postalCode"],
    ["type", "number"],
]
    
def test_typical_use_case():
    expected = OrderedDict([
        ('firstName', 'John'),                   # The keys appear in the same order
        ('lastName', 'Smith'),                   # as specified in the `orders` list
        ('isAlive', True),                       # "firstName", "lastName", "isAlive", etc.
        ('age', 25),
        ('height_cm', 167.6),
        ('address', OrderedDict([
            ('streetAddress', '21 2nd Street'),  # This works for any dict nested
            ('city', 'New York'),                # either in another dict...
            ('state', 'NY'),
            ('postalCode', '10021-3100')
        ])),
        ('phoneNumbers', [
            OrderedDict([                        # ... or in a list.
                ('type', 'home'),
                ('number', '212 555-1234')
            ]), 
            OrderedDict([
                ('type', 'office'),
                ('number', '646 555-4567')
            ])
        ])]
    )
    custom_sort = make_custom_sort(orders)
    assert custom_sort(stuff) == expected

def test_JSON_typical_use_case(): # You could dump a JSON file with a meaningful order
    expected = """{
        "firstName": "John", 
        "lastName": "Smith", 
        "isAlive": true, 
        "age": 25, 
        "height_cm": 167.6, 
        "address": {
            "streetAddress": "21 2nd Street", 
            "city": "New York", 
            "state": "NY", 
            "postalCode": "10021-3100"
        }, 
        "phoneNumbers": [
            {
                "type": "home", 
                "number": "212 555-1234"
            }, 
            {
                "type": "office", 
                "number": "646 555-4567"
            }
        ]
    }""".replace("\n    ","\n") # dedent all lines
    custom_sort = make_custom_sort(orders)
    assert json.dumps( custom_sort(stuff), indent=4) == expected

def test_no_order_for_some_dict():
    new_orders = [orders[0], orders[2]]  # no more 'address' key order
    custom_sort = make_custom_sort(new_orders)
    expected = OrderedDict([
        ('firstName', 'John'),
        ('lastName', 'Smith'),
        ('isAlive', True),
        ('age', 25),
        ('height_cm', 167.6),
        ('address', OrderedDict([
            ('city', 'New York'),                # if no order is specified
            ('postalCode', '10021-3100'),        # for a given dictionary,
            ('state', 'NY'),                     # its keys will be sorted
            ('streetAddress', '21 2nd Street')   # in lexicographical order
        ])),
        ('phoneNumbers', [
            OrderedDict([
                ('type', 'home'),
                ('number', '212 555-1234')
            ]), 
            OrderedDict([
                ('type', 'office'),
                ('number', '646 555-4567')
            ])
        ])]
    )
    result = custom_sort(stuff)
    assert result == expected

def test_no_order_for_some_keys():
    new_orders = [orders[0][:2] + orders[0][5:], orders[1], orders[2]] # no more 'isAlive', 'age', 'height_cm' keys
    custom_sort = make_custom_sort(new_orders)
    expected = OrderedDict([
        ('firstName', 'John'),
        ('lastName', 'Smith'),
        ('address', OrderedDict([
            ('streetAddress', '21 2nd Street'),
            ('city', 'New York'),
            ('state', 'NY'),
            ('postalCode', '10021-3100')
        ])),
        ('phoneNumbers', [
            OrderedDict([
                ('type', 'home'),
                ('number', '212 555-1234')
            ]), 
            OrderedDict([
                ('type', 'office'),
                ('number', '646 555-4567')
            ])
        ]),
        ('isAlive', True),     # the missing keys
        ('height_cm', 167.6),  # are rejected at the end
        ('age', 25),           # in an unspecified order
    ])
    result = custom_sort(stuff)
    assert result == expected

def test_root_is_a_list():
    stuff = [
        {"Alice": 1, "Bob": 2, "Eve": 3, "Oscar": 4},
        {"Bob": 5, "Alice": 6, "Eve": 7, "Oscar": 8},
        {"Bob": 9, "Alice": 0, "Oscar": 1, "Eve": 2},
    ]
    orders = [["Bob", "Oscar", "Alice", "Eve"]]
    expected = [
        OrderedDict([('Bob', 2), ('Oscar', 4), ('Alice', 1), ('Eve', 3)]),
        OrderedDict([('Bob', 5), ('Oscar', 8), ('Alice', 6), ('Eve', 7)]),
        OrderedDict([('Bob', 9), ('Oscar', 1), ('Alice', 0), ('Eve', 2)]),
    ]
    custom_sort = make_custom_sort(orders)
    result = custom_sort(stuff)
    assert result == expected

def test_deep_sorted_copy():
    """ The result is an entirely new object. """
    stuff = {"Alice": 1, "Bob": [1,2,3], "Eve": set("ABC"), "Oscar": 4}
    orders = [["Bob", "Oscar", "Alice", "Eve"]]
    expected = OrderedDict([('Bob', [1,2,3]), ('Oscar', 4), ('Alice', 1), ('Eve', set("ABC"))])
    custom_sort = make_custom_sort(orders)
    result = custom_sort(stuff)
    assert result == expected
    expected["Oscar"] = 5
    expected["Bob"].append(6)
    del expected["Alice"]
    expected["Eve"].add("D")
    assert expected == OrderedDict([('Bob', [1,2,3,6]), ('Oscar', 5), ('Eve', set("ABCD"))])
    assert stuff == {"Alice": 1, "Bob": [1,2,3], "Eve": set("ABC"), "Oscar": 4}
             