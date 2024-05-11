from __future__ import annotations
import pickle
import neat
import sys
import os
import cv2
import numpy as np
import time
import argparse
from snake import Snake, Food, senses, wall_collision, body_collision, check_collision
from config import block_size, bg_width, bg_height, UP, RIGHT, DOWN, LEFT
import visualize



def eval_genomes(genomes, config):
    nets = []
    snakes = []
    foods = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake())
        foods.append(Food())
        ge.append(genome)

    running = True
    while running and len(snakes) > 0:
        frame = np.zeros((bg_height, bg_width, 3), dtype=np.uint8)  # Black frame
        
        for x, (snake, apple) in enumerate(zip(snakes, foods)):
            inputs = senses(snake, apple)  # Get sensory inputs for the snake
            outputs = nets[x].activate(inputs)  # Neural network predicts the move

            max_value = max(outputs)
            max_index = outputs.index(max_value)

            directions = [UP, RIGHT, DOWN, LEFT]
            snake.change_dir(directions[max_index])  # Change direction based on the output

        # Draw snakes and food
        for snake in snakes:
            for segment in snake.get_body():
                cv2.rectangle(frame, (segment[0], segment[1]), (segment[0] + block_size, segment[1] + block_size), snake.color, -1)
        
        for apple in foods:
            cv2.rectangle(frame, (apple.position[0], apple.position[1]), (apple.position[0] + block_size, apple.position[1] + block_size), apple.color, -1)

        # Update game state and evaluate fitness
        for x in range(len(snakes) - 1, -1, -1):  # Iterate backwards to safely remove items
            snake = snakes[x]
            apple = foods[x]
            snake.move()
            snake.hunger -= 1

            if snake.hunger < 1:
                ge[x].fitness -= 10  # Penalty for starving
            if wall_collision(snake) or body_collision(snake):
                ge[x].fitness -= 5  # Penalty for collision
            if snake.hunger < 1 or wall_collision(snake) or body_collision(snake):
                nets.pop(x)
                snakes.pop(x)
                foods.pop(x)
                ge.pop(x)
                continue

            if check_collision(snake.head, apple.position):
                snake.add_to_tail()
                snake.hunger = 200
                ge[x].fitness += 10  # Reward for eating food
                apple.spawn_new_food()

        cv2.imshow("Snake AI", frame)
        key = cv2.waitKey(10)  # Slow down the frame update for better visibility
        if key == 27:  # ESC key to stop
            running = False

        time.sleep(0.0001)  # Control the speed of the game to be reasonably fast but still observable

    cv2.destroyAllWindows()




def run(config_file, demo_mode=False):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 1000)
    with open("./output/winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    print('\nBest genome:\n{!s}'.format(winner))

    visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.draw_net(config, winner, True) # opening in sublime instead of browser...

def replay_genome(config_file, genome_path="./output/winner.pkl"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    eval_genomes(genomes, config)

def main():
    parser = argparse.ArgumentParser(description='Snake AI Trainer & Tester v.0.1')
    parser.add_argument('mode', type=str, choices=["run", "replay", "exit"], default="run",
                        help='run: Train an AI with NEAT, replay: Test an already trained AI, exit: Exit the script')
    args = parser.parse_args()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')

    if args.mode == "run":
        run(config_path)
    elif args.mode == "replay":
        try:
            replay_genome(config_path)
        except FileNotFoundError:
            print("No winner file found in the output directory")
            sys.exit()
    elif args.mode == "exit":
        sys.exit()

if __name__ == '__main__':
    main()