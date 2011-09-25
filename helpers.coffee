p = console.log

# Source: http://coffeescriptcookbook.com/chapters/classes_and_objects/cloning
clone = (obj) ->
  return obj if not obj? or typeof obj isnt 'object'

  newInstance = new obj.constructor()
  for key of obj
    newInstance[key] = clone obj[key] # recursion for deep clone

  return newInstance

exports.p = p
exports.clone = clone
