import json

import click
import networkx as nx
import networkx.algorithms.community as nx_comm


@click.command()
@click.argument('network', type=click.Path(exists=True, dir_okay=False))
@click.argument('outfile', type=click.File('w'))
@click.option('--weight', 'weight', default='weight', show_default=True)
@click.option('--cutoff', type=click.IntRange(1), default=1, show_default=True)
@click.option('--best_n', type=click.IntRange(1), default=None)
def main(network, outfile, weight, cutoff, best_n):
    graph = nx.read_gml(network)

    null_edges = [
        (x, y)
        for x, y, w in graph.edges(data=True)
        if w[weight] == 0
    ]
    graph.remove_edges_from(null_edges)

    ccs = nx.weakly_connected_components(graph)
    gcc = max(ccs, key=len)
    gcc = graph.subgraph(gcc)

    comm = nx_comm.greedy_modularity_communities(
        gcc, weight=weight, cutoff=cutoff, best_n=best_n
    )
    comm = sorted(comm, key=len, reverse=True)
    comm = {node: i for i, c in enumerate(comm) for node in c}
    json.dump(comm, outfile)


if __name__ == '__main__':
    main()
