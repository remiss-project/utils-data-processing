import json
import os

import click
from tqdm import tqdm
from twarc import ensure_flattened


@click.command()
@click.argument('inpath')
@click.argument('outfile', type=click.File('w'))
def main(inpath, outfile):
    tids = set()
    files = [f for f in os.listdir(inpath) if '.jsonl' in f]
    for f in tqdm(files):
        with open(inpath + f) as infile:
            for line in infile:
                for tweet in ensure_flattened(json.loads(line)):
                    tid = tweet['id']
                    if tid not in tids:
                        tids |= {tid}
                        outfile.write(json.dumps(tweet) + '\n')


if __name__ == '__main__':
    main()
