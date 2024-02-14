# Author:  Dominic Fantauzzo
# GitHub username: fantauzd
# Date: 10/31/2023
# Description:  Defines a class that reads a JSON file containing data on Nobel Prizes
# and initializes the data to data members. Allows users to search the data,
# using the year and category, to find the surnames of the respective winner(s).

import json

class NobelData:
    """
    Reads a JSON file containing data on Nobel Prizes and initializes the data to data members. Allows users to
    search the data, using the year and category, to find the surnames of the respective winner(s).
    """
    def __init__(self):
        with open('nobels.json', 'r') as infile:
            self._data = json.load(infile)

    def find_record(self, year, category):
        """
        Uses the year and category to identify and return a specific Nobel Prize object. Not used in search_noble()
        :param year: year of prize
        :param cateogry: category of prize
        :return: specific prize object
        """
        for prize in self._data['prizes']:
            if prize['year'] == year and prize['category'] == category:
                return prize


    def find_record_binary(self, year, category):
        """
        Uses the year and category to identify and return a specific Nobel Prize object
        :param year: year of prize
        :param cateogry: category of prize
        :return: specific prize object
        """
        first = 0
        last = len(self._data['prizes']) - 1
        while first <= last:  # uses a bisection search to reduce time complexity from n to log(n)
            mid = (first + last)//2
            if self._data['prizes'][mid]['year'] == year:  # first checks the year using bisection search
                if self._data['prizes'][mid]['category'] == category:  # sees if category is right by coincidence
                    return self._data['prizes'][mid]
                else:
                    for value in range(0, 11):  # checks within 5 elements each direction as there are 6 categories
                        # makes sure the year and category are both accurate, must check year so we don't grab correct category, wrong year
                        if self._data['prizes'][(mid - 5 + value)]['category'] == category and \
                                self._data['prizes'][mid - 5 + value]['year'] == year:
                            return self._data['prizes'][(mid - 5 + value)]
            if self._data['prizes'][mid]['year'] < year:  # reverses order as list has largest (recent) years first
                last = mid - 1
            if self._data['prizes'][mid]['year'] > year:
                first = mid + 1


    def find_names(self, prize):
        """
        Takes a specific Nobel Prize object and creates a list of the laureates' surnames.
        The list is not sorted.
        :param prize: A Nobel Prize object
        :return: A list of laureates' surnames
        """
        names = []
        for winner in prize['laureates']:
            names.append(winner['surname'])
        return names


    def search_nobel(self, year, category):
        """
        Uses the year and category to identify a specific Nobel Prize and then returns the winners for that
        prize in alphabetical order
        :param year: The respective year of the prize
        :param category: the respective category of the prize
        :return: a list of winners of the prize, in alphabetical order
        """
        prize = self.find_record_binary(year, category)
        names = self.find_names(prize)
        for pass_num in range(len(names)-1):
            for surname in range(len(names) - 1 - pass_num):
                if names[surname] > names[surname + 1]:
                    temp = names[surname]
                    names[surname] = names[surname + 1]
                    names[surname + 1] = temp
        return names
