# TODO - Implement this function
# I want to get a better understanding of the json data and what
# we might want from the two files we aren't currently using before I implement this.




# import json

# def load_json_file(file_path):
#     """Load and return the content of the specified JSON file."""
#     with open(file_path, 'r') as file:
#         return json.load(file)

# def load_json_lines_file(file_path):
#     """Load and return the content of a .jsonl file as a list of JSON objects."""
#     data = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             data.append(json.loads(line))
#     return data

# def filter_actions_based_on_config(actions, config):
#     """Filter and adjust actions based on config settings."""
#     if not config.get('pauseOnLostFocus', False):
#         actions = [action for action in actions if not action.get('isGuiOpen', False)]
#     return actions

# def extract_actions(actions, config):
#     """Extract relevant data from actions, potentially adjusted by config."""
#     mouse_movements = []
#     keyboard_actions = []
#     inventory_changes = []

#     for action in actions:
#         mouse_movements.append({
#             'x': action['mouse']['x'],
#             'y': action['mouse']['y'],
#             'dx': action['mouse']['dx'],
#             'dy': action['mouse']['dy'],
#             'dwheel': action['mouse']['dwheel'],
#             'buttons': action['mouse']['buttons'],
#             'newButtons': action['mouse']['newButtons']
#         })

#         keyboard_actions.append({
#             'keys': action['keyboard']['keys'],
#             'newKeys': action['keyboard']['newKeys'],
#             'chars': action['keyboard']['chars']
#         })

#         inventory_changes.append(action['inventory'])

#     sensitivity_factor = config.get('mouseSensitivity', 1)
#     for movement in mouse_movements:
#         movement['dx'] *= sensitivity_factor
#         movement['dy'] *= sensitivity_factor

#     return mouse_movements, keyboard_actions, inventory_changes

# def main(config_file_path, actions_file_path):
#     config = load_json_file(config_file_path)
#     actions = load_json_lines_file(actions_file_path)
    
#     filtered_actions = filter_actions_based_on_config(actions, config)
#     mouse_movements, keyboard_actions, inventory_changes = extract_actions(filtered_actions, config)
    
#     print("Extracted Mouse Movements (first 3):", json.dumps(mouse_movements[:3], indent=4))
#     print("Extracted Keyboard Actions (first 3):", json.dumps(keyboard_actions[:3], indent=4))
#     print("Extracted Inventory Changes (first 3):", json.dumps(inventory_changes[:3], indent=4))



# import json

# def load_json_lines_file(file_path):
#     """Load and return the content of a .jsonl file as a list of JSON objects."""
#     data = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             data.append(json.loads(line))
#     return data

# def extract_actions(actions):
#     """Extract all relevant action data."""
#     mouse_movements = []
#     keyboard_actions = []
#     inventory_changes = []

#     for action in actions:
#         mouse_movements.append(action['mouse'])
#         keyboard_actions.append(action['keyboard'])
#         inventory_changes.append(action['inventory'])
    
#     return mouse_movements, keyboard_actions, inventory_changes

# def track_inventory_changes(inventory_changes):
#     """Track changes in inventory between frames."""
#     changes = []
#     for i in range(1, len(inventory_changes)):
#         current_inventory = {item['type']: item['quantity'] for item in inventory_changes[i]}
#         previous_inventory = {item['type']: item['quantity'] for item in inventory_changes[i-1]}
        
#         inventory_diff = {'added': [], 'removed': [], 'changed': []}
        
#         # Check for added items or quantity changes
#         for item, quantity in current_inventory.items():
#             if item not in previous_inventory:
#                 inventory_diff['added'].append({item: quantity})
#             elif quantity != previous_inventory[item]:
#                 inventory_diff['changed'].append({item: quantity - previous_inventory[item]})
        
#         # Check for removed items
#         for item, quantity in previous_inventory.items():
#             if item not in current_inventory:
#                 inventory_diff['removed'].append({item: quantity})
        
