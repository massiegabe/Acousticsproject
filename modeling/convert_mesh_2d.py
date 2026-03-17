#!/usr/bin/env python
"""
Convert a Gmsh 2.2 .msh file to a 2D Medit .mesh file.

Strips the z coordinate (assumed to be 0) and preserves physical group
tags on edge and quad elements so SfePy can read it as a proper 2D mesh.

Usage:
    python convert_mesh_2d.py [input.msh] [output.mesh]
Defaults to gabe2_openclosed.msh -> gabe2_openclosed_2d.mesh
"""
import sys

GMSH_LINE  = 1   # 2-node line element
GMSH_QUAD  = 3   # 4-node quadrangle element


def parse_gmsh_msh(filename):
    nodes = {}        # node_id (1-based) -> (x, y)
    edge_elems = []   # (n1, n2, phys_group)
    quad_elems = []   # (n1, n2, n3, n4, phys_group)

    with open(filename) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        tag = lines[i].strip()

        if tag == '$Nodes':
            i += 1
            n_nodes = int(lines[i].strip())
            i += 1
            for _ in range(n_nodes):
                parts = lines[i].strip().split()
                nid = int(parts[0])
                x, y = float(parts[1]), float(parts[2])
                # z = float(parts[3]) — discarded
                nodes[nid] = (x, y)
                i += 1

        elif tag == '$Elements':
            i += 1
            n_elems = int(lines[i].strip())
            i += 1
            for _ in range(n_elems):
                parts = list(map(int, lines[i].strip().split()))
                elm_type = parts[1]
                n_tags   = parts[2]
                phys_grp = parts[3]          # first tag = physical group
                node_ids = parts[3 + n_tags:]

                if elm_type == GMSH_LINE:
                    edge_elems.append((node_ids[0], node_ids[1], phys_grp))
                elif elm_type == GMSH_QUAD:
                    quad_elems.append((node_ids[0], node_ids[1],
                                       node_ids[2], node_ids[3], phys_grp))
                i += 1
        else:
            i += 1

    return nodes, edge_elems, quad_elems


def write_medit_2d(filename, nodes, edge_elems, quad_elems):
    # Medit format uses 1-based, sequential node ids.
    # Gmsh node ids are 1-based but may have gaps — remap to be safe.
    node_ids_sorted = sorted(nodes.keys())
    remap = {old: new for new, old in enumerate(node_ids_sorted, start=1)}

    with open(filename, 'w') as f:
        f.write('MeshVersionFormatted 1\n\n')
        f.write('Dimension\n2\n\n')

        f.write('Vertices\n%d\n' % len(nodes))
        for nid in node_ids_sorted:
            x, y = nodes[nid]
            f.write('%.15g %.15g 0\n' % (x, y))   # x y ref(=0)

        f.write('\nQuadrilaterals\n%d\n' % len(quad_elems))
        for n1, n2, n3, n4, ref in quad_elems:
            f.write('%d %d %d %d %d\n' % (
                remap[n1], remap[n2], remap[n3], remap[n4], ref))

        f.write('\nEdges\n%d\n' % len(edge_elems))
        for n1, n2, ref in edge_elems:
            f.write('%d %d %d\n' % (remap[n1], remap[n2], ref))

        f.write('\nEnd\n')

    print('Wrote %d vertices, %d quads, %d edges -> %s' % (
        len(nodes), len(quad_elems), len(edge_elems), filename))


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'gabe2_openclosed.msh'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'gabe2_openclosed_2d.mesh'
    nodes, edges, quads = parse_gmsh_msh(src)
    write_medit_2d(dst, nodes, edges, quads)
