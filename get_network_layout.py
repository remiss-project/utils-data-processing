import json
import os

import click
import graph_tool.all as gt
from tqdm import tqdm


def get_network_layout(infile, outfile, component, layout, weight):
    g = gt.load_graph(infile)

    non_null_edges = [g.ep[weight][e] > 0 for e in g.edges()]
    g.set_edge_filter(g.new_edge_property('bool', vals=non_null_edges))

    if component:
        d = component == 'strong'
        g = gt.GraphView(g, vfilt=gt.label_largest_component(g, directed=d))

    if layout == 'sfdp':
        layout = gt.sfdp_layout(g, eweight=g.ep[weight])
    elif layout == 'arf':
        layout = gt.arf_layout(g, weight=g.ep[weight])
    else:
        layout = gt.fruchterman_reingold_layout(g, weight=g.ep[weight])

    layout = {g.vp.label[v]: list(layout[v]) for v in g.vertices()}
    with open(outfile, 'w') as f:
        json.dump(layout, f)


@click.command()
@click.argument(
    'infiles', type=click.Path(exists=True, dir_okay=False), nargs=-1
)
@click.argument(
    'outdir', type=click.Path(exists=True, file_okay=False, writable=True)
)
@click.option(
    '--component', 'component',
    type=click.Choice(['weak', 'strong']), default=None
)
@click.option(
    '--layout', 'layout',
    type=click.Choice(['sfdp', 'arf', 'fr']),
    default='sfdp', show_default=True
)
@click.option('--weight', 'weight', default='weight', show_default=True)
def main(infiles, outdir, component, layout, weight):
    infiles = [f for f in infiles if f.endswith('.gml')]
    for infile in tqdm(infiles):
        name = os.path.basename(infile)[:-4]
        outfile = os.path.join(outdir, name + '.json')
        get_network_layout(infile, outfile, component, layout, weight)


if __name__ == '__main__':
    main()
