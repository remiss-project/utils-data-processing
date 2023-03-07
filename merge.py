import json
import os

import click
from tqdm import tqdm
from twarc import ensure_flattened


@click.command()
@click.argument('inpath')
@click.argument('outpath')
def main(inpath, outpath):
    tids = set()
    files = [f for f in os.listdir(inpath) if '.jsonl' in f]
    for f in tqdm(files):
        with open(inpath + f) as inf:
            for line in inf:
                for tweet in ensure_flattened(json.loads(line)):
                    tid = tweet['id']
                    if tid not in tids:
                        with open(outpath, 'a') as outf:
                            tids |= {tid}
                            outf.write(json.dumps(tweet) + '\n')


if __name__ == '__main__':
    main()
