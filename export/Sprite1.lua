-- Sprite: Sprite1
local Sprite1 = {
    myVar = 0,
    testing_var = 0,
}

function onCreatePost()
    makeLuaSprite('stage')
    makeGraphic('stage', 1920, 1080, 'FFFFFF')
    setObjectCamera('stage', 'other')
    addLuaSprite('stage')

    makeLuaSprite('Sprite1', 'Sprite1')
    setObjectCamera('Sprite1', 'other')
    addLuaSprite('Sprite1')
    Sprite1.myVar = 5
    Sprite1.myVar = getProperty("Sprite1.x")
    Sprite1.myVar = Sprite1.myVar
    Sprite1.testing_var = Sprite1.testing_var + 3
    Sprite1.testing_var = Sprite1.testing_var + tonumber(getProperty("Sprite1.y"))
    Sprite1.testing_var = Sprite1.testing_var + tonumber(Sprite1.testing_var)
end
