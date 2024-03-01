import json

file_path = "testoutput.jsonl"
keys = {}
output = []

def run(file_path):
    max_x = 0
    max_y = 0

    kiterator = 0
    with open(file_path, 'r') as file:
        content = file.read()

    # Assuming each JSON object is separated by a newline
    json_objects = content.split('\n')

    for json_str in json_objects:
        if json_str.strip():  # Skip empty lines
            data = json.loads(json_str)
            for key in data.get('keyboard', None).get('keys', None):
                if key not in keys and key != "key.keyboard.f11" and key != "key.keyboard.escape":
                    keys[key] = kiterator
                    kiterator = kiterator + 1

    #print(keys)

    for json_str in json_objects:
        if json_str.strip():  # Skip empty lines
            if json_objects.index(json_str) > 0:
                dataPrev = json.loads(json_objects[json_objects.index(json_str)-1])
            else:
                dataPrev = json.loads(json_str)
            data = json.loads(json_str)

            #left = 1 if data.get('mouse', None).get('x', None) < dataPrev.get('mouse', None).get('x', None) else 0
            #right = 1 if data.get('mouse', None).get('x', None) > dataPrev.get('mouse', None).get('x', None) else 0
            #up = 1 if data.get('mouse', None).get('y', None) > dataPrev.get('mouse', None).get('y', None) else 0
            #down = 1 if data.get('mouse', None).get('y', None) < dataPrev.get('mouse', None).get('y', None) else 0

            dx = data.get('mouse', None).get('dx', None)/714
            dy = data.get('mouse', None).get('dy', None)/310

            keysTemp = [0 for _ in range(len(keys))]

            for key in data.get('keyboard', None).get('keys', None):
                if key in keys:
                    keysTemp[keys[key]] = 1

            if len(data.get('mouse', None).get('buttons', None)) == 0:
                output.append((dx,
                               dy,
                               0,
                               0,
                               *keysTemp))

            elif 0 in data.get('mouse', None).get('buttons', None) and 1 not in data.get('mouse', None).get('buttons', None):
                output.append((dx,
                               dy,
                               1,
                               0,
                               *keysTemp))

            elif 1 in data.get('mouse', None).get('buttons', None) and 0 not in data.get('mouse', None).get('buttons', None):
                output.append((dx,
                               dy,
                               0,
                               1,
                               *keysTemp))

            elif 1 in data.get('mouse', None).get('buttons', None) and 0 in data.get('mouse', None).get('buttons', None):
                output.append((dx,
                               dy,
                               1,
                               1,
                               *keysTemp))

            if abs(output[-1][0]) > max_x:
                max_x = abs(output[-1][0])
            if abs(output[-1][1]) > max_y:
                max_y = abs(output[-1][1])
    #print(output[4319])
    #print(len(output[0]))
    #print(max_x)
    #print(max_y)
    #print(keys)
    return output
                

#run(file_path)
    
