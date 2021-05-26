#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script was written by Michael Schmidt
# (Also textfiles with instructions)

import sys
from enum import Enum


class KierasDurations(Enum):
    k = 280
    p = 1100
    b = 100
    h = 400
    m = 1200


def extractOperations():
    # Extract every oparation for klm out of textfile
    operations = []
    try:
        f = open(sys.argv[1], "r")
        temp = f.read().splitlines()
        f.close()

        # Extract every oparator as lowercase stripped string
        for operation in temp:
            if (operation.split("#")[0] != ""):
                operations.append(operation.split("#")[0].strip().lower())

        print(f"Found operations {operations}")
        return operations
    except Exception as e:
        print("There was an error with reading from the operations file. " + e)
        sys.exit(1)


def calculate_klm(operations, factors):
    # Calculate KLM estimated based on the given factors and operations
    # Values Enum check is from Stackoverflow:
    # https://stackoverflow.com/questions/43634618/
    # how-do-i-test-if-int-value-exists-in-python
    # -enum-without-using-try-catch
    values = set(item.name for item in factors)
    estimate = 0
    singleInstructions = []

    for operation in operations:
        for index, char in enumerate(operation):
            digitFactor = ""
            # if digit is found, complete indented number, save as factor
            # and multiple next instruction with it
            if (char.isdigit()):
                j = index
                while(operation[j].isdigit()):
                    digitFactor += operation[j]
                    j += 1
            if (digitFactor != ""):
                digitFactor = int(digitFactor.strip())
                if (char in values):
                    estimate += factors[char].value * digitFactor

            # if char is in enum add its value to estimate
            if (char in values):
                estimate += factors[char].value

    return estimate


if __name__ == "__main__":
    operations = extractOperations()
    origialEstimate = calculate_klm(operations, KierasDurations)
    # origialEstimate = calculate_klm(operations, false)
    print(
        f"With original estimates (Card et. al): {origialEstimate} Milliseconds")
