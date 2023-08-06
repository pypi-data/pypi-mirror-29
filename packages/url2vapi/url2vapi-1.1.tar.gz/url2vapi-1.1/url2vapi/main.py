"""Core of the package, contains only one function responsible for url
parsing/processing.
"""

import re

from urllib.parse import urlparse

from . import exceptions, models


def _parse_tuple(delimiter, cast_to):
    def fun(val):
        return tuple([cast_to(val) for val in val.split(delimiter)])

    return fun


def parse_pattern(pattern):
    cast_types = {
        'number': lambda val: int(float(val)),
        'double': float,
        'string': str,
        'bool': bool,
    }

    if not pattern:
        raise exceptions.InvalidInputPattern("Pattern cannot be empty")

    # first group is optional and it is prefix, this group precedes < that
    # marks beginning of the variable
    # then follows mandatory name of the variable
    # then follows optional type of variable (default to string if not
    # provided)
    # then follows optional delimiter variable (important only for tuples,
    # defaults to .)
    # then follows optional suffix (should behind closing >)
    elements = re.findall(
        r'([\w,._-]+)?<([\w_\.]+)(:([\w\[\]]+))?(:([\w,.|_-]+))?>([\w,._-]+)?',
        pattern)

    groups = []

    for (
            prefix, element, separator, item_type,
            separator, delimiter, suffix) in elements:

        if not item_type:
            item_type = 'string'

        if not delimiter:
            delimiter = '.'

        if item_type.startswith('tuple'):
            item_type, tuple_element = re.match(
                r'(tuple)(\[\w+\])?', item_type).groups()

            tuple_element = tuple_element.strip(
                '[]') if tuple_element else 'string'

            if tuple_element not in cast_types:
                raise exceptions.InvalidInputPattern(
                    "Elements of the tuple cannot be cast into unrecognised "
                    "item type ({}) for variable {}".format(
                        item_type, element))
        elif item_type not in cast_types:
            raise exceptions.InvalidInputPattern(
                "There is unrecognised item type ({}) for variable{}".format(
                    item_type, element))

        if (element, item_type) in groups:
            raise exceptions.InvalidInputPattern(
                "Element ({}) present twice on a pattern".format(element))

        cast_to = _parse_tuple(delimiter, cast_types[tuple_element]) \
            if item_type == 'tuple' else cast_types[item_type]

        groups.append((element, cast_to, prefix, suffix))

        del separator
        del delimiter

    return groups


def split(url, pattern=''):
    """Function takes a string and parses it into restful api relevant chunks.

    Second argument is optional. It allows to predefine that given url has to
    have certain structure. For example we can enforce that version or
    namespace is present. If not provided it will default to:

        <version:double>/<rest_of_url>

    Pattern consists of backslash separated groups. Each group member needs to
    be defined as:

        <name>

    or

        <name:type>

    Where type can be number, double, string, tuple or bool (default: string).
    """
    parsed_url = urlparse(url)

    if pattern == '' or not pattern.endswith('<...>'):
        pattern += '<...>' if not pattern or pattern[-1] == '/' else '/<...>'

    if parsed_url.scheme not in ('http', 'https'):
        raise exceptions.UnrecognisedProtocol(
            "Only http or https is ok with us")

    groups = parse_pattern(pattern)

    url = parsed_url.path

    url = url[1:] if url.startswith('/') else url

    kwargs = {}

    while url:
        if not groups:
            break

        name, cast_to, prefix, suffix = groups.pop(0)

        idx = url.find('/')

        if name == '...':
            if groups:
                raise exceptions.InvalidInputPattern(
                    "Argpars <...> cannot be followed by any other group")

            value = url
            url = ''
            name = 'remainder'

        else:
            value = url[:idx]
            url = url[idx + 1:]

            value = value[len(prefix):] \
                if prefix and value.startswith(prefix) else value
            value = value[:len(suffix) * -1] \
                if suffix and value.endswith(suffix) else value

            try:
                value = cast_to(value)
            except (NameError, TypeError, ValueError):
                raise exceptions.InvalidUrlPattern(
                    "Unable to cast value ({}) using ({})".format(
                        value, cast_to))

        kwargs[name] = {
            'value': value,
            'prefix': prefix,
            'suffix': suffix,
        }

    if 'remainder' not in kwargs:
        kwargs['remainder'] = {
            'value': '',
        }

    if parsed_url.params:
        kwargs['remainder']['value'] += ';' + parsed_url.params

    elif parsed_url.query:
        kwargs['remainder']['value'] += '?' + parsed_url.query

    elif parsed_url.fragment:
        kwargs['remainder']['value'] += '#' + parsed_url.fragment

    return models.ApiUrl(
        protocol=parsed_url.scheme,
        domain=parsed_url.hostname,
        port=parsed_url.port,
        remainder=kwargs.pop('remainder')['value'],
        **kwargs
    )
