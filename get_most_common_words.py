import json
import re
import sys
from collections import Counter

from tqdm import tqdm
from twarc import ensure_flattened


consulta = sys.argv[1]


def get_words(text):
    text = text.lower()
    text = re.sub('(\w+:\/\/\S+)', '', text) #URL fora
    text = re.sub('[^ a-z0-9_#@ñçáéíóúàèìòùäëïöü]', ' ', text)
    return text.split()


counts = Counter()
with open(consulta) as f:
    lines = sum(1 for line in f)
with open(consulta) as f:
    for line in tqdm(f, total=lines):
        for t in ensure_flattened(json.loads(line)):
            text = t['text']
            words = get_words(text)
            counts.update(words)

with open('words.csv', 'w') as f:
    for w, c in counts.most_common():
        f.write(w + ',' + str(c) + '\n')
