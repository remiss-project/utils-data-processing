import json
import os

import click
from tqdm import tqdm
from twarc import ensure_flattened


def get_index(granularity):
    if granularity == 'day':
        return 10
    if granularity == 'hour':
        return 13
    if granularity == 'minute':
        return 16


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
@click.option(
    '--granularity', 'granularity',
    type=click.Choice(['day', 'hour', 'minute']), default='day'
)
def main(infile, outfile, granularity):
    counts = dict()
    with tqdm(total=os.stat(infile.name).st_size, unit='B') as progress:
        for line in infile:
            for t in ensure_flattened(json.loads(line)):
                date = t['created_at'][5:get_index(granularity)]
                if date in counts:
                    counts[date] += 1
                else:
                    counts[date] = 1
            progress.update(len(line))
    outfile.write('start,' + granularity + '_count\n')
    for k, v in counts.items():
        outfile.write(k + ',' + str(v) + '\n')


if __name__ == '__main__':
    main()
