import requests
from datetime import datetime
from collections import Counter


def calc_age(uid):
    """Client to the VK API, which will consider the distribution of the ages of friends for the specified user.
    That is, the username or user_id of the user is input, the output is a list of pairs
    (<age>, <number of friends with that age>) sorted in descending order by the second key (number of friends) and
    ascending by the first key (age)"""

    if isinstance(uid, str):
        payload = {
            "v": "5.71",
            "access_token": "17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711",
            "user_ids": uid,
        }

        response = requests.get("https://api.vk.com/method/users.get", params=payload)
        id_response = response.json()["response"][0]["id"]
    else:
        id_response = uid

    payload_2 = {
        "v": "5.71",
        "access_token": "17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711",
        "user_id": id_response,
        "fields": "bdate",
    }

    r = requests.get("https://api.vk.com/method/friends.get", params=payload_2)

    users_with_bdate = [
        i["bdate"] for i in r.json()["response"]["items"] if "bdate" in i
    ]

    counter = Counter()
    for user in users_with_bdate:
        try:
            year = datetime.strptime(user, "%d.%m.%Y").year
            counter[2019 - year] += 1
        except ValueError:
            continue
    return sorted(counter.items(), key=lambda x: (-x[1], x[0]))


if __name__ == "__main__":
    # res = calc_age("reigning")
    # print(res)
