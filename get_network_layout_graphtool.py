import json

import click
import graph_tool.all as gt


@click.command()
@click.argument('infile')
@click.argument('outfile')
@click.option(
    '--component', 'component',
    type=click.Choice(['weak', 'strong']), default=None
)
@click.option(
    '--layout', 'layout',
    type=click.Choice(['sfdp', 'arf', 'fr']),
    default='sfdp'
)
@click.option('--weight', 'weight', default='weight')
def main(infile, outfile, component, layout, weight):
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
    with open(outfile, 'w') as outf:
        json.dump(layout, outf)


if __name__ == '__main__':
    main()
