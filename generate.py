from train import TextGenerator
import argparse
import random


def parse_args():
    parser = argparse.ArgumentParser(description='N-gramm text generation')
    parser.add_argument('--model', help='The path to the file in which the model is saved. If empty, the file to save '
                                        'will be created')
    parser.add_argument('--prefix', nargs='+', default=[], help='The beginning of the sentence (one or more words). '
                                                                'If not specified, choose the opening word at random '
                                                                'from all the words. (default: [])')
    parser.add_argument('--length', type=int, help='The length of the generated sequence.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    random.seed(0)
    print(TextGenerator.generate(args.prefix, args.length, args.model))
