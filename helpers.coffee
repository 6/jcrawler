exports.p = p = console.log

# Source: http://coffeescriptcookbook.com/chapters/classes_and_objects/cloning
exports.clone = clone = (obj) ->
  return obj if not obj? or typeof obj isnt 'object'
  newInstance = new obj.constructor()
  for key of obj
    newInstance[key] = clone obj[key] # recursion for deep clone
  return newInstance

# Source: https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Date
exports.date_string = date_string = (d) ->
   pad = (n) -> return if n<10 then "0#{n}" else n
   "#{d.getUTCFullYear()}#{pad d.getUTCMonth()+1}#{pad d.getUTCDate()}#{pad d.getUTCHours()}#{pad d.getUTCMinutes()}#{pad d.getUTCSeconds()}"

# inclusive random range
# Source: http://www.admixweb.com/2010/08/24/javascript-tip-get-a-random-number-between-two-integers/
exports.random_range = random_range = (from, to) ->
  val = Math.floor(Math.random() * (to - from + 1) + from)
  # in case Math.random() can produce 1.0 (does it?)
  val = to if val > to
  val

# simple random sampling w/o replacement
exports.srswor = srswor = (list, n) ->
  new_list = []
  while new_list.length < n or list.length == 0
    rand_idx = random_range(0, list.length - 1)
    new_list.push(list.splice(rand_idx, 1)[0])
  new_list

# Source: http://stackoverflow.com/questions/646628/javascript-startswith
exports.startsWith = startsWith = (str, start) ->
  str.slice(0, start.length) == start
