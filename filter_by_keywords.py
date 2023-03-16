import json
import sys

import click
from twarc import ensure_flattened
from twarc.decorators2 import FileSizeProgressBar

from strip_accents import strip_accents


def contains_keywords(text, keywords):
    for k in keywords:
        if k in text:
            return True
    return False


def get_text(tweet):
    try:
        referenced_tweet = t['referenced_tweets'][0]
        if referenced_tweet['type'] == 'retweeted':
            return referenced_tweet['text']
    except:
        pass
    return tweet['text']


@click.command()
@click.argument('keywords', type=click.File('r'))
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def main(keywords, infile, outfile):
    keywords = [strip_accents(k) for k in json.load(keywords)['keywords']]

    with FileSizeProgressBar(infile, outfile) as progress:
        for line in infile:
            for t in ensure_flattened(json.loads(line)):
                text = strip_accents(get_text(t))
                if contains_keywords(text, keywords):
                    outfile.write(json.dumps(t) + '\n')
            progress.update(len(line))


if __name__ == '__main__':
    main()
