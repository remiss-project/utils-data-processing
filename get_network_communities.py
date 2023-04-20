import json
import os

import click
import networkx as nx
import networkx.algorithms.community as nx_comm
from tqdm import tqdm


def get_network_communities(network, outfile, weight, cutoff, best_n):
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
    with open(outfile, 'w') as f:
        json.dump(comm, f)


@click.command()
@click.argument(
    'infiles', type=click.Path(exists=True, dir_okay=False), nargs=-1
)
@click.argument(
    'outdir', type=click.Path(exists=True, file_okay=False, writable=True)
)
@click.option('--weight', 'weight', default='weight', show_default=True)
@click.option('--cutoff', type=click.IntRange(1), default=1, show_default=True)
@click.option('--best_n', type=click.IntRange(1), default=None)
def main(infiles, outdir, weight, cutoff, best_n):
    infiles = [f for f in infiles if f.endswith('.gml')]
    for infile in tqdm(infiles):
        name = os.path.basename(infile)[:-4]
        outfile = os.path.join(outdir, name + '.json')
        get_network_communities(infile, outfile, weight, cutoff, best_n)


if __name__ == '__main__':
    main()
