class FileReader:
    """FileReader class helps to read from files"""

    def __init__(self, file_name: str):
        self._file_name = file_name

    def read(self):
        """This method tries to read the file."""
        try:
            with open(self._file_name, "r") as file:
                return file.read()
        except IOError:
            return ""

