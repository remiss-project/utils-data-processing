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
    files = [inpath + f for f in os.listdir(inpath) if '.jsonl' in f]
    size = sum([os.stat(f).st_size for f in files])
    with tqdm(total=size, unit='B') as progress:
        for f in files:
            with open(f) as infile:
                for line in infile:
                    for tweet in ensure_flattened(json.loads(line)):
                        tid = tweet['id']
                        if tid not in tids:
                            tids |= {tid}
                            outfile.write(json.dumps(tweet) + '\n')
                    progress.update(len(line))


if __name__ == '__main__':
    main()