#         if inventory_diff['added'] or inventory_diff['removed'] or inventory_diff['changed']:
#             changes.append(inventory_diff)
    
#     return changes

# def main(config_file_path, actions_file_path):
#     # Load actions data from a JSON Lines file
#     actions = load_json_lines_file(actions_file_path)
    
#     # Extract relevant action data
#     mouse_movements, keyboard_actions, inventory_changes = extract_actions(actions)
    
#     # Track significant inventory changes
#     inventory_change_log = track_inventory_changes(inventory_changes)
    
#     print("Extracted Mouse Movements (first 3):", json.dumps(mouse_movements[:3], indent=4))
#     print("Extracted Keyboard Actions (first 3):", json.dumps(keyboard_actions[:3], indent=4))
#     print("Inventory Changes (first 3):", json.dumps(inventory_change_log[:3], indent=4))



# # Call the main function with the paths to your files
# if __name__ == "__main__":
#     # Specify the path to your config and actions JSON files here
#     config_file_path = r'/Users/samblooms/Downloads/Player129-f153ac423f61-20210617-171344-options.json'
#     actions_file_path = r'/Users/samblooms/Dev/school/Capstone/CSCI4970-MC-GamePlayingBot/data/temp_training/Player129-f153ac423f61-20210617-171344.jsonl'
#     main(config_file_path, actions_file_path)


#//============================================================ 

import json

