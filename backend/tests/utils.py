import random
import string


def random_string(length=3):
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))
