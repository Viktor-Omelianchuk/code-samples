"""This module is designed to perform the task of the third week of
the course specializing in Python.
In this module, the base class, the class inheritor and the function that
can create class objects are implemented."""
import os
import csv
from collections import namedtuple


class CarBase:
    """Base class with common methods and attributes"""

    def __init__(self, car_type: str, brand: str, photo_file_name: str, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)
        self.car_type = car_type

    def get_photo_file_ext(self):
        """This method returns a slice of a tuple in which there are only file extensions.
        Example name.txt >> .txt """
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    """Class passenger car"""

    def __init__(
        self,
        car_type: str,
        brand: str,
        photo_file_name: str,
        carrying,
        passenger_seats_count,
    ):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    """Class truck"""

    def __init__(
        self, car_type: str, brand: str, photo_file_name: str, carrying, body_whl: str
    ):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.body_width = 0
        self.body_height = 0
        self.body_length = 0
        pline = body_whl.split("x")
        if len(pline) == 3:
            try:
                self.body_width = float(pline[0])
            except ValueError:
                pass
            try:
                self.body_height = float(pline[1])
            except ValueError:
                pass
            try:
                self.body_length = float(pline[2])
            except ValueError:
                pass

    @property
    def body_volume(self):
        """This method considers volume"""
        return self.body_width * self.body_length * self.body_height

    def get_body_volume(self):
        """This method returns volume"""
        return self.body_volume


class SpecMachine(CarBase):
    """Class special equipment"""

    def __init__(
        self, car_type: str, brand: str, photo_file_name: str, carrying: float, extra
    ):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    """The function accesses the file. Parses it line by line.
    Creates a named tuple.
    Creates class objects and returns them as a list """
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=";")
        header = next(reader)
        Cars = namedtuple("Cars", header)

        for row in reader:
            if len(row) != len(header):
                continue
            x = Cars._make(row)
            if "car" == x.car_type:
                try:
                    instance_of_class = Car(
                        x.car_type,
                        x.brand,
                        x.photo_file_name,
                        x.carrying,
                        x.passenger_seats_count,
                    )
                except (ValueError, IndexError):
                    continue
                else:
                    car_list.append(instance_of_class)
            if "truck" == x.car_type:
                try:
                    instance_of_class = Truck(
                        x.car_type, x.brand, x.photo_file_name, x.carrying, x.body_whl
                    )
                except (ValueError, IndexError):
                    continue
                else:
                    car_list.append(instance_of_class)
            if "spec_machine" == x.car_type:
                try:
                    instance_of_class = SpecMachine(
                        x.car_type, x.brand, x.photo_file_name, x.carrying, x.extra
                    )
                except (ValueError, IndexError):
                    continue
                else:
                    car_list.append(instance_of_class)

    return car_list
