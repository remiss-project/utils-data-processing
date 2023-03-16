import json
import re
import sys
import unicodedata
from collections import Counter

import click
from tqdm import tqdm
from twarc import ensure_flattened


def strip_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = [c for c in text if unicodedata.category(c) != 'Mn']
    return ''.join(text)


def get_words(text):
    text = text.lower()
    text = strip_accents(text)
    text = re.sub('(\w+:\/\/\S+)', '', text) #URL fora
    text = re.sub('[^ a-z0-9_#@]', ' ', text)
    return text.split()


@click.command()
@click.argument('infile')
@click.argument('outfile')
def main(infile, outfile):
    counts = Counter()
    with open(infile) as f:
        lines = sum(1 for line in f)
    with open(infile) as f:
        for line in tqdm(f, total=lines):
            for t in ensure_flattened(json.loads(line)):
                text = t['text']
                words = get_words(text)
                counts.update(words)

    with open(outfile, 'w') as f:
        for w, c in counts.most_common():
            f.write(w + ',' + str(c) + '\n')


if __name__ == '__main__':
    main()
