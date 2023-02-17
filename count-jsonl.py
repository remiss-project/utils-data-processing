import json
import sys

import matplotlib.pyplot as plt
from matplotlib import dates
from tqdm import tqdm
from twarc import ensure_flattened


ARREL = '/mnt/data/jupyterlab/twarc/'


def get_index(granularitat):
  if granularitat == 'day':
    return 10
  if granularitat == 'hour':
    return 13


def get_xlabel(granularitat):
  if granularitat == 'day':
    return 'Day (mm-dd)'
  if granularitat == 'hour':
    return 'Hour (mm-dd HH)'


def get_locator(granularitat):
  if granularitat == 'day':
    return dates.DayLocator(interval=7)
  if granularitat == 'hour':
    return dates.DayLocator(interval=1)


if len(sys.argv) == 2:
  granularitat = 'day'
  consulta = sys.argv[1]
else:
  granularitat = sys.argv[1]
  consulta = sys.argv[2]

counts = dict()
with open(ARREL + consulta + '.jsonl') as f:
  lines = sum(1 for line in f)
with open(ARREL + consulta + '.jsonl') as f:
  for line in tqdm(f, total=lines):
    for t in ensure_flattened(json.loads(line)):
      date = t['created_at'][5:get_index(granularitat)]
      if date in counts:
        counts[date] += 1
      else:
        counts[date] = 1

counts = sorted(list(counts.items()))
days = [d.replace('T', ' ') for d, _ in counts]
counts = [c for _, c in counts]
fig, ax = plt.subplots(1, 1)
plt.bar(days, counts)
ax.set_ylabel('Tweets')
ax.set_xlabel(get_xlabel(granularitat))
ax.xaxis.set_major_locator(get_locator(granularitat))
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
fig.savefig('tweets-per-' + granularitat + '.pdf')
