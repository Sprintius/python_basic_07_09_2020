import json

data = {
    1 : 23434,
    2 : 'hello',
    'three' : [1, 2, 4],
}

j_data = json.dumps(data)
print(j_data)