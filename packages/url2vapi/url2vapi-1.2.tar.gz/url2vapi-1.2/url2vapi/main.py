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

    # first group is optional and it is prefix, this group precedes < that
    # marks beginning of the variable
    # then follows mandatory name of the variable
    # then follows optional type of variable (default to string if not
    # provided)
    # then follows optional delimiter variable (important only for tuples,
    # defaults to .)
    # then follows optional suffix (should behind closing >)
    elements = re.findall(
        r'([\w,._-]+)?<([\w_]+)(:([\w\[\]]+))?(:([\w,.|_-]+))?>([\w,._-]+)?',
        pattern)

    groups = []
    prefixes = []
    suffixes = []

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

        if prefix:
            ambigous_prefix = [
                val for val in prefixes if val in prefix]

            if ambigous_prefix:
                raise exceptions.InvalidInputPattern(
                    "Prefix {} is conflicting with prefix {} "
                    "(use more distinct values)".format(
                        prefix, ",".join(ambigous_prefix)))

            prefixes.append(prefix)

        if suffix:
            ambigous_suffix = [
                val for val in suffixes if val in suffix]

            if ambigous_suffix:
                raise exceptions.InvalidInputPattern(
                    "Suffix {} is conflicting with suffix {} "
                    "(use more distinct values)".format(
                        suffix, ",".join(ambigous_suffix)))

            suffixes.append(suffix)

    return groups


def _parse_section(value, cast_to, prefix, suffix):
    if prefix and not value.startswith(prefix):
        return
    elif prefix:
        value = value[len(prefix):]

    if suffix and not value.endswith(suffix):
        return
    elif suffix:
        value = value[:len(suffix) * -1]

    try:
        return cast_to(value)
    except (NameError, TypeError, ValueError):
        pass


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

    url = parsed_url.path[1:]

    groups = parse_pattern(pattern)
    sections = url.split('/')

    kwargs = {}

    for group_name in [tmp[0] for tmp in groups]:
        kwargs[group_name] = None

    while sections:
        section = sections.pop(0)

        # pylint: disable=consider-using-enumerate
        for idx in range(len(groups)):
        # pylint: enable=consider-using-enumerate
            name, cast_to, prefix, suffix = groups[idx]

            val = _parse_section(section, cast_to, prefix, suffix)

            if val is not None:
                kwargs[name] = {
                    'value': val,
                    'prefix': prefix,
                    'suffix': suffix,
                }
                groups.pop(idx)
                break

        if not groups:
            break

    remainder = '/'.join(sections)

    if not remainder:
        remainder = '/'

    if parsed_url.params:
        remainder += ';' + parsed_url.params

    elif parsed_url.query:
        remainder += '?' + parsed_url.query

    elif parsed_url.fragment:
        remainder += '#' + parsed_url.fragment

    return models.ApiUrl(
        protocol=parsed_url.scheme,
        domain=parsed_url.hostname,
        port=parsed_url.port,
        remainder=remainder,
        **kwargs
    )
