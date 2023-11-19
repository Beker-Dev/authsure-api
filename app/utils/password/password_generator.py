import string
import random


def password_generator(length=20) -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation.replace('"', ''), length))
