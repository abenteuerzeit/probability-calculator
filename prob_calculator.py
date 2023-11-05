from collections import Counter
import random
import copy


class Hat:
    """
    Hat class representing a hat filled with balls of different colors.
    """

    def __init__(self, **balls):
        """
        Initializes a Hat with a variable number of balls.

        :param balls: A series of key-value pairs where key is the color of the ball and
                      value is the count of balls of that color.
        """
        if not balls:
            raise ValueError("Must pass in at least one ball.")
        self.contents = [
            color for color, count in balls.items() for _ in range(count)
        ]

    def draw(self, number):
        """
        Draws a number of balls from the hat at random.

        :param number: The number of balls to draw from the hat.
        :return: A list of strings representing the color of each ball drawn.
        """
        number = min(number, len(self.contents))
        draw = random.sample(self.contents, number)
        for item in draw:
            self.contents.remove(item)
        return draw


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    """
    Conducts a number of experiments to calculate the probability of drawing a certain
    combination of balls from the hat.

    :param hat: A Hat object containing balls.
    :param expected_balls: A dictionary of the expected count of each color to draw.
    :param num_balls_drawn: The number of balls to draw in each experiment.
    :param num_experiments: The total number of experiments to perform.
    :return: The probability of drawing the expected combination of balls.
    """
    count_success = 0
    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        balls_drawn = Counter(hat_copy.draw(num_balls_drawn))
        if not Counter(expected_balls) - balls_drawn:
            count_success += 1

    return count_success / num_experiments
