import json
from os.path import isfile

import click
import networkx as nx


def save_layout(layout, outfile):
    layout = {k: list(v) for k, v in layout.items()}
    with open(outfile, 'w') as outf:
        json.dump(layout, outf)


@click.command()
@click.argument('infile')
@click.argument('outfile')
@click.option(
    '--component', 'component',
    type=click.Choice(['weak', 'strong']), default=None
)
@click.option(
    '--layout', 'layout',
    type=click.Choice(['kamada_kawai', 'spectral', 'spring']),
    default='kamada_kawai'
)
@click.option('--weight', 'weight', default='weight')
def main(infile, outfile, component, layout, weight):
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

    if layout == 'spring':
        layout = None
        if isfile(outfile):
            with open(outfile) as inf:
                layout = json.load(inf)
        while True:
            layout = nx.spring_layout(
                graph, weight=weight,
                pos=layout, iterations=1
            )
            save_layout(layout, outfile)
    else:
        if layout == 'kamada_kawai':
            weights = nx.get_edge_attributes(graph, weight)
            costs = {k: 1/v for k, v in weights.items()}
            nx.set_edge_attributes(graph, costs, 'cost')
            dist = nx.shortest_path_length(graph, weight='cost')
            layout = nx.kamada_kawai_layout(graph, weight=weight, dist=dist)
        else:
            layout = nx.spectral_layout(graph, weight=weight)
        save_layout(layout, outfile)


if __name__ == '__main__':
    main()
