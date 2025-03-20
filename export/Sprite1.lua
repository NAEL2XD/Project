-- Sprite: Sprite1
function onCreatePost()
    makeLuaSprite('stage')
    makeGraphic('stage', 1920, 1080, 'FFFFFF')
    setObjectCamera('stage', 'other')
    addLuaSprite('stage')

    makeLuaSprite('Sprite1', 'Sprite1')
    setObjectCamera('Sprite1', 'other')
    addLuaSprite('Sprite1')
debugPrint("Sprite1:1: " .. tonumber("5") % tonumber("3"))
debugPrint("Sprite1:2: " .. tonumber("i") % tonumber("j"))
debugPrint("Sprite1:3: " .. math.floor(tonumber("1.5")))
debugPrint("Sprite1:4: " .. math.floor(tonumber("l")))

end
