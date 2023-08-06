from .common import MeshInfoBase, dump_array
from . import _triangle as internals


class MeshInfo(internals.MeshInfo, MeshInfoBase):
    _constituents = [
        "points", "point_attributes", "point_markers",
        "elements", "element_attributes", "element_volumes",
        "neighbors",
        "facets", "facet_markers",
        "holes",
        "regions",
        "faces", "face_markers",
        "normals",
    ]

    def __getstate__(self):
        return self.number_of_point_attributes, \
            self.number_of_element_attributes, \
            [(name, getattr(self, name)) for name in self._constituents]

    def __setstate__(self, xxx_todo_changeme):
        (p_attr_count, e_attr_count, state) = xxx_todo_changeme
        self.number_of_point_attributes = p_attr_count
        self.number_of_element_attributes = e_attr_count
        for name, array in state:
            if name not in self._constituents:
                raise RuntimeError("Unknown constituent during unpickling")

            dest_array = getattr(self, name)

            if array is None:
                dest_array.deallocate()
            else:
                if len(dest_array) != len(array):
                    dest_array.resize(len(array))
                if not dest_array.allocated and len(array) > 0:
                    dest_array.setup()

                for i, tup in enumerate(array):
                    for j, v in enumerate(tup):
                        dest_array[i, j] = v

    def set_facets(self, facets, facet_markers=None):
        self.facets.resize(len(facets))

        for i, facet in enumerate(facets):
            self.facets[i] = facet

        if facet_markers is not None:
            self.facet_markers.setup()
            for i, mark in enumerate(facet_markers):
                self.facet_markers[i] = mark

    def dump(self):
        for name in self._constituents:
            dump_array(name, getattr(self, name))


def build(mesh_info, verbose=False, refinement_func=None, attributes=False,
          volume_constraints=False, max_volume=None, allow_boundary_steiner=True,
          allow_volume_steiner=True, quality_meshing=True,
          generate_edges=None, generate_faces=False, min_angle=None,
          mesh_order=None, generate_neighbor_lists=False):
    """Triangulate the domain given in `mesh_info'."""
    opts = "pzj"
    if quality_meshing:
        if min_angle is not None:
            opts += "q%f" % min_angle
        else:
            opts += "q"

    if mesh_order is not None:
        opts += "o%d" % mesh_order

    if verbose:
        opts += "VV"
    else:
        opts += "Q"

    if attributes:
        opts += "A"

    if volume_constraints:
        opts += "a"
    if max_volume:
        opts += "a%.20f" % max_volume

    if refinement_func is not None:
        opts += "u"

    if generate_edges is not None:
        from warnings import warn
        warn("generate_edges is deprecated--use generate_faces instead")
        generate_faces = generate_edges
    if generate_neighbor_lists is not None:
        opts += "n"

    if generate_faces:
        opts += "e"

    if not allow_volume_steiner:
        opts += "YY"
        if allow_boundary_steiner:
            raise ValueError("cannot allow boundary Steiner points when volume "
                             "Steiner points are forbidden")
    else:
        if not allow_boundary_steiner:
            opts += "Y"

    # restore "C" locale--otherwise triangle might mis-parse stuff like "a0.01"
    try:
        import locale
    except ImportError:
        have_locale = False
    else:
        have_locale = True
        prev_num_locale = locale.getlocale(locale.LC_NUMERIC)
        locale.setlocale(locale.LC_NUMERIC, "C")

    try:
        mesh = MeshInfo()
        internals.triangulate(opts, mesh_info, mesh,
                              MeshInfo(), refinement_func)
    finally:
        # restore previous locale if we've changed it
        if have_locale:
            locale.setlocale(locale.LC_NUMERIC, prev_num_locale)

    return mesh


def refine(input_p, verbose=False, refinement_func=None,  quality_meshing=True,
           min_angle=None, generate_neighbor_lists=False):
    opts = "razj"

    if quality_meshing:
        if min_angle is not None:
            opts += "q%f" % min_angle
        else:
            opts += "q"

    if len(input_p.faces) != 0:
        opts += "p"
    if verbose:
        opts += "VV"
    else:
        opts += "Q"
    if refinement_func is not None:
        opts += "u"
    if generate_neighbor_lists is not None:
        opts += "n"

    output_p = MeshInfo()
    internals.triangulate(opts, input_p, output_p, MeshInfo(), refinement_func)
    return output_p


def write_gnuplot_mesh(filename, out_p, facets=False):
    gp_file = open(filename, "w")

    if facets:
        segments = out_p.facets
    else:
        segments = out_p.elements

    for points in segments:
        for pt in points:
            gp_file.write("%f %f\n" % tuple(out_p.points[pt]))
        gp_file.write("%f %f\n\n" % tuple(out_p.points[points[0]]))
