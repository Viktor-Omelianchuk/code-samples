from collections import defaultdict
import os
import json
import argparse


def save_storage(storage, path_to_file):
    with open(path_to_file, "w") as file:
        json.dump(storage, file)


def load_storage(path_to_file):
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            return defaultdict(list, json.load(file))
    else:
        return defaultdict(list)


def main(path_to_file, key, value):
    if value:
        storage = load_storage(path_to_file)
        storage[key].append(value)
        save_storage(storage, path_to_file)
    else:
        storage = load_storage(path_to_file)
        print(*storage[key], sep=", ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, help=" random text")
    parser.add_argument(
        "--val", default=None, required=False, type=str, help="random_text"
    )
    args = parser.parse_args()
    key = args.key
    value = args.val
    path_to_file = "/tmp/storage.data"
    main(path_to_file, key, value)
