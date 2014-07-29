# Custom sort

Sort in a specified order any dictionary nested in a complex structure.
Especially useful for sorting a JSON file in a meaningful order.


## Example

```python
stuff = {
    "Alice": 0,
    "Bob": [1, 2, {"fizz": 4, "buzz": 6, "fizzbuzz": 7}],
    "Eve": set("ABC"),
    "Oscar": {"fizz": 3, "buzz": 5, "fizzbuzz": 15}
}
custom_sort = make_custom_sort([["Oscar","Alice","Bob","Eve"], ["buzz","fizzbuzz","fizz"]])
sorted_stuff = custom_sort(stuff)
assert sorted_stuff == OrderedDict([
    ('Oscar', OrderedDict([('buzz', 5), ('fizzbuzz', 15), ('fizz', 3)])),
    ('Alice', 0),
    ('Bob', [1, 2, OrderedDict([('buzz', 6), ('fizzbuzz', 7), ('fizz', 4)])]),
    ('Eve', set(['A', 'C', 'B']))
])
```

## Implementation

This uses a closure as a lightweight function factory.