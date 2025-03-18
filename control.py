from booleans import boolean_map
from operators import operator_map

def handle_wait(inputs, sprite_name, line_count, blocks):
    seconds = get_input_value(inputs["DURATION"], sprite_name, blocks=blocks)
    return f'wait({seconds})\n'

def handle_repeat(inputs, sprite_name, line_count, blocks, process_block):
    repeat_count = get_input_value(inputs["TIMES"], sprite_name, blocks=blocks)
    repeat_count = f'math.floor(tonumber({repeat_count}))'
    substack = inputs["SUBSTACK"]
    substack_code = process_substack(substack, sprite_name, blocks, process_block)
    return f'for i = 1, {repeat_count} do\n{substack_code}end\n'

def handle_forever(inputs, sprite_name, blocks, process_block):
    substack = inputs["SUBSTACK"]
    substack_code = process_substack(substack, sprite_name, blocks, process_block)
    return f'function onUpdate()\n{substack_code}end\n'

def handle_if(inputs, sprite_name, blocks, process_block):
    condition = get_input_or_boolean_value(inputs["CONDITION"], sprite_name, blocks=blocks)
    substack = inputs["SUBSTACK"]
    substack_code = process_substack(substack, sprite_name, blocks, process_block)
    return f'if ({condition}) then\n{substack_code}end\n'

def process_substack(substack, sprite_name, blocks, process_block):
    substack_code = []
    if isinstance(substack, list) and len(substack) > 1:
        substack_id = substack[1]
        while substack_id:
            if substack_id in blocks:
                process_block(substack_id, substack_code)
                substack_id = blocks[substack_id].get("next")
            else:
                substack_id = None
    return "\n".join(substack_code)

def get_input_value(input_value, sprite_name, blocks=None):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if isinstance(value, list) and len(value) > 1:
            inner_value = value[1]
            if isinstance(inner_value, str):
                return f'"{inner_value}"'
            return str(inner_value)
        return str(value)
    return "0"

def get_input_or_boolean_value(input_value, sprite_name, blocks=None):
    if isinstance(input_value, list) and len(input_value) > 1:
        block_id = input_value[1]
        if isinstance(block_id, str) and block_id in blocks:
            block = blocks[block_id]
            if block["opcode"] in boolean_map:
                return boolean_map[block["opcode"]](block["inputs"], blocks)
            if block["opcode"] in operator_map:
                return operator_map[block["opcode"]](block["inputs"], {}, blocks)
    return get_input_value(input_value, sprite_name, blocks=blocks)