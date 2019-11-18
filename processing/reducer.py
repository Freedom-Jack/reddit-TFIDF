#!/usr/bin/python

import sys
import re

previous = None
termSum = 0

for line in sys.stdin:
    # Split by tab to get key and value
    key, value = re.split(r'\t', line)

    # Not the same as previous, means new key
    if key != previous:
        # If it is not the first element, print and reset
        if previous is not None:
            print(previous + '\t' + str(termSum))

        previous = key
        termSum = 0

    # Else, sum up the values of the same key
    termSum = termSum + int(value)

# Print the last element in the list
print(previous + '\t' + str(termSum))