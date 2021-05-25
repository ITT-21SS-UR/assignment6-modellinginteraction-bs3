#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script was written by Michael Schmidt

import sys
from enum import Enum


class OriginalDurations(Enum):
    k = 280
    p = 1100
    b = 100
    h = 400
    m = 1200

# Extract every oparation for klm out of textfile
def extractOperations():
    operations = []
    try:
        f = open(sys.argv[1], "r")
        temp = f.read().splitlines()
        f.close()

        # Extract every oparator as lowercase stripped string
        for operation in temp:
            if (operation.split("#")[0] != ""):
                operations.append(operation.split("#")[0].strip().lower())


        print(operations)
        print(OriginalDurations.k.value)
        return operations
    except:
        print("There was an error with reading from the operations file.")
        sys.exit(1)


if __name__ == "__main__":
    operations = extractOperations()
    # origialEstimate = calculate_klm_orginal(operations)

    # singleInstructions = []
    #     for operation in operations:
    #         for char in operation: 
    #             if (char.isDigit()):
    # median = calculate_klm_orginal(nums)
