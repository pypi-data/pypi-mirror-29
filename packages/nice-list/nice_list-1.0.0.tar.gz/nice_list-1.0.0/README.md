# nice-list

[![Build Status](https://travis-ci.org/Fylipp/nice-list.svg?branch=master)](https://travis-ci.org/Fylipp/nice-list)

Pretty prints Python lists.

## Usage

```python
from nice_list import nice_print, nice_format

nice_print([1, 2, 3, 4])
# -> 1, 2, 3 and 4

nice_print(["Alice", "Bob", "Charles"])
# -> Alice, Bob and Charles

nice_print(["Alice", "Bob", "Charles"], use_and=False)
# -> Alice, Bob, Charles

nice_print(["Alice", "Bob", "Charles", 20], string_quotes='"')
# -> "Alice", "Bob", "Charles" and 20

print(nice_format(["Alice", "Bob", "Charles"]))
# -> Alice, Bob and Charles
```

## Installation

```sh
pip install nice_list
```

## Testing

```sh
python nice_list_test.py
```

## License

MIT.
