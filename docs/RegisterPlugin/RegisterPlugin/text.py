from formatter import formatter

VALUE = '''
class Text:
    # add variables with string that you want to be able to have translated
    # using the language editor in here
    {attributes}
    {actions}
'''

ACTION = '''
    class {class_name}:
        name = {name}
        description = {description}
        {attributes}
'''

ACTION_ATTRIBUTE = '        {attribute} = {value}\n'
PLUGIN_ATTRIBUTE = '    {attribute} = {value}\n'


def build(plugin):
    actions = []
    attributes = []

    for attribute in plugin.text_attributes:
        attributes += [PLUGIN_ATTRIBUTE.format(**attribute)]

    for action in plugin.actions:
        action_attributes = []

        for attribute, value in action.text_attributes:
            value = formatter(value)


            action_attributes += [ACTION_ATTRIBUTE.format(**attribute)]

        actions += [
            ACTION.format(
                name=action.name,
                description=action.description,
                attributes=''.join(action_attributes)
            )
        ]


