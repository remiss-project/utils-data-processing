import json
import os

import click
from tqdm import tqdm
from twarc import ensure_flattened


@click.command()
@click.argument('infiles', type=click.File('r'), nargs=-1)
@click.argument('outfile', type=click.File('w'))
def main(infiles, outfile):
    tids = set()
    infiles = [f for f in infiles if '.jsonl' in f.name]
    size = sum([os.stat(f.name).st_size for f in infiles])
    with tqdm(total=size, unit='B') as progress:
        for infile in infiles:
            for line in infile:
                for tweet in ensure_flattened(json.loads(line)):
                    tid = tweet['id']
                    if tid not in tids:
                        tids |= {tid}
                        outfile.write(json.dumps(tweet) + '\n')
                progress.update(len(line))


if __name__ == '__main__':
    main()
