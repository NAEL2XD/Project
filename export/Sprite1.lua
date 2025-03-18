-- Sprite: Sprite1
function onCreatePost()
    makeLuaSprite('stage')
    makeGraphic('stage', 1920, 1080, 'FFFFFF')
    setObjectCamera('stage', 'other')
    addLuaSprite('stage')

    makeLuaSprite('Sprite1', 'Sprite1')
    setObjectCamera('Sprite1', 'other')
    addLuaSprite('Sprite1')
--[[Error processing block b:
Traceback (most recent call last):
  File "c:\Users\nael\Downloads\Project\main.py", line 99, in process_block
    result = block_map[opcode](block["inputs"], block["fields"])
  File "c:\Users\nael\Downloads\Project\main.py", line 61, in <lambda>
    "control_if": lambda inputs, fields: control.handle_if(inputs, sprite_name, blocks, process_block),
  File "c:\Users\nael\Downloads\Project\control.py", line 18, in handle_if
    condition = get_input_or_boolean_value(inputs["CONDITION"], sprite_name, blocks=blocks)
  File "c:\Users\nael\Downloads\Project\control.py", line 51, in get_input_or_boolean_value
    if block["opcode"] in boolean_map:
NameError: name 'boolean_map' is not defined
]]
end
