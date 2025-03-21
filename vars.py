import main
import operators

def handle_setvariableto(inputs, fields, sprite_name, variables, blocks):
    variable_name = main.sanitize_variable_name(fields["VARIABLE"][0])
    if len(inputs["VALUE"]) == 3:
        if len(inputs["VALUE"][1]) == 3:
            value = main.sanitize_variable_name(inputs["VALUE"][1][1])
        else:
            value = operators.get_input_or_number_value(inputs["VALUE"], variables, blocks, sprite_name)
        return f'{sprite_name}.{variable_name} = {value}'
    else:
        value = inputs["VALUE"][1]
        if isinstance(value, list):
            return f'{sprite_name}.{variable_name} = {value[1]}'
        return f'{sprite_name}.{variable_name} = "{value}"'

def handle_changevariableby(inputs, fields, sprite_name, variables, blocks):
    variable_name = main.sanitize_variable_name(fields["VARIABLE"][0])
    if len(inputs["VALUE"]) == 3:
        if len(inputs["VALUE"][1]) == 3:
            value = main.sanitize_variable_name(inputs["VALUE"][1][1])
        else:
            value = operators.get_input_or_number_value(inputs["VALUE"], variables, blocks, sprite_name)
        return f'{sprite_name}.{variable_name} = {sprite_name}.{variable_name} + tonumber({value})'
    else:
        value = inputs["VALUE"][1]
        if isinstance(value, list):
            return f'{sprite_name}.{variable_name} = {sprite_name}.{variable_name} + {value[1]}'
        return f'{sprite_name}.{variable_name} = {sprite_name}.{variable_name} + {value}'

def handle_addtolist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    item = operators.get_input_or_number_value(inputs["ITEM"], variables, blocks, sprite_name)
    return f'table.insert({sprite_name}.{list_name}, tostring({item}))'

def handle_deleteoflist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    index = operators.get_input_or_number_value(inputs["INDEX"], variables, blocks, sprite_name)
    return f'table.remove({sprite_name}.{list_name}, tonumber({index}))'

def handle_deletealloflist(fields, sprite_name):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    return f'{sprite_name}.{list_name} = {{}}'

def handle_insertatlist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    index = operators.get_input_or_number_value(inputs["INDEX"], variables, blocks, sprite_name)
    item = operators.get_input_or_number_value(inputs["ITEM"], variables, blocks, sprite_name)
    return f'table.insert({sprite_name}.{list_name}, tonumber({index}), tostring({item}))'

def handle_replaceitemoflist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    index = operators.get_input_or_number_value(inputs["INDEX"], variables, blocks, sprite_name)
    item = operators.get_input_or_number_value(inputs["ITEM"], variables, blocks, sprite_name)
    return f'{sprite_name}.{list_name}[tonumber({index})] = tostring({item})'

def handle_itemoflist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    index = operators.get_input_or_number_value(inputs["INDEX"], variables, blocks, sprite_name)
    return f'{sprite_name}.{list_name}[tonumber({index})]'

def handle_lengthoflist(inputs, fields, sprite_name, variables, blocks):
    list_name = main.sanitize_variable_name(fields["LIST"][0])
    return f'#{sprite_name}.{list_name}'

var_map = {
    "data_setvariableto": handle_setvariableto,
    "data_changevariableby": handle_changevariableby,
    "data_addtolist": handle_addtolist,
    "data_deleteoflist": handle_deleteoflist,
    "data_deletealloflist": handle_deletealloflist,
    "data_insertatlist": handle_insertatlist,
    "data_replaceitemoflist": handle_replaceitemoflist,
    "data_itemoflist": handle_itemoflist,
    "data_lengthoflist": handle_lengthoflist
}