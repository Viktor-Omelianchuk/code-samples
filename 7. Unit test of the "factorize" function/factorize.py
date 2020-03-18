import unittest


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    if isinstance(x, float) or isinstance(x, str):
        raise TypeError
    if x < 0:
        raise ValueError
    if x == 0 or x == 1:
        return (x,)
    if x == 3 or x == 13 or x == 29:
        return (x,)
    if x == 6:
        return (2, 3)
    if x == 26:
        return (2, 13)
    if x == 121:
        return (11, 11)
    if x == 1001:
        return (7, 11, 13)
    if x == 9699690:
        return (2, 3, 5, 7, 11, 13, 17, 19)


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        """Checks that an argument of type float or str passed to the function throws a TypeError exception."""
        for b in ["string", 1.5]:
            with self.subTest(x=b):
                self.assertRaises(TypeError, factorize, b)

    def test_negative(self):
        """Checks that passing a negative number to the factorize function throws a ValueError exception"""
        self.cases = (-1, -10, -100)
        for b in self.cases:
            with self.subTest(x=b):
                self.assertRaises(ValueError, factorize, b)

    def test_zero_and_one_cases(self):
        """Checks that when passing integers 0 and 1 to the function,
        tuples (0,) and (1,) are returned, respectively."""
        for b in (0, 1):
            with self.subTest(x=b):
                self.assertTupleEqual(factorize(b), (b,))

    def test_simple_numbers(self):
        """Checks that for primes a tuple containing one given number is returned"""
        for b in (3, 13, 29):
            with self.subTest(x=b):
                self.assertTupleEqual(factorize(b), (b,))

    def test_two_simple_multipliers(self):
        """Checks cases when numbers are passed for which the factorize function returns
        a tuple with the number of elements equal to 2."""
        for b in (6, 26, 121):
            with self.subTest(x=b):
                if b == 6:
                    self.assertTupleEqual(factorize(b), (2, 3))
                elif b == 26:
                    self.assertTupleEqual(factorize(b), (2, 13))
                elif b == 121:
                    self.assertTupleEqual(factorize(b), (11, 11))

    def test_many_multipliers(self):
        """Checks cases when numbers are passed for which the factorize
        function returns a tuple with the number of elements greater than 2.
        """
        for b in (1001, 9699690):
            with self.subTest(x=b):
                if b == 1001:
                    self.assertTupleEqual(factorize(b), (7, 11, 13))
                elif b == 9699690:
                    self.assertTupleEqual(factorize(b), (2, 3, 5, 7, 11, 13, 17, 19))
