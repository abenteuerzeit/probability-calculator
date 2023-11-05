import argparse
import subprocess
import prob_calculator
from prob_calculator import Hat
import unittest
import shutil

prob_calculator.random.seed(95)


class UnitTests(unittest.TestCase):
    maxDiff = None

    def test_hat_class_contents(self):
        hat = prob_calculator.Hat(red=3, blue=2)
        actual = hat.contents
        expected = ["red", "red", "red", "blue", "blue"]
        self.assertEqual(
            actual, expected,
            'Expected creation of hat object to add correct contents.')

    def test_hat_draw(self):
        hat = prob_calculator.Hat(red=5, blue=2)
        actual = hat.draw(2)
        expected = ['blue', 'red']
        self.assertEqual(
            actual, expected,
            'Expected hat draw to return two random items from hat contents.')
        actual = len(hat.contents)
        expected = 5
        self.assertEqual(
            actual, expected,
            'Expected hat draw to reduce number of items in contents.')

    def test_prob_experiment(self):
        hat = prob_calculator.Hat(blue=3, red=2, green=6)
        probability = prob_calculator.experiment(hat=hat,
                                                 expected_balls={
                                                     "blue": 2,
                                                     "green": 1
                                                 },
                                                 num_balls_drawn=4,
                                                 num_experiments=1000)
        actual = probability
        expected = 0.272
        self.assertAlmostEqual(
            actual,
            expected,
            delta=0.01,
            msg='Expected experiment method to return a different probability.'
        )
        hat = prob_calculator.Hat(yellow=5, red=1, green=3, blue=9, test=1)
        probability = prob_calculator.experiment(hat=hat,
                                                 expected_balls={
                                                     "yellow": 2,
                                                     "blue": 3,
                                                     "test": 1
                                                 },
                                                 num_balls_drawn=20,
                                                 num_experiments=100)
        actual = probability
        expected = 1.0
        self.assertAlmostEqual(
            actual,
            expected,
            delta=0.01,
            msg='Expected experiment method to return a different probability.'
        )


def parse_hat_args(hat_arg):
    try:
        return {
            k: int(v)
            for k, v in (pair.split('=') for pair in hat_arg.split())
        }
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Hat configuration is invalid. Use 'color=count' pairs separated by spaces."
        )


def parse_expected_args(expected_arg):
    try:
        return {
            k: int(v)
            for k, v in (pair.split('=') for pair in expected_arg.split())
        }
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Expected balls configuration is invalid. Use 'color=count' pairs separated by spaces."
        )


def run_tests():
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


def color_to_emoji(color: str) -> str:
    color_map = {
        'blue': '🟦',
        'red': '🟥',
        'green': '🟩',
        'yellow': '🟨',
        'black': '⬛',
        'white': '⬜',
        'orange': '🟧'
    }
    return color_map.get(color, color)


def balls_to_emoji_string(balls):
    """
    Converts a dictionary of balls to a string representation using emojis.

    :param balls: A dictionary of the balls count for each color.
    :return: A string with emojis representing the balls.
    """
    return ''.join(f"{count}[{color_to_emoji(color)}] "
                   for color, count in balls.items())


def create_padded_string(s, max_width):
    """Create a string padded to max_width."""
    return s.ljust(max_width)[:max_width]


def get_terminal_width():
    fallback_width = 80
    try:
        columns, _ = shutil.get_terminal_size()
    except AttributeError:
        columns = fallback_width
    return columns


