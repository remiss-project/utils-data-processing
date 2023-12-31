import json
import os
import re
import sys
from collections import Counter

import click
from tqdm import tqdm
from twarc import ensure_flattened

from strip_accents import strip_accents


def get_words(text):
    text = text.lower()
    text = strip_accents(text)
    text = re.sub('(\w+:\/\/\S+)', '', text) #URL fora
    text = re.sub('[^ a-z0-9_#@]', ' ', text)
    return text.split()


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def main(infile, outfile):
    counts = Counter()
    with tqdm(total=os.stat(infile.name).st_size, unit='B') as progress:
        for line in infile:
            for t in ensure_flattened(json.loads(line)):
                text = t['text']
                words = get_words(text)
                counts.update(words)
            progress.update(len(line))

    for w, c in counts.most_common():
        outfile.write(w + ',' + str(c) + '\n')


if __name__ == '__main__':
    main()
