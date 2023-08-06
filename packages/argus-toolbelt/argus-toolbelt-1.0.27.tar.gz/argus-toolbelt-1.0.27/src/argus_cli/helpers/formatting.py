import keyword
from typing import Iterable
from re import sub, match
from typing import List, Dict, Callable
from terminaltables import AsciiTable
from string import capwords

def to_caterpillar_case(camel_cased_string: str) -> str:
    """Replace UpperCase with upper-case and upperCase_Name with upper-case-name and splits into the dictionary levels

    :param str camel_cased_string: CamelCasedString to convert
    :rtype: str
    :returns: caterpillar-cased-string
    """
    if match(r".*[a-z](ID).*", camel_cased_string):
        camel_cased_string = camel_cased_string.replace("ID", "Id")
    return sub('(?<!^)(?=[A-Z])', '-', camel_cased_string).replace("_", "-").lower().split(".")[-1]


def to_snake_case(camel_cased_string: str) -> str:
    """Replace UpperCase with upper-case and upperCase_Name with upper_case_name and splits into the dictionary levels

    :param str camel_cased_string: CamelCasedString to convert
    :rtype: str
    :returns: snake_cased_string
    """
    if match(r".*[a-z](ID).*", camel_cased_string):
        camel_cased_string = camel_cased_string.replace("ID", "Id")
    return sub('(?<!^)(?=[A-Z])', '_', camel_cased_string).lower().split(".")[-1]


def to_camel_case(snake_cased_string: str) -> str:
    """Turns snake_cased_strings into snakeCasedStrings, reversing to_snake_case

    :param str snake_cased_string: snake_cased_string to convert
    :returns: camelCasedString
    """
    first, *others = snake_cased_string.split("_")

    # Turn ID back into uppercase
    return sub(r'(?<=[a-z])(Id)(?=[A-Za-z_]|$)',
               lambda match: match[1].upper(),
               ''.join([first.lower(), *map(str.title, others)]))


def python_name_for(javascript_type: str) -> str:
    """Find the Python name for a javascript type
    
    :param str javascript_type: JavaScript type name, e.g array, string, integer
    :returns: Name for the type in python
    :rtype: str
    """
    alternatives = {
        'integer': 'int',
        'number': 'int',
        'float': 'float',
        'object': 'dict',
        'array': 'list',
        'bool': 'bool',
        'boolean': 'bool',
        'string': 'str',
        'null': 'None'
    }

    if javascript_type in alternatives:
        return alternatives[javascript_type.lower()]
    else:
        return javascript_type

def to_safe_name(argument: str) -> str:
    """Python prevents us from using the built-in keywords as parameter names in
    functions, so if the API requests any of these keywords, we escape them with
    an underscore and provide a method to escape and unescape them

    :param str argument: Argument name to escape, if necessary
    :returns: _argument if the argument was unsafe
    """
    if keyword.iskeyword(argument):
        return "_%s" % argument
    return argument

def from_safe_name(argument: str) -> str:
    """Python prevents us from using the built-in keywords as parameter names in
    functions, so if the API requests any of these keywords, we escape them with
    an underscore and provide a method to escape and unescape them

    :param str argument: Argument name to escape, if necessary
    :returns: _argument if the argument was unsafe
    """
    if argument.startswith("_") and keyword.iskeyword(argument.replace("_", "")):
        return argument.replace("_", "")
    return argument


def clear() -> None:
    """Clears the terminal"""
    print("\033[H\033[J")


def ask(question: str) -> bool:
    """Prompts user with a a yes/no terminal prompt and returns True if the user answered yes

    :param bool question:
    :return:
    """
    yN = input("%s (Y/n) " % question)
    return yN.strip().lower() == 'y'


def table(data: Iterable[Dict[str, str]], keys: Iterable[str], format: Callable = None, title: str = None) -> str:
    """Accepts a list of dicts or objects, and keys to extract from it, then creates a 
    table that can be printed to the terminal.

    :param list data: Dataset to print as a table
    :param list keys: Keys to extract from each dict or object
    :param callable format: Optional formatter, will be called as format(value, key)
    :param str title: Title to print over the table (optional)
    :returns: str
    """
    # Print updates and let user accept before performing updates
    table_data = [
        list(map(capwords, keys)),
    ]

    if not format:
        format = lambda value, key: value

    for row in data:
        table_data.append([
            format(row.key if hasattr(row, key) else row[key], key=key)
            for key in keys
        ])

    return AsciiTable(table_data, title=title if title else None).table


def red(text: str, **kwargs) -> str:
    return "\033[1;31m%s\033[0m" % text

def green(text: str, **kwargs) -> str:
    return "\033[1;32m%s\033[0m" % text