import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    """The convert function (sum, cur_from, cur_to, date, requests)
    takes the amount in currency with the code cur_from and translates into cur_to
    through ruble (code: RUR) based on the specified date"""
    amount = Decimal(amount)
    response = requests.get(
        "http://www.cbr.ru/scripts/XML_daily.asp", params={"date_req": date}
    )
    soup = BeautifulSoup(response.content, "xml")
    if cur_from != "RUR":
        nominal = int(
            soup.find("CharCode", text=cur_from).find_next_sibling("Nominal").string
        )
        value = Decimal(
            soup.find("CharCode", text=cur_from)
            .find_next_sibling("Value")
            .string.replace(",", ".")
        )
        rur_value = Decimal(value * amount / nominal)
        if cur_to != "RUR":
            nominal_2 = int(
                soup.find("CharCode", text=cur_to).find_next_sibling("Nominal").string
            )
            value_2 = Decimal(
                soup.find("CharCode", text=cur_to)
                .find_next_sibling("Value")
                .string.replace(",", ".")
            )
            result = Decimal(rur_value * nominal_2 / value_2).quantize(Decimal(".0001"))
        else:
            result = Decimal(rur_value).quantize(Decimal(".0001"))
    else:
        nominal = int(
            soup.find("CharCode", text=cur_to).find_next_sibling("Nominal").string
        )
        value = Decimal(
            soup.find("CharCode", text=cur_to)
            .find_next_sibling("Value")
            .string.replace(",", ".")
        )
        result = Decimal(amount * nominal / value).quantize(Decimal(".0001"))

    return result


# print(convert(Decimal(10 ** 3), 'EUR', 'USD', "26/02/2017", requests))
