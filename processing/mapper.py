#!/usr/bin/python

import argparse
import collections
import json
import re
from json import JSONDecoder, JSONDecodeError


# Argument parser
parser = argparse.ArgumentParser(description="project_batch")
parser.add_argument("source_path", help="The path of the json data source file")

# Argument variables
sourcePath = parser.parse_args().source_path


# Decode method for stacked json
def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = re.compile(r'[^\s]').search(document, pos)
        if not match:
            return
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(document, pos)
        except JSONDecodeError:
            raise Exception("Decoder exception: can not decode stacked json input")
        yield obj


# Read input using json module
with open(sourcePath, 'r') as input_file:
    data = decode_stacked(input_file.read().replace('\n', ''))
    for row in data:

        # Remove any weird characters from the first column, i.e. the text column
        # Lastly, find words including apostrophe
        line = re.sub(r'^\W+|\W+$', '', row['body'])
        words = re.findall(r'[a-zA-Z0-9_]+\'?[a-zA-Z0-9_]{0,2}', line)

        # Aggregate the word array into a word dictionary with their counts
        words_dict = collections.defaultdict(lambda: int(0))
        for word in words:
            words_dict[word] = words_dict[word] + 1

        # Print out tf, df and n for MapReduce
        for aggregate_word in words_dict:
            print(word.lower() + " tr\t" + str(words_dict[aggregate_word]))
            print(word.lower() + " df\t1")
            print(word.lower() + "\t1")
