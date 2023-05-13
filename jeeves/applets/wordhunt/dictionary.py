import os


current_dir = os.path.dirname(os.path.realpath(__file__))


def load_dict():
    with open(os.path.join(current_dir, "dictionary.txt")) as f:
        return {word.lower() for word in f.read().splitlines()}