def load_json_lines_file(file_path):
    """Load and return the content of a .jsonl file as a list of JSON objects."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def process_inventory_changes(actions):
    """Process inventory changes between frames to identify added, removed, or changed items."""
    inventory_changes = []
    previous_inventory = {}

    for action in actions:
        current_inventory = {item['type']: item['quantity'] for item in action['inventory']}
        added = {k: v for k, v in current_inventory.items() if k not in previous_inventory}
        removed = {k: previous_inventory[k] for k in previous_inventory if k not in current_inventory}
        changed = {k: (current_inventory[k] - previous_inventory[k]) for k in current_inventory if k in previous_inventory and previous_inventory[k] != current_inventory[k]}
        
        inventory_changes.append({
            "added": added,
            "removed": removed,
            "changed": changed
        })
        
        previous_inventory = current_inventory

    return inventory_changes

def list_inventory_changes_with_frames(inventory_changes):
    """List all inventory changes along with the frames they occur."""
    changes_list = []

    for index, change in enumerate(inventory_changes):
        if change['added'] or change['removed'] or change['changed']:
            changes_list.append({
                "frame": index,
                "added": change['added'],
                "removed": change['removed'],
                "changed": change['changed']
            })
    
    return changes_list

# def main(file_path):
#     actions = load_json_lines_file(file_path)
    
#     # Process inventory changes
#     inventory_changes = process_inventory_changes(actions)

#     # List all changes along with the frames they occur in
#     inventory_changes_with_frames = list_inventory_changes_with_frames(inventory_changes)

#     # Displaying first 10 for brevity; you can adjust as needed or process further
#     print("Inventory Changes (first 10):", json.dumps(inventory_changes_with_frames[:10], indent=4))

# def process_player_and_mouse_movements(actions):

#     """Process player and mouse movements to identify significant changes."""
#     movement_changes = []
#     previous_position = None
#     previous_mouse_movement = None



#     for action in actions:

#         current_position = (action['xpos'], action['ypos'], action['zpos'])
#         current_mouse_movement = (action['mouse']['dx'], action['mouse']['dy'])

#         position_changed = previous_position is not None and current_position != previous_position
#         mouse_movement_changed = previous_mouse_movement is not None and current_mouse_movement != (0.0, 0.0)

#         movement_changes.append({

#             "position_changed": position_changed,
#             "mouse_movement_changed": mouse_movement_changed,
#             "current_position": current_position if position_changed else None,
#             "current_mouse_movement": current_mouse_movement if mouse_movement_changed else None
#         })
#         previous_position = current_position
#         previous_mouse_movement = current_mouse_movement


#     return movement_changes



# # Adjust the main function to include processing for player and mouse movements

# def main(file_path):

#     actions = load_json_lines_file(file_path)

#     # Process inventory and movement changes
#     inventory_changes = process_inventory_changes(actions)
#     movement_changes = process_player_and_mouse_movements(actions)



#     # List all inventory changes along with the frames they occur in
#     inventory_changes_with_frames = list_inventory_changes_with_frames(inventory_changes)



#     # For demonstration, print summaries of both inventory and movement changes

#     #print("Inventory Changes (sample):", json.dumps(inventory_changes_with_frames[:5], indent=4))
#     #print("Inventory Changes (sample):", json.dumps(inventory_changes_with_frames, indent=4))

#     #print("Movement Changes (sample):", json.dumps(movement_changes[:5], indent=4))
#     #print("Movement Changes (sample):", json.dumps(movement_changes, indent=4))

#     #print the total number of movement changes
#     #print("Total Movement Changes: ", len(movement_changes))
#     #print the total number of inventory changes
#     #print("Total Inventory Changes: ", len(inventory_changes_with_frames))

#     #print the total number of inventory additions
#     total_additions = 0
#     for change in inventory_changes_with_frames:
#         total_additions += len(change['added'])
#     print("Total Inventory Additions: ", total_additions)

#     #print the total number of inventory removals
#     total_removals = 0
#     for change in inventory_changes_with_frames:
#         total_removals += len(change['removed'])
#     print("Total Inventory Removals: ", total_removals)


#     #print the total number of position changes
#     total_position_changes = 0
#     for change in movement_changes:
#         if change['position_changed']:
#             total_position_changes += 1

#     print("Total Position Changes: ", total_position_changes)

#     #print the total number of mouse movement changes
#     total_mouse_movement_changes = 0
#     for change in movement_changes:
#         if change['mouse_movement_changed']:
#             total_mouse_movement_changes += 1

#     print("Total Mouse Movement Changes: ", total_mouse_movement_changes)

#     #print the total mouse movement in the x direction
#     total_x_movement = 0
#     for change in movement_changes:
#         if change['current_mouse_movement']:
#             total_x_movement += change['current_mouse_movement'][0]
#     print("Total X Movement: ", total_x_movement)

#     #print the total mouse movement in the y direction
#     total_y_movement = 0
#     for change in movement_changes:
#         if change['current_mouse_movement']:
#             total_y_movement += change['current_mouse_movement'][1]
#     print("Total Y Movement: ", total_y_movement)

#     #print the total player movement in the x direction
#     total_x_player_movement = 0
#     for change in movement_changes:
#         if change['current_position']:
#             total_x_player_movement += change['current_position'][0]
#     print("Total X Player Movement: ", total_x_player_movement)

#     #print the total player movement in the y direction
#     total_y_player_movement = 0
#     for change in movement_changes:
#         if change['current_position']:
#             total_y_player_movement += change['current_position'][1]
#     print("Total Y Player Movement: ", total_y_player_movement)

#     #print the total player movement in the z direction
#     total_z_player_movement = 0
#     for change in movement_changes:
#         if change['current_position']:
#             total_z_player_movement += change['current_position'][2]
#     print("Total Z Player Movement: ", total_z_player_movement)

# if __name__ == "__main__":
#     #file_path = 'path_to_your_file.jsonl'  # Update this to the path of your JSON Lines file
#     file_path = r'/Users/samblooms/Dev/school/Capstone/CSCI4970-MC-GamePlayingBot/data/temp_training/Player129-f153ac423f61-20210617-171344.jsonl'
#     main(file_path)

# #============================================================
    


import json

def load_json_lines_file(file_path):
    """Load and return the content of a .jsonl file as a list of JSON objects."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def process_inventory_changes(actions):
    """Process inventory changes between frames to identify added, removed, or changed items."""
    inventory_changes = []
    previous_inventory = {}

    for action in actions:
        current_inventory = {item['type']: item['quantity'] for item in action['inventory']}
        added = {k: v for k, v in current_inventory.items() if k not in previous_inventory}
        removed = {k: previous_inventory[k] for k in previous_inventory if k not in current_inventory}
        changed = {k: (current_inventory[k] - previous_inventory[k]) for k in current_inventory if k in previous_inventory and previous_inventory[k] != current_inventory[k]}
        
        inventory_changes.append({
            "added": added,
            "removed": removed,
            "changed": changed
        })
        
        previous_inventory = current_inventory

    return inventory_changes

