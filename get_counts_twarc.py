import json
import subprocess

import click


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile')
@click.option(
    '--granularity', 'granularity',
    type=click.Choice(['day', 'hour', 'minute']), default='day'
)
def main(infile, outfile, granularity):
    for window in json.load(infile):
        with open('tmp.txt', 'w') as t:
            for keyword in window['keywords']:
                t.write(keyword + '\n')
        subprocess.run([
            'twarc2', 'searches', '--archive', '--counts-only',
            '--granularity', granularity,
            '--start-time', window['start-time'],
            '--end-time', window['end-time'],
            'tmp.txt', outfile
        ])


if __name__ == '__main__':
    main()
