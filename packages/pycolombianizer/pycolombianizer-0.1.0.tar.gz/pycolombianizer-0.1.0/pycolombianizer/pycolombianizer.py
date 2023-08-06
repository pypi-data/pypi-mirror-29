# -*- coding: utf-8 -*-

"""Utils to colombianize a string."""
import random
from random import randint


class Colombianizer(object):
    """Colombianize class."""

    paisa_slang = ["parse", "sisas"]
    costa_slang = ["aja", "eche"]

    def string_2_paisa(self, your_string):
        """Conver a given string into the paisa representation.

        :param string: Your string
        :type string: String
        :return: Paisa string representation
        :rtype: String
        """
        slang = self.__get_slang("paisa")
        return self.__get_representation(slang, your_string)

    def string_2_costa(self, your_string):
        """Conver a given string into the costa representation.

        :param string: Your string
        :type string: String
        :return: Costa string representation
        :rtype: String
        """
        slang = self.__get_slang("costa")
        return self.__get_representation(slang, your_string)

    def __get_representation(self, slang, your_string):
        position = randint(0, 1)
        return "{ini_slang} {string} {end_slang}".format(
            ini_slang=slang if position is 0 else "",
            string=your_string if your_string else "",
            end_slang=slang if position is 1 else ""
        )

    def __get_slang(self, slang_type):
        """Return the slang.

        :param slang_type: The type of slang: "paisa" or "costa"
        :type slang_type: String
        """
        if slang_type == "paisa":
            random.shuffle(self.paisa_slang)
            return self.paisa_slang[0]
        elif slang_type == "costa":
            random.shuffle(self.costa_slang)
            return self.costa_slang[0]
        # Other slangs to be defined
        return ""

if __name__ == "__main__":
    colombianizer = Colombianizer()
    print(colombianizer.string_2_paisa("Hello world"))
    print(colombianizer.string_2_costa("Hello world"))
    print(colombianizer.string_2_costa(None))

