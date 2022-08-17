# C-Py-Py

```python
from cpp import *

x = (cpp)[std::vector<int>v({1, 2, 3})]
x.push_back(4)
(cpp)[std::cout] << "Vector x: " << x << (cpp)[std::endl]
# -> prints 'Vector x: [1, 2, 3]'
for i in auto& x:
    (cpp)[std::cout] << "Incrementing " << i << "..." << (cpp)[std::endl]
    # -> prints 'Incrementing 1...', 'Incrementing 2...', etc.
    i += 1

(cpp)[std::cout] << "Vector after: " << x << (cpp)[std::endl]
# -> prints 'Vector after: [2, 3, 4, 5]'
```

## How?

### Template notation

The `<>` template notation was quite difficult to pull off. Python has a weird concept of multiple-boolean-operators, so the following:

```python
x = (cpp)[std::vector<int>v({1, 2, 3})]
```

is equivalent to

```python
x = (cpp)[std::((vector < int) and (int > v({1, 2, 3})))]
```

We can then overwrite the less than operator for the object `vector` to simply return True, so that it's negligible:

```python
x = (cpp)[std::(True and (int > v({1, 2, 3})))]
x = (cpp)[std::(int > v({1, 2, 3}))]
```

Now we can overwrite the less than operator on a different class (`v`, in this case) so that it simply takes in a fully formed vector object as `self` and a type as the comparison, then tries to transform that into a new vector of the type in the comparison. This would be equivalent to:

```python
x = (cpp)[std::(v({1, 2, 3}))]
```

### C++-style namespacing

Nearly there. For the namespacing (`::`), we turn to the only place in the Python syntax where adjacent colons are allowed: slice notation. The code above is equivalent to:

```python
x = cpp[slice(std, None, v({1, 2, 3}))]
```

We can define `cpp` to be an instance of a class that overrides the `__getitem__` method to simply return the rightmost part of the slice:

```python
class cpp:
    def __getitem__(self, other: slice):
        return other.step
cpp = cpp()
```

Now the code is equivalent to just:

```python
x = v({1, 2, 3})
```

where `v` is essentially a thin wrapper around `list`.

### cout

`cout` performs a small sleight-of-hand. Since Python is evaluated left-to-right, we have to have the `<<` operator reduce each of the expressions down into a single format string, then pass that to `endl` to actually do the printing. We do this by making `cout`.__lshift__() return a `Coutable`:

```python
class _Coutable:
    def __init__(self, o) -> None:
        self._total_str: str = format(o)

    def __lshift__(self, other: Any) -> Self:
        if other is endl:
            print(self._total_str)
        self._total_str = self._total_str + format(other)
        return self
```

This class will just keep accumulating objects' formatted representations until it hits endl, when it will print everything out.

### Taking references

Unfortunately, Python's `for _ in _:` syntax is pretty rigid, and won't allow any operations in-between for and in, so we have to stick the `auto&` on the right side. This 

## Why?

Scientists are hard at work trying to come up with an answer to that question.
