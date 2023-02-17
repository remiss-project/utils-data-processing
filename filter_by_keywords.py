import json
import sys

import click
from tqdm import tqdm
from twarc import ensure_flattened


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


def parse(text):
  substitutions = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
  }
  text = text.lower()
  for x, y in substitutions.items():
    text = text.replace(x, y)
  return text


@click.command()
@click.option('--count-lines', '-c', is_flag=True, default=False)
@click.argument('keywords')
@click.argument('infile')
@click.argument('outfile')
def main(count_lines, keywords, infile, outfile):
  with open(keywords) as f:
    keywords = [parse(k) for k in json.load(f)['keywords']]

  if count_lines:
    with open(infile) as f:
      lines = sum(1 for line in f)
  else:
    lines = None

  with open(infile) as infile:
    with open(outfile, 'w') as outfile:
      for line in tqdm(infile, total=lines):
        for t in ensure_flattened(json.loads(line)):
          text = parse(get_text(t))
          if contains_keywords(text, keywords):
            outfile.write(json.dumps(t) + '\n')


if __name__ == '__main__':
  main()
