def nice_format(iterable, use_and: bool = True, string_quotes: str = None, oxford_comma: bool = False) -> str:
    """
    Format a list nicely. Supports lazy collections.
    :param iterable: The collection to format
    :param use_and: Whether to use 'and' as the last conjunction otherwise a comma is used
    :param string_quotes: Either None or the character to quote strings with
    :param oxford_comma: Whether to use an Oxford comma (comma before and)
    :return: The formatted representation
    """

    text = ''

    first = True
    second = False
    last_element = None

    for element in iterable:
        if first:
            first = False
            second = True
        elif second:
            second = False
            text += _str(last_element, string_quotes)
        else:
            text += f', {_str(last_element, string_quotes)}'

        last_element = element

    s = _str(last_element, string_quotes)
    if second:
        text += s
    elif not first:
        if use_and:
            if oxford_comma:
                text += f', and {s}'
            else:
                text += f' and {s}'
        else:
            text += f', {s}'

    return text


def nice_print(iterable, use_and: bool = True, string_quotes: str = None, oxford_comma: bool = False):
    """
    Prints a nicely formatted list. Supports lazy collections.
    :param iterable: The list to format
    :param use_and: Whether to use 'and' as the last conjunction otherwise a comma is used
    :param string_quotes: Either None or the character to quote strings with
    :param oxford_comma: Whether to use an Oxford comma (comma before and)
    """
    print(nice_format(iterable, use_and, string_quotes, oxford_comma))


def _str(obj: object, string_quotes: str) -> str:
    if isinstance(obj, str):
        return f'"{obj}"' if string_quotes else obj
    else:
        return str(obj)