def list_inventory_changes_with_frames(inventory_changes):
    """List all inventory changes along with the frames they occur."""
    changes_list = []

    for index, change in enumerate(inventory_changes):
        if change['added'] or change['removed'] or change['changed']:
            changes_list.append({
                "frame": index,
                "added": change['added'],
                "removed": change['removed'],
                "changed": change['changed']
            })
    
    return changes_list

def process_player_and_mouse_movements(actions):
    """Process player and mouse movements to identify significant changes."""
    movement_changes = []
    previous_position = None
    previous_mouse_movement = None

    for action in actions:
        current_position = (action['xpos'], action['ypos'], action['zpos'])
        current_mouse_movement = (action['mouse']['dx'], action['mouse']['dy'])

        position_changed = previous_position is not None and current_position != previous_position
        mouse_movement_changed = previous_mouse_movement is not None and current_mouse_movement != (0.0, 0.0)

        movement_changes.append({
            "position_changed": position_changed,
            "mouse_movement_changed": mouse_movement_changed,
            "current_position": current_position if position_changed else None,
            "current_mouse_movement": current_mouse_movement if mouse_movement_changed else None
        })
        previous_position = current_position
        previous_mouse_movement = current_mouse_movement

    return movement_changes

def calculate_total_displacement(movement_changes):
    """Calculate the total displacement for player and mouse movements."""
    total_displacement = {
        "x_player_displacement": 0,
        "y_player_displacement": 0,
        "z_player_displacement": 0,
        "x_mouse_displacement": 0,
        "y_mouse_displacement": 0
    }
    
    previous_position = None
    for change in movement_changes:
        if change['position_changed'] and previous_position is not None:
            total_displacement["x_player_displacement"] += abs(change['current_position'][0] - previous_position[0])
            total_displacement["y_player_displacement"] += abs(change['current_position'][1] - previous_position[1])
            total_displacement["z_player_displacement"] += abs(change['current_position'][2] - previous_position[2])
        if change['mouse_movement_changed']:
            total_displacement["x_mouse_displacement"] += abs(change['current_mouse_movement'][0])
            total_displacement["y_mouse_displacement"] += abs(change['current_mouse_movement'][1])
        previous_position = change['current_position'] if change['position_changed'] else previous_position

    return total_displacement

def calculate_bounding_box(movement_changes):
    """Calculate the bounding box of the region visited."""
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    for change in movement_changes:
        if change['position_changed']:
            x, y, z = change['current_position']
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            min_z, max_z = min(min_z, z), max(max_z, z)

    # Handle case where no movement occurred
    if min_x == float('inf'):
        min_x = min_y = min_z = max_x = max_y = max_z = 0

    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "min_z": min_z,
        "max_z": max_z
    }


def process_button_presses_and_gameEvents(actions):
    """Process button presses and game events."""
    button_presses = []
    gameEvents = []

    for index, action in enumerate(actions):
        if 'newButtons' in action['mouse'] or 'newKeys' in action['keyboard']:
            button_presses.append({
                "frame": index,
                "mouse_buttons": action['mouse'].get('newButtons', []),
                "keyboard_keys": action['keyboard'].get('newKeys', [])
            })

        if action.get('stats', {}):
            gameEvents.append({"frame": index, "achievements": action['stats']})

    return button_presses, gameEvents

def process_game_events(actions):
    """Process game events to accurately capture achievements for each frame."""
    gameEvents = []

    for index, action in enumerate(actions):
        # Initialize an empty dictionary for each frame to ensure events don't carry over
        frame_events = {}

        # Only add events that are explicitly mentioned in the current frame
        if 'stats' in action:
            frame_events = action['stats']

        gameEvents.append({"frame": index, "achievements": frame_events})

    return gameEvents

