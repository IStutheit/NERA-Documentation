import neat
import os
import visualize
import math
import numpy as np
import multiprocessing
import pickle
import datetime
import time
import sys
import io

#CONSTANT Declarations ---

#Define the amount of generations to run
GENERATIONS = 100
    
#Determine if you want to output at each generation or at the end of program
PRINT_AT_END = False

#with open("model.pkl", 'rb') as file:
    #autoencoder = pickle.load(file)

with open("../../data/tree_chop_data/prepped_input_data.pkl", 'rb') as file:
    input_data = pickle.load(file)

with open("../../data/tree_chop_data/prepped_output_data.pkl", 'rb') as file:
    output_data = pickle.load(file)

# Constant declaration concluded
    
def mean_squared_error(y_true, y_pred, dead_outputs):
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
    mse = mse + (10 * dead_outputs)
    return mse

def BinaryCrossEntropy(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
    term_0 = (1-y_true) * np.log(1-y_pred + 1e-7)
    term_1 = y_true * np.log(y_pred + 1e-7)
    return -np.mean(term_0+term_1, axis=0)

def error(y_true, y_pred):
    error = 0
    for i in range(len(y_true)):
        if i == 1 or i == 2 or i == 3 or i == 5 or i == 17 or i == 18:
            error += (abs(y_true[i] - y_pred[i])*10)
        else:
            error += abs(y_true[i] - y_pred[i])
    return error

def eval_genome(genome, config):
    x = 0
    score = 0
    net = neat.nn.RecurrentNetwork.create(genome, config)
    dead_outputs = count_zero_incoming_weights(genome, config)
    for i in range(len(input_data)):
        for j in range(input_data[i].shape[0]):
            output = net.activate(input_data[i][j])
            #no = np.array(o)
            #if (output).all() == 0:
                #score += 1*(1 - BinaryCrossEntropy(output,output_data[i][j]))
            #else:
            #score += 1 - ((.913 * BinaryCrossEntropy(output_data[i][j][0:2] + output_data[i][j][4:], output[0:2] + output[4:]) + .087*mean_squared_error(output_data[i][j][2:4], output[2:4])) / 2)
            score += 1 - mean_squared_error(output_data[i][j], output, dead_outputs)
        net.reset()
    return score/(len(input_data)*1200)

def count_zero_incoming_weights(genome, config):
    # Create a dictionary to count incoming connections for each output neuron
    incoming_weights = {node_id: 0 for node_id in config.genome_config.output_keys}

    # Iterate over all connections in the genome
    for connection in genome.connections.values():
        if connection.enabled and connection.key[1] in incoming_weights:
            incoming_weights[connection.key[1]] += 1

    # Count output nodes with zero incoming weights
    zero_incoming = sum(1 for count in incoming_weights.values() if count == 0)
    return zero_incoming


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #checkpoint_path = 'neat-checkpoint-42'

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)


    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.Checkpointer(generation_interval= int(GENERATIONS/3)))
    
    print("-- NEAT Starting --")
    
    if PRINT_AT_END:
        #Redirect the stdout to an IO object
        stream = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stream
   
    #Keep track of how long the process took
    start = time.time()

    if 'SLURM_NTASKS' in os.environ:
        num_cores = num_cores = int(os.getenv('SLURM_NTASKS'))  # Get the number of cores from Slurm environment variable
    else:
        num_cores = multiprocessing.cpu_count()  # Get the number of CPU cores available on the machine
    
    print(f"Number of cores used: {num_cores}")

    # Run for up to 500 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, GENERATIONS)
    
    #Finish the timer for how long Neat.run() took
    end = time.time()
    
    if PRINT_AT_END:
        #Restore stdout to original
        sys.stdout = old_stdout

    # Save the winner
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)
        


    #Display the latest generation to console
    print("\nLatest Generation:")
    data = stream.getvalue().splitlines()[-12:]
    for i in data:
        print(i)


    date = datetime.datetime.now()
    if PRINT_AT_END:
        outputFile = local_dir + "/" +"NEAT_Output_" + date.strftime("%d-%b-%Y") + ".txt"
        with open(outputFile, "w+") as f:

            f.write(date.strftime("%d-%b-%Y-%H:%M%Z"))
            f.write("\nNEAT ran for: " + str(end-start) + " seconds\n")

            f.write(stream.getvalue())

    else: 
        print(date.strftime("%d-%b-%Y-%H:%M%Z"))
        print("\nNEAT ran for: " + str(end-start) + " seconds\n")
        
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    #print('\nOutput:')
    #winner_net = neat.nn.RecurrentNetwork.create(winner, config)
##    for i, o in zip(inputs, outputs):
##        output = winner_net.activate(i)
##        #output = np.round(np.array(output))
##        print("input {!r}, expected output {!r}, got {!r}".format(i, o, output))

    # Visualize the winning network
    #visualize.draw_net(config, winner, True, filename='winner_net')
    #visualize.plot_stats(stats, ylog=False, view=True, filename='avg_fitness.svg')
    #visualize.plot_species(stats, view=True, filename='species.svg')


    
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)


