# UNO CSCI-4970 | Group 17 Capstone Project

## Overview

## Release Notes

Milestone 1: Basic implementation and testing of NEAT Algorithm implemented.

Milestone 2: More refined implentation of NEAT. How to format network input and output has largely been solved.
We used NEAT to evolve a population of 150 networks over 400 generations. Networks were initially had 625 inputs,
300 hidden nodes, and 22 output nodes. 6 minutes of tree chopping footage was used. This took ~100 minutes to run on 10 cores.

Milestone 3: For this milestone, we trained a model on 45 minutes of training data. The training data consists of player's chopping down trees.
In the demo video, a context window is mentioned. The context window is how many previous events the agent is aware of. During training, the agent has a context
window of 1200 time steps - this is because a given tree chop video is 60 seconds at 20 frames per second. So, the nodes in the network aren't reset back to 0
until the end of a sample is reached. In practice, the context window can be adjusted and will alter performance. 

With 45 minutes of training data, agents are demonstrating more complex behavior but it seems to be a result of overfitting. Agents in the demo video break blocks, 
slowly look down, and occassionally move backward. This is still an improvement over the previous agents, many of which would not do anything. Overall, while 
the agents aren't doing nothing, they seem to take the same or similar action repeatedly.

## Build and Install

Open a terminal to the cloned directory.

Run `pip install -e .`

This will install the package in "editable mode"

To install with dev-dependencies: 

Run `pip install -e '.[dev]`'

## MineRL Build & Install

These steps have been run & tested with:

- **Operating Systems:** Windows 11
- **Python Versions:** 3.10.6
- **Java JDKs:** Temurin Java8 JDK (You can download it from [Adoptium](https://adoptium.net/temurin/releases/?version=8))


### Step 1: Java JDK Installation

MineRL requires Java JDK 8 to run. If you haven't installed Java8 JDK yet, download and install it from the link above.

### Step 2: MineRL Setup

I used Git-Bash here just because I know it works.
It very well may build/install just fine if run from command prompt/powershell if you have the necessary executables in your path.
I just can't guarantee the build will succeed.

1. **Open Terminal Window:** Navigate to the `Utils/MineRL` directory within the cloned repository.

2. **Install MineRL:** Run the following command to install MineRL in editable mode with verbose output. The editable mode (`-e`) allows us to modify MineRL's source files without the need to reinstall the package. Verbose output (`-vvv`) helps in troubleshooting potential errors during the installation. I have found that some build errors will not show at all without this enabled.

    ```bash
    pip install -e . -vvv
    ```

    - `-e` flag: Installs the package in editable mode.
    - `-vvv` flag: Enables verbose output to display detailed information during installation.

### Step 3: Patience Is Key

Just wait for the install to complete. (Seriously, this has taken up to 2 hours on my windows machine. And even with `-vvv`, there are periods where you will have no indication of progress).
