import os
import re
from collections import deque


def find_shortest_path(files: dict, start, end):
    """The function returns the shortest path from start to end."""
    dist = {start: [start]}
    queue = deque()
    queue.append(start)
    while len(queue):
        at = queue.popleft()
        for next in files[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                queue.append(next)
    return dist[end]


def unzip_nested_lists(nested_lists):
    """Recursively retrieves nested list items and adds them to the result variable"""
    result = []

    def recursively_extract_list_items(nested_lists):
        nonlocal result
        for element in nested_lists:
            if isinstance(element, list):
                recursively_extract_list_items(element)
            else:
                result.append(element)

    recursively_extract_list_items(nested_lists)
    return result


def build_tree(start, end, path):
    """Builds a tree of transitions between files by links"""
    list_of_all_files = os.listdir(path)
    files = dict.fromkeys(os.listdir(path))
    for file in list_of_all_files:
        with open("{}{}".format(path, file), "r") as f:
            html = f.read()
            results = re.findall(r"(?<=/wiki/)[\w()]+", html)
            files[file] = list(
                set(
                    [
                        result
                        for result in results
                        if result in list_of_all_files
                        and result != file
                        and result != start
                    ]
                )
            )
    return files


if __name__ == "__main__":
    transition_tree = build_tree("Stone_Age", "Python_(programming_language)", "wiki/")
    the_shortest_path = find_shortest_path(transition_tree, "Stone_Age", "Python_(programming_language)")
    correct_result = unzip_nested_lists(the_shortest_path)
    print(correct_result)
