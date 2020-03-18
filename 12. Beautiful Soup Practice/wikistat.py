import unittest
from bs4 import BeautifulSoup


def parse(path_to_file):
    """Parser for collecting statistics from Wikipedia pages."""

    with open(path_to_file, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        body = soup.find(id="bodyContent")

    # the number of images (img) with a width of at least 200
    imgs = len(body.find_all("img", width=lambda x: int(x or 0) > 199))

    # number of headers (h1, h2, h3, h4, h5, h6), the first letter of the text inside which
    # matches capital letter E, T or C
    headers = sum(
        1
        for tag in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        if tag.get_text()[0] in "ETC"
    )

    # the number of lists (ul, ol) not nested in other lists
    lists = sum(
        1 for tag in body.find_all(["ol", "ul"]) if not tag.find_parent(["ol", "ul"])
    )

    # The length of the maximum sequence of links between which there are no other tags
    linkslen = 0

    for a in body.find_all("a"):
        current_streak = 1

        for tag in a.find_next_siblings():
            if tag.name == "a":
                current_streak += 1
            else:
                break

        linkslen = current_streak if current_streak > linkslen else linkslen

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ("wiki/Stone_Age", [13, 10, 12, 40]),
            ("wiki/Brain", [19, 5, 25, 11]),
            ("wiki/Artificial_intelligence", [8, 19, 13, 198]),
            ("wiki/Python_(programming_language)", [2, 5, 17, 41]),
            ("wiki/Spectrogram", [1, 2, 4, 7]),
        )

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == "__main__":
    unittest.main()
