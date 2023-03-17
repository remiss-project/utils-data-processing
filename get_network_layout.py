import json
from os.path import isfile

import click
import networkx as nx


@click.command()
@click.argument('infile')
@click.argument('outfile')
@click.option(
    '--component', 'component',
    type=click.Choice(['weak', 'strong']), default=None
)
@click.option('--weight', 'weight', default='weight')
def main(infile, outfile, component, weight):
    graph = nx.read_gml(infile)
    null_edges = [
        (x, y)
        for x, y, w in graph.edges(data=True)
        if w[weight] == 0
    ]
    graph.remove_edges_from(null_edges)
    if component is not None:
        if component == 'strong':
            cc = nx.strongly_connected_components(graph)
        else:
            cc = nx.weakly_connected_components(graph)
        gcc = max(cc, key=len)
        graph = graph.subgraph(gcc)
    graph = graph.to_undirected()

    layout = None
    if isfile(outfile):
        with open(outfile) as inf:
            layout = json.load(inf)
    while True:
        layout = nx.spring_layout(
            graph, weight=weight,
            pos=layout, iterations=1
        )
        layout = {k: list(v) for k, v in layout.items()}
        with open(outfile, 'w') as outf:
            json.dump(layout, outf)


if __name__ == '__main__':
    main()
