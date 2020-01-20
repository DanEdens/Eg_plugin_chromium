
attribute = ('this is a test',)


def _format_handler(value):
    if isinstance(value, tuple):
        func = format_tuple
    elif isinstance(value, list):
        func = format_list
    elif isinstance(value, dict):
        func = format_dict
    elif isinstance(value, unicode):
        func = format_unicode
    elif isinstance(value, str):
        func = format_string
    else:
        def func(v, *_):
            return str(v)
    return func


def format_tuple(data, attr_len, indent):
    output = []
    for value in data:
        i = attr_len + len(', '.join(output)) + 2
        output += [_format_handler(value)(value, i, indent + 4)]

    indent = ' ' * indent

    res = '('
    if len(output) == 1:
        res += output[0] + ',)'
    elif output:
        res += ', '.join(output) + ')'
    else:
        res += ')'

    if len(res) + attr_len > 80:
        value_indent = ',\n' + indent + ' ' * 4
        res = '(\n' +  value_indent[2:] + value_indent.join(output)
        res += '\n' + indent + ')'

    return res

def format_list(data, attr_len, indent):
    output = []
    for value in data:
        i = attr_len + len(', '.join(output)) + 2
        output += [_format_handler(value)(value, i, indent + 4)]
    indent = ' ' * indent

    res = '['
    if output:
        res += ', '.join(output)
    res += ']'

    if len(res) + attr_len > 80:
        value_indent = ',\n' + indent + ' ' * 4
        res = '[\n' + value_indent[2:] + value_indent.join(output)
        res += '\n' + indent + ']'

    return res


def text_formatter(data, attr_len, indent):
    if isinstance(data, unicode):
        t = unicode
    else:
        t = str

    output = ''

    multiLine = attr_len + len(t(data)) > 80

    if multiLine:
        new_data = []
        while data:
            jump = min([len(data), 67])
            value = data[:jump]
            if '\n' in value:
                jump = value.find('\n') + 1
            elif value.endswith('.') or value.endswith(' '):
                pass
            elif ' ' in value:
                jump = value.rfind(' ') + 1

                new_data += [t(data[:jump])]
            data = data[jump:]
        i = '\n' + ' ' * (indent + 4)
        output += '(\n'
        output += i.join(list('%r' % item for item in  new_data))

        for item in new_data:
            output += i + '%r\n' % t(item)
        output += ' ' * indent + ')'
    else:
        output += '%r' % t(data)

    return output

def format_str(data, attr_len, indent):
    return text_formatter(data, attr_len, indent)

def format_unicode(data, attr_len, indent):
    return text_formatter(data, attr_len, indent)

def format_dict(data, attr_len, indent):
    output = []
    i = attr_len + len(str(data)) + 2

    if i + indent > 79:
        for key, value in data.items():
            i = indent + 8 + len(key)
            output += [
                repr(str(key)) +
                ': ' +
                _format_handler(value)(value, i, indent + 4)
            ]




def formatter(value, indent):
    if isinstance(value, tuple):

    elif isinstance(value, list):


    elif isinstance(value, dict):

    elif isinstance(value, (str, unicode)):
