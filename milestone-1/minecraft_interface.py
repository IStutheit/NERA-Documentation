import gym
import minerl
import neat
import pickle
import cv2
import numpy as np

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     "C:/Users/admin/Desktop/CSCI4970Repo/CSCI4970-MC-GamePlayingBot/basic-mc-neat/config")

# Load the winner
with open("C:/Users/admin/Desktop/CSCI4970Repo/CSCI4970-MC-GamePlayingBot/basic-mc-neat/winner.pkl", 'rb') as f:
    winner = pickle.load(f)
    
winner_net = neat.nn.RecurrentNetwork.create(winner, config)

env = gym.make('MineRLBasaltFindCave-v0')
print(env.action_space)

obs = env.reset()

done = False

while not done:

    gobs = cv2.cvtColor(obs['pov'], cv2.COLOR_BGR2GRAY)

    # Resize to 25x25
    gobs = cv2.resize(gobs, (25, 25))

    # Flatten the image to a 625x1 array
    gobs = gobs.flatten().reshape(625, 1)

    gobs = gobs/255

    output = winner_net.activate(gobs)
    output[2] = output[0]*714
    output[3] = output[1]*310
    
    # Take a random action
    action = env.action_space.sample()
    # In BASALT environments, sending ESC action will end the episode
    # Lets not do that]
    for key in action:
        if isinstance(action[key], int):
            action[key] = 0
        elif isinstance(action[key], float):
            action[key] = 0.0
        elif isinstance(action[key], list) and all(isinstance(x, float) for x in action[key]):
            action[key] = [0.0 for _ in action[key]]
        elif isinstance(action[key], str):
            action[key] = 'none'  # Assuming 'none' is a valid value for string actions
    
    if (output[0] >= .5):
        action["attack"] = 1
    if (output[1] >= .5):
        action["back"] = 1

    action["camera"] = [output[2], output[3]]
        
    if (output[4] >= .5):
        action["drop"] = 1
    if (output[5] >= .5):
        action["forward"] = 1
        
    if (output[6] >= .5):
        action["hotbar.1"] = 1
    if (output[7] >= .5):
        action["hotbar.2"] = 1
    if (output[8] >= .5):
        action["hotbar.3"] = 1
    if (output[9] >= .5):
        action["hotbar.4"] = 1
    if (output[10] >= .5):
        action["hotbar.5"] = 1
    if (output[11] >= .5):
        action["hotbar.6"] = 1
    if (output[12] >= .5):
        action["hotbar.7"] = 1
    if (output[13] >= .5):
        action["hotbar.8"] = 1
    if (output[14] >= .5):
        action["hotbar.9"] = 1
    
        
    if (output[15] >= .5):
        action["inventory"] = 1
    if (output[16] >= .5):
        action["jump"] = 1
    if (output[17] >= .5):
        action["left"] = 1
    if (output[18] >= .5):
        action["right"] = 1
    if (output[19] >= .5):
        action["sneak"] = 1
    if (output[20] >= .5):
        action["sprint"] = 1
    if (output[21] >= .5):
        action["use"] = 1
    
            
    action["ESC"] = 0
    obs, reward, done, _ = env.step(action)
    env.render()