def run_and_print_experiments(hat_args, expected_args, num_balls_drawn,
                              num_experiments):
    terminal_width = get_terminal_width()
    success_count = 0

    exp_num_width = max(len(str(num_experiments)), 3)
    hat_contents_width = max(len(balls_to_emoji_string(hat_args)), 7)
    expected_width = max(len(balls_to_emoji_string(expected_args)), 9)
    actual_width = max(hat_contents_width, expected_width)
    result_width = 3
    draw_width = len(str(num_balls_drawn))

    min_width_per_experiment = exp_num_width + hat_contents_width + expected_width + actual_width + result_width + draw_width
    padding = 15
    min_total_width = min_width_per_experiment + padding

    vertical_layout = min_total_width > terminal_width

    for i in range(1, num_experiments + 1):
        hat = Hat(**hat_args)
        drawn_balls = hat.draw(num_balls_drawn)
        drawn_balls_freq = {
            color: drawn_balls.count(color)
            for color in set(drawn_balls)
        }
        success = all(
            drawn_balls_freq.get(color, 0) >= count
            for color, count in expected_args.items())
        if success:
            success_count += 1

        hat_str = balls_to_emoji_string(hat_args)
        expected_str = balls_to_emoji_string(expected_args)
        drawn_str = balls_to_emoji_string(drawn_balls_freq)

        if vertical_layout:
            labels = [
                'Hat contents:', 'Expected draw:', 'Actual draw:', 'Result:',
                'Balls drawn:'
            ]
            max_label_width = max(len(label) for label in labels) + 1
            max_value_width = max(len(hat_str), len(expected_str),
                                  len(drawn_str), 1, len(
                                      str(num_balls_drawn))) + 2

            format_str = "  {label:<{label_width}} {value:<{value_width}}"
            hr = f"{'=' * (max_label_width + max_value_width + 2)}"
            print(hr)
            print(f"💡 Experiment {i}:")
            print(hr)
            print(
                format_str.format(label='Hat contents:',
                                  value=hat_str,
                                  label_width=max_label_width,
                                  value_width=max_value_width))
            print(
                format_str.format(label='Expected draw:',
                                  value=expected_str,
                                  label_width=max_label_width,
                                  value_width=max_value_width))
            print(
                format_str.format(label='Actual draw:',
                                  value=drawn_str,
                                  label_width=max_label_width,
                                  value_width=max_value_width))

            combined_format_str = (
                "\n  [{result_label} {value_result}] {value_drawn} Balls drawn"
            )

            print(
                combined_format_str.format(
                    result_label='SUCCESS' if success else 'FAILURE',
                    value_result='✅' if success else '❌',
                    value_drawn=num_balls_drawn))

            print(f"{'-' * (max_label_width + max_value_width + 2)}")

        else:
            result_str = '✅' if success else '❌'
            format_str = (
                f"💡 Experiment {{exp_num:>{exp_num_width}}} : "
                f"| {{hat_contents:<{hat_contents_width}}} "
                f"| 🎯 {{expected:<{expected_width}}} "
                f"| {{actual:<{actual_width}}} "
                f"| {{result_str:<{result_width}}} | 🔄 {{num_balls_drawn:<{draw_width}}}  "
            )

            print(
                format_str.format(exp_num=i,
                                  hat_contents=hat_str,
                                  expected=expected_str,
                                  actual=drawn_str,
                                  result_str=result_str,
                                  num_balls_drawn=num_balls_drawn))

    print(f"\nTotal Successes: {success_count}/{num_experiments}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        "Simulate drawing balls from a hat and calculate the probability of a specific outcome."
    )

    parser.add_argument('--hat',
                        '-ht',
                        type=str,
                        help='Balls in the hat (e.g., "red=3 blue=2")')
    parser.add_argument('--expected',
                        '-ex',
                        type=str,
                        help='Expected balls to draw (e.g., "red=2 green=1")')
    parser.add_argument('--draw',
                        '-d',
                        type=int,
                        help='Number of balls to draw')
    parser.add_argument('--experiments',
                        '-e',
                        type=int,
                        help='Number of experiments to run')
    parser.add_argument('--test',
                        '-t',
                        action='store_true',
                        help="Run tests against prob_calculator.py")
    parser.add_argument('--shell',
                        '-sh',
                        action='store_true',
                        help="Run a shell script instead")
    parser.add_argument('--interactive',
                        '-i',
                        action='store_true',
                        help="Enter interactive mode for manual input")

    args = parser.parse_args()

    if args.test:
        run_tests()
        if not args.interactive:
            exit(0)

    if args.shell:
        subprocess.run(["./run_experiments.sh"])

    if args.interactive:
        print("Welcome to the interactive mode.")
        print(
            "You will be prompted to enter the contents of the hat, the expected outcome, the number of draws, "
            "and the number of experiments.")
        print("Enter 'exit' at any time to quit.")
        while True:
            try:
                hat_input = input(
                    "Enter hat contents (e.g., 'red=3 blue=2'): ")
                if hat_input.lower() == 'exit':
                    break
                expected_input = input(
                    "Enter expected outcome (e.g., 'red=2 green=1'): ")
                if expected_input.lower() == 'exit':
                    break
                draws_input = input("Enter number of draws: ")
                if draws_input.lower() == 'exit':
                    break
                experiments_input = input("Enter number of experiments: ")
                if experiments_input.lower() == 'exit':
                    break

                hat_contents = parse_hat_args(hat_input)
                expected_outcome = parse_expected_args(expected_input)
                number_draws = int(draws_input)
                number_experiments = int(experiments_input)

                run_and_print_experiments(hat_contents, expected_outcome,
                                          number_draws, number_experiments)
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    elif args.hat and args.expected and args.draw and args.experiments:
        hat_contents = parse_hat_args(args.hat)
        expected_outcome = parse_expected_args(args.expected)
        number_draws = args.draw
        number_experiments = args.experiments

        run_and_print_experiments(hat_contents, expected_outcome, number_draws,
                                  number_experiments)
