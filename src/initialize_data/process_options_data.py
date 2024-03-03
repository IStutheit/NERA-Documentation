import json

def parse_options_file(options_file_path):
    # Read the JSON file
    with open(options_file_path, 'r') as file:
        options_data = json.load(file)
    
    # Extract relevant data. Here, we assume all data in the file is relevant.
    # However, this function can be customized to extract specific fields if necessary.
    extracted_data = {
        'game_settings': {},
        'control_settings': {}
    }
    
    # Assuming the options data is categorized into game settings and control settings
    for key, value in options_data.items():
        if key.startswith('key_'):
            extracted_data['control_settings'][key] = value
        else:
            extracted_data['game_settings'][key] = value
    
    return extracted_data

# Example usage
if __name__ == '__main__':
    options_file_path = 'path_to_your_options_json_file.json'  # Replace this with the actual path
    options_data = parse_options_file(options_file_path)
    print(json.dumps(options_data, indent=4))
