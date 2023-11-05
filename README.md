# Probability Calculator

## Overview

This repository contains the implementation of a Probability Calculator that simulates drawing balls from a hat and calculates the probability of drawing a specific combination of balls. This project is a part of the curriculum at [freeCodeCamp](https://www.freecodecamp.org/learn/scientific-computing-with-python/scientific-computing-with-python-projects/probability-calculator).

## Description

Suppose you have a hat containing balls of various colors. The Probability Calculator can determine the approximate probability of drawing a particular combination of balls, without replacement. The program creates a `Hat` class where each instance represents a hat filled with balls of different colors and quantities. It then runs a specified number of experiments to estimate the probability of drawing a certain number of balls of various colors.

## Features

- Implement a `Hat` class with methods to add balls and draw them at random.
- Calculate probabilities based on large numbers of experiments to provide an approximation.
- Test the program's functionality with a suite of unit tests.
- Interactive mode for manual experimentation.
- Emoji representation for visual representation of the balls and outcomes.

## Getting Started

### Dependencies

- Python 3.x
- No additional Python packages are required to run the main script.
- Bash shell for running the shell script included for Unix users.

### Installing and Running

1. Clone this repository or download the source code.
2. Ensure you have Python 3.x installed on your machine.
3. Run the program using the command line:


   ```bash
   python main.py --hat "red=3 blue=2" --expected "red=2 blue=1" --draw 5 --experiments 1000
   ```


4. To run unit tests to validate the program's functionality:


   ```bash
   python main.py --test
   ```


5. For an interactive experience:


   ```bash
   python main.py --interactive
   ```


6. Execute the bash script directly on Unix systems:


   ```bash
   ./run_experiments.sh <iterations>
   ```

### Help

If you need help with the command-line arguments, use:

```bash
python main.py -h
```

## Example

Creating and using a `Hat` object:

```python
hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={"red":2,"green":1},
                  num_balls_drawn=5,
                  num_experiments=2000)
```