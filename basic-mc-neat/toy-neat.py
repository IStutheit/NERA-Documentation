import neat
import os
import visualize
from output_formatter import run
import json
import math

# Read the JSON file containing the flattened frames
with open('frames_data.json', 'r') as json_file:
    frames_data = json.load(json_file)

# Convert each flattened frame into a tuple representing a frame
inputs = [tuple(frame) for frame in frames_data]
inputs.pop()

##inputs = [(0.0, 0.0),
##          (0.0, 1.0),
##          (1.0, 0.0),
##          (1.0, 1.0),
##          (0.0, 1.0),
##          (0.0, 0.0),
##          (1.0, 1.0)]

outputs = run("testoutput.jsonl")
print(len(inputs))
print(len(outputs))

##outputs = [(0.0,),
##           (0.0,),
##           (1.0,),
##           (0.0,),
##           (1.0,),
##           (0.0,),
##           (0.0,)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 6000
        net = neat.nn.RecurrentNetwork.create(genome, config)
        for i, o in zip(inputs, outputs):
            output = net.activate(i)
            genome.fitness -= math.sqrt((((output[0] - o[0]) ** 2)) +
                                        (((output[1] - o[1]) ** 2)) +
                                        (((output[2] - o[2]) ** 2)) +
                                        (((output[3] - o[3]) ** 2)) +
                                        (((output[4] - o[4]) ** 2)) +
                                        (((output[5] - o[5]) ** 2)) +
                                        (((output[6] - o[6]) ** 2)) +
                                        (((output[7] - o[7]) ** 2)) +
                                        (((output[8] - o[8]) ** 2)) +
                                        (((output[9] - o[9]) ** 2)) +
                                        (((output[10] - o[10]) ** 2)) +
                                        (((output[11] - o[11]) ** 2)) +
                                        (((output[11] - o[12]) ** 2)) +
                                        (((output[11] - o[13]) ** 2)) +
                                        (((output[12] - o[14]) ** 2)))

def step(x):
    return 1.0 if x >= 0 else 0

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    config.genome_config.add_activation('step', step)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Visualize the winning network
    visualize.draw_net(config, winner, True, filename='winner_net')
    visualize.plot_stats(stats, ylog=False, view=True, filename='avg_fitness.svg')
    visualize.plot_species(stats, view=True, filename='species.svg')


    
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)


