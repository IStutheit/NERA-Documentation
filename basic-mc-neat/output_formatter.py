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
                if key not in keys:
                    keys[key] = kiterator
                    kiterator = kiterator + 1

    for json_str in json_objects:
        if json_str.strip():  # Skip empty lines
            data = json.loads(json_str)
            keysTemp = [0 for _ in range(len(keys))]

            for key in data.get('keyboard', None).get('keys', None):
                keysTemp[keys[key]] = 1

            output.append((data.get('mouse', None).get('x', None)/2211.0, data.get('mouse', None).get('y', None)/383.0, *keysTemp))

            if output[-1][0] > max_x:
                max_x = output[-1][0]
            if output[-1][0] > max_y:
                max_y = output[-1][1]
    #print(output)
    #print(len(output))
    print(max_x)
    print(max_y)
    return output
                

#run(file_path)
    
