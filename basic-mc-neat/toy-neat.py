import neat
import os
import visualize
from output_formatter import run
import json
import math
import numpy as np
import multiprocessing
import pickle

# Read the JSON file containing the flattened frames
with open('frames_data.json', 'r') as json_file:
    frames_data = json.load(json_file)

# Convert each flattened frame into a tuple representing a frame
frames_data.pop()

outputs = run("testoutput.jsonl")

##for i in range(len(frames_data)):
##    frames_data[i] = np.array(frames_data[i]).reshape(-1, 1)  # Reshape to a column vector
##    if i == 0:
##        frames_data[i] = np.concatenate((frames_data[i], np.zeros((19, 1))), axis = 0)
##    else:
##        frames_data[i] = np.concatenate((frames_data[i], np.array(outputs[i]).reshape(-1, 1)), axis = 0)


inputs = [tuple(frame) for frame in frames_data]
#print(inputs[0])
#print(len(inputs[0]))


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def binary_cross_entropy_loss(y_true, y_pred):
    """
    Computes the binary cross-entropy loss between true labels and predicted probabilities for multi-label classification.
    :param y_true: Array of true binary labels (0 or 1).
    :param y_pred: Array of predicted probabilities.
    :return: Binary cross-entropy loss.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    # Clip predictions to avoid log(0) error
    y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
    # Compute binary cross-entropy loss
    loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss

def mean_squared_error(y_true, y_pred):
    """
    Computes the mean squared error between true values and predicted values.
    :param y_true: Array of true values.
    :param y_pred: Array of predicted values.
    :return: Mean squared error.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    # Compute mean squared error
    mse = np.mean((y_true - y_pred) ** 2)
    return mse

def BinaryCrossEntropy(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
    term_0 = (1-y_true) * np.log(1-y_pred + 1e-7)
    term_1 = y_true * np.log(y_pred + 1e-7)
    return -np.mean(term_0+term_1, axis=0)

def calculate_loss(binary_loss, continuous_loss, binary_weight=0.5, continuous_weight=0.5):
    """
    Calculates a combined fitness value from binary loss and continuous loss, with optional weighting.
    :param binary_loss: The binary-cross-entropy loss for the binary action bits.
    :param continuous_loss: The mean squared error for the continuous mouse position values.
    :param binary_weight: Weight for the binary loss in the combined fitness value.
    :param continuous_weight: Weight for the continuous loss in the combined fitness value.
    :return: Combined fitness value.
    """
    # Normalize or scale the losses if necessary
    # For example:
    # binary_loss = binary_loss / max_binary_loss
    # continuous_loss = continuous_loss / max_continuous_loss

    # Combine the losses with weighting
    loss = binary_weight * binary_loss + continuous_weight * continuous_loss
    return loss

def hamming_loss(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Ensure that y_pred contains binary values by applying rounding
    y_pred_rounded = np.round(y_pred)

    # Calculate the number of mismatches between y_true and y_pred_rounded
    mismatches = np.sum(np.abs(y_true - y_pred_rounded))

    # Normalize by the total number of elements to get the average loss per label
    loss = mismatches / float(y_true.size)

    return loss

def intersection_loss(y_true, y_pred):
    y_pred = np.array(y_pred)
    y_pred_rounded = np.round(y_pred)
    y_true_set = set()
    y_pred_set = set()

    for i in range(len(y_true)):
        if y_true[i] == 1:
            y_true_set.add(i)
            
        if y_pred[i] == 1:
            y_pred_set.add(i)

    if len(y_true_set) == 0:
        return len(y_pred_set) 

    return len(y_true_set) - len(y_true_set.intersection(y_pred_set))


##def eval_genomes(genomes, config):
##    for genome_id, genome in genomes:
##        genome.fitness = 6000
##        net = neat.nn.RecurrentNetwork.create(genome, config)
##        for i, o in zip(inputs, outputs):
##            output = net.activate(i)
##            #genome.fitness -= calculate_loss(binary_cross_entropy_loss(o[2:],output[2:]), mean_squared_error(output[0:2], o[0:2]))
##            genome.fitness -= binary_cross_entropy_loss(o,output)

def eval_genome(genome, config):
    x = 0
    score = 0
    net = neat.nn.RecurrentNetwork.create(genome, config)
    for i, o in zip(inputs, outputs):
        if x % 50 == 0:
            net.reset()
        x += 1
        output = net.activate(i)
        #error -= calculate_loss(binary_cross_entropy_loss(o[2:],output[2:]), mean_squared_error(output[0:2], o[0:2]))
        no = np.array(o)
        if (no == 0).all() == 0:
            score += 1*(1 - BinaryCrossEntropy(o,output))
        else:
            score += 1 - BinaryCrossEntropy(o,output)
    return score/6000

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
    p.add_reporter(neat.Checkpointer(1))

    # Run for up to 500 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, 10000)

    # Save the winner
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
##    for i, o in zip(inputs, outputs):
##        output = winner_net.activate(i)
##        #output = np.round(np.array(output))
##        print("input {!r}, expected output {!r}, got {!r}".format(i, o, output))

    # Visualize the winning network
    visualize.plot_stats(stats, ylog=False, view=True, filename='avg_fitness.svg')
    visualize.plot_species(stats, view=True, filename='species.svg')
    visualize.draw_net(config, winner, True, filename='winner_net')


    
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)