def process_stats_changes_only(actions):
    """Process stats to record changes only when they occur."""
    processed_stats = []
    previous_stats = None

    for index, action in enumerate(actions):
        current_stats = action.get('stats', {})
        # Initialize previous_stats in the first iteration
        if previous_stats is None:
            previous_stats = current_stats
        
        # Compare current_stats with previous_stats to identify changes
        stats_changes = {key: value for key, value in current_stats.items() if previous_stats.get(key) != value}
        
        if stats_changes or index == 0:  # Always include the first frame for context
            processed_stats.append({"frame": index, "stats_changes": stats_changes})
        
        previous_stats = current_stats  # Update previous_stats for the next iteration

    return processed_stats

def main(file_path):
    actions = load_json_lines_file(file_path)
    
    # Process inventory and movement changes
    inventory_changes = process_inventory_changes(actions)
    movement_changes = process_player_and_mouse_movements(actions)
    button_presses, gameEvents = process_button_presses_and_gameEvents(actions)
    

    # Calculate total displacement
    total_displacement = calculate_total_displacement(movement_changes)
    bounding_box = calculate_bounding_box(movement_changes)

    #print("Sample gameEvents:", json.dumps(gameEvents[:5], indent=4))  # Displaying first 5 for brevity
    #print("Sample button presses:", json.dumps(button_presses[:5], indent=4))  # Displaying first 5 for brevity

    #print("Sample gameEvents:", json.dumps(gameEvents, indent=4))  # Displaying first 5 for brevity
    #print("Sample button presses:", json.dumps(button_presses, indent=4))  # Displaying first 5 for brevity

    # Applying the revised function to process stats changes only
    processed_stats_changes = process_stats_changes_only(actions)

    # Printing processed stats changes to verify the script is functioning as intended
    #print("Processed Stats Changes (first instances):", json.dumps(processed_stats_changes[:5], indent=4))
    #print("Processed Stats Changes (first instances):", json.dumps(processed_stats_changes, indent=4)) #this is broken. It prints time_since_rest and time_since_death and play_one_minute every single frame.

    #filter out all stats changes that contain minecraft.custom:minecraft.time_since_rest, minecraft.custom:minecraft.play_one_minute, and minecraft.custom:minecraft.time_since_death. But keep all other events.
    #these occur every frame though, so we can't just filter the frames that contain them. We need to filter the events themselves.
    filtered_stats_changes = processed_stats_changes.copy()
    for change in filtered_stats_changes:
        for key in change['stats_changes'].copy():
            if key == 'minecraft.custom:minecraft.time_since_rest' or key == 'minecraft.custom:minecraft.play_one_minute' or key == 'minecraft.custom:minecraft.time_since_death':
                change['stats_changes'].pop(key)
    
    #print("Filtered Stats Changes (first instances):", json.dumps(filtered_stats_changes[:5], indent=4))
    #print("Filtered Stats Changes (first instances):", json.dumps(filtered_stats_changes, indent=4))
                
    #only print the filtered_stats_changes that contain events
    filtered_stats_changes_with_events = []
    for change in filtered_stats_changes:
        if change['stats_changes']:
            filtered_stats_changes_with_events.append(change)
    print("Filtered Stats Changes with Events (first instances):", json.dumps(filtered_stats_changes_with_events[:5], indent=4))
    




    # Output results
    print("Total Displacement:", json.dumps(total_displacement, indent=4))
    print("Bounding Box:", json.dumps(bounding_box, indent=4))

if __name__ == "__main__":
    #file_path = 'path_to_your_file.jsonl'  # Update this to the path of your JSON Lines file
    file_path = r'/Users/samblooms/Dev/school/Capstone/CSCI4970-MC-GamePlayingBot/data/temp_training/Player129-f153ac423f61-20210617-171344.jsonl'
    main(file_path)
