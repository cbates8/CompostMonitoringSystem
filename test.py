import json

x = '{ "name":"John", "age":30}'

y = json.loads(x)

print(y["name"])