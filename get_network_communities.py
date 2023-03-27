import json

import click
import networkx as nx
import networkx.algorithms.community as nx_comm


@click.command()
@click.argument('network')
@click.argument('outfile')
@click.option(
    '--component', 'component',
    type=click.Choice(['weak', 'strong']), default=None
)
@click.option('--weight', 'weight', default='weight')
def main(network, outfile, component, weight):
    graph = nx.read_gml(network)

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

    graph = nx.DiGraph(graph)
    graph.remove_edges_from(nx.selfloop_edges(graph))

    comm = nx_comm.louvain_communities(graph, weight=weight)
    comm = sorted(comm, key=len, reverse=True)
    comm = {node: i for i, c in enumerate(comm) for node in c}

    with open(outfile, 'w') as outf:
        json.dump(comm, outf)


if __name__ == '__main__':
    main()
