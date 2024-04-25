import gym
import minerl
import neat
import pickle
import cv2
import numpy as np
import tensorflow as tf

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     "model_generation/config")

# Load the winner
with open("model_generation/winner.pkl", 'rb') as f:
    winner = pickle.load(f)
    
winner_net = neat.nn.RecurrentNetwork.create(winner, config)

autoencoder = tf.keras.models.load_model('autoencoder.h5')

env = gym.make("MineRLBasaltFindCave-v0")
print(env.action_space)

obs = env.reset()

done = False

action = env.action_space.sample()

for key in action:
        if isinstance(action[key], int):
            action[key] = 0
        elif isinstance(action[key], float):
            action[key] = 0.0
        elif isinstance(action[key], list) and all(isinstance(x, float) for x in action[key]):
            action[key] = [0.0 for _ in action[key]]
        elif isinstance(action[key], str):
            action[key] = 'none'  # Assuming 'none' is a valid value for string actions

x = 0

while not done:
    #print("test")
    if x%1200 == 0:
        winner_net.reset()
    x = x+1

    gobs = cv2.cvtColor(obs['pov'], cv2.COLOR_BGR2GRAY)

    # Resize to 25x25
    gobs = cv2.resize(gobs, (64, 64))

    # Flatten the image to a 625x1 array
    #gobs = gobs.flatten().reshape(4096, 1)

    gobs = gobs/255

    gobs = [gobs]

    gobs = np.stack(gobs, axis=0)

    gobs = autoencoder.predict(gobs, verbose=0)[0]

    output = winner_net.activate(gobs)
    output[2] = output[2]#*1.8
    output[3] = output[3]#*.7
    
    
    if (output[0] >= .5):
        action["attack"] = 1
    else:
        action["attack"] = 0
        
    if (output[1] >= .5):
        action["back"] = 1
    else:
        action["back"] = 0

    action["camera"] = [output[3], output[2]]
        
    if (output[4] >= .5):
        action["drop"] = 1
    else:
        action["drop"] = 0

    if (output[5] >= .5):
        action["forward"] = 1
    else:
        action["forward"] = 0
        
    if (output[6] >= .5):
        action["hotbar.1"] = 1
    else:
        action["hotbar.1"] = 0
        
    if (output[7] >= .5):
        action["hotbar.2"] = 1
    else:
        action["hotbar.2"] = 0
        
    if (output[8] >= .5):
        action["hotbar.3"] = 1
    else:
        action["hotbar.3"] = 0
        
    if (output[9] >= .5):
        action["hotbar.4"] = 1
    else:
        action["hotbar.4"] = 0
        
    if (output[10] >= .5):
        action["hotbar.5"] = 1
    else:
        action["hotbar.5"] = 0
        
    if (output[11] >= .5):
        action["hotbar.6"] = 1
    else:
        action["hotbar.6"] = 0
        
    if (output[12] >= .5):
        action["hotbar.7"] = 1
    else:
        action["hotbar.7"] = 0
        
    if (output[13] >= .5):
        action["hotbar.8"] = 1
    else:
        action["hotbar.8"] = 0
        
    if (output[14] >= .5):
        action["hotbar.9"] = 1
    else:
        action["hotbar.9"] = 0  
    
        
    if (output[15] >= .5):
        action["inventory"] = 0
    else:
        action["inventory"] = 0
        
    if (output[16] >= .5):
        action["jump"] = 1
    else:
        action["jump"] = 0
        
    if (output[17] >= .5):
        action["left"] = 1
    else:
        action["left"] = 0
        
    if (output[18] >= .5):
        action["right"] = 1
    else:
        action["right"] = 0
        
    if (output[19] >= .5):
        action["sneak"] = 1
    else:
        action["sneak"] = 0
        
    if (output[20] >= .5):
        action["sprint"] = 1
    else:
        action["sprint"] = 0
        
    if (output[21] >= .5):
        action["use"] = 1
    else:
        action["use"] = 0
    
            
    action["ESC"] = 0
##    print()
##    print()
##    print()
##    print(output)
##    print()
##    print(action)
##    print()
##    print()
##    print()
    obs, reward, done, _ = env.step(action)
    env.render()
