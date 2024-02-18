import neat
import os
import visualize

inputs = [(0.0, 0.0),
          (0.0, 1.0),
          (1.0, 0.0),
          (1.0, 1.0),
          (0.0, 1.0),
          (0.0,0.0),
          (1.0, 1.0)]

outputs = [(0.0,),
           (0.0,),
           (1.0,),
           (0.0,),
           (1.0,),
           (0.0,),
           (0.0,)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 7.0
        net = neat.nn.RecurrentNetwork.create(genome, config)
        for i, o in zip(inputs, outputs):
            output = net.activate(i)
            genome.fitness -= (output[0] - o[0]) ** 2

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

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

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
    for i, o in zip(inputs, outputs):
        output = winner_net.activate(i)
        print("input {!r}, expected output {!r}, got {!r}".format(i, o, output))

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


