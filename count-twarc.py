import subprocess
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import dates


ARREL = '/home/ubuntu/jupyterlab/twarc/'

consulta = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
counts = 'counts.csv'

comanda = [
  'twarc2', 'searches', '--combine-queries', '--archive',
  '--counts-only', '--granularity', 'day',
  '--start-time', start, '--end-time', end,
  ARREL + consulta + '.txt',
  counts
]
#subprocess.run(comanda)

counts = pd.read_csv(counts).sort_values(by='start')

counts.columns = ['query', 'start', 'end', 'tweets']
counts['start'] = counts['start'].apply(lambda x: x[5:10])
ax = counts.plot.bar(x='start', y='tweets')
#counts = counts.set_index('start')
#ax = counts.plot.bar(y='tweets')
#ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
ax.xaxis.set_major_locator(dates.DayLocator(interval=7))
plt.xlabel('')
plt.tight_layout()
ax.get_figure().savefig('counts.pdf')

total = sum(counts['tweets'])
print(total)
with open('counts.txt', 'w') as f:
  f.write(str(total))
