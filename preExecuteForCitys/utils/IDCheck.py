# _*_ coding=utf-8 _*_
import re
from datetime import date


class IdentityCardWrongException(Exception):
    pass


class IDCheck(object):
    @classmethod
    def get_id_card_verify_number(cls, id_card):
        factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        check_sum = sum([a * b for a, b in zip(factor, [int(a) for a in id_card[0:-1]])])
        return str(check_code_list[check_sum % 11])

    @classmethod
    def is_date(cls, id_card):
        try:
            date(int(id_card[6:10]), int(id_card[10:12]), int(id_card[12:14]))
            return True
        except ValueError as ve:
            return False  # "Datetime error: {0}".format(ve)


if __name__ == '__main__':
    id = "34030219850308081X"
