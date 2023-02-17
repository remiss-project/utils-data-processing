import json

import click
from tqdm import tqdm
from twarc import ensure_flattened


@click.command()
@click.option('--number', '-n', default=10)
@click.argument('infile')
@click.argument('outfile')
def main(number, infile, outfile):
    most_retweeted = []
    with open(infile) as infile:
        for line in tqdm(infile):
            for tweet in ensure_flattened(json.loads(line)):
                rt = tweet['public_metrics']['retweet_count']
                if len(most_retweeted) < number:
                    most_retweeted += [(rt, tweet)]
                elif most_retweeted[-1][0] < rt:
                    most_retweeted[-1] = (rt, tweet)
                else:
                    continue
                most_retweeted = sorted(most_retweeted, key=lambda x: -x[0])
    with open(outfile, 'w') as outfile:
        for _, tweet in most_retweeted:
            outfile.write(json.dumps(tweet) + '\n')


if __name__ == '__main__':
    main()
