import os
import uuid


class File:
    def __init__(self, path):
        self.path = path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def write(self, content):
        with open(self.path, "w") as file:
            return file.write(content)

    def read(self):
        with open(self.path, "r") as file:
            return file.read()

    def __add__(self, obj):
        new_path = os.path.join(os.path.dirname(self.path), str(uuid.uuid4().hex))
        new_file = type(self)(new_path)
        new_file.write(self.read() + obj.read())

        return new_file

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, "r") as file:
            file.seek(self.current_position)

            line = file.readline()
            if not line:
                self.current_position = 0
                raise StopIteration("EOF")

            self.current_position = file.tell()
            return line