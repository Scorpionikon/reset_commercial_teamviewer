from random import randint


class MAC:

    def __init__(self, mac: str):
        self._mac = mac.split(":")
        self.mac = [int(m, 16) for m in self._mac]

    def reset_mac(self):
        self.mac = [randint(0, 255) for _ in self.mac]

    @staticmethod
    def _from_deci(number):
        number = hex(number).lstrip("0x").rstrip("L")
        if len(number) is 1:
            number = "0" + number
        return number

    def __str__(self):
        str_mac = ":".join([self._from_deci(c) for c in self.mac])
        return str_mac


def random_mac():
    random = [randint(0, 250) for _ in range(6)]
    return str(MAC(":".join([MAC._from_deci(c) for c in random])))