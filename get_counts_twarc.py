import json
import subprocess

import click


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile')
def main(infile, outfile):
    for window in json.load(infile):
        with open('tmp.txt', 'w') as t:
            for keyword in window['keywords']:
                t.write(keyword + '\n')
        subprocess.run([
            'twarc2', 'searches', '--archive', '--counts-only',
            '--start-time', window['start-time'],
            '--end-time', window['end-time'],
            'tmp.txt', outfile
        ])


if __name__ == '__main__':
    main()
