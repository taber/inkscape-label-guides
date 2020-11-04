#!/usr/bin/env python2
'''
Label Guides Creator

Copyright (C) 2018 John Beard - john.j.beard **guesswhat** gmail.com

## Simple Extension to draw guides and outlines for common paper labels

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import inkex
import simplestyle
from lxml import etree

# Colours to use for the guides
GUIDE_COLOURS = {
        'edge': '#00A000',
        'centre': '#A00000',
        'inset': '#0000A0'
}
'''
prolapse
'''

# Preset list
# Regular grids defined as:
#       'reg', unit, page_szie, l marg, t marg, X size, Y size,
#       X pitch, Y pitch, Number across, Number down, shapes
PRESETS = {
    # Rounded rectangular labels in grid layout
    'A5267':        ['reg', 'in', 'letter', 0.25, 0.5, 1.75, 0.5, 2, 0.5, 4, 20, 'rrect'],
    'L7167':        ['reg', 'mm', 'a4', 5.2, 3.95, 199.6, 289.1, 199.6, 289.1, 1, 1, 'rrect'],
    'L7168':        ['reg', 'mm', 'a4', 5.2, 5, 199.6, 143.5, 199.6, 143.5, 1, 2, 'rrect'],

    # Rect labels
    'L7784':        ['reg', 'mm', 'a4', 0, 0, 210, 297, 210, 297, 1, 1, 'rect'],
    'LP2_105':      ['reg', 'mm', 'a4', 0, 0, 105, 297, 105, 297, 2, 1, 'rect'],
    '3655':         ['reg', 'mm', 'a4', 0, 0, 210, 148.5, 210, 148.5, 1, 2, 'rect'],

    # Round labels
    'LP2_115R':     ['reg', 'mm', 'a4', 47.75, 16.65, 114.5, 114.5, 114.5, 149.2, 1, 2, 'circle'],
    'LP6_88R':      ['reg', 'mm', 'a4', 16, 14.5, 88, 88, 90, 90, 2, 3, 'circle'],
    'LP6_85R':      ['reg', 'mm', 'a4', 17.5, 16, 85, 85, 90, 90, 2, 3, 'circle'],
    'LP6_76R':      ['reg', 'mm', 'a4', 27, 31, 76, 76, 80, 79.5, 2, 3, 'circle'],

    # Oval labels
    'LP2_195OV':    ['reg', 'mm', 'a4', 7.5, 8.5, 195, 138, 195, 142, 1, 2, 'circle'],
    'LP4_90OV':     ['reg', 'mm', 'a4', 14, 12.5, 90, 135, 92, 137, 2, 2, 'circle'],

    # Square labels
    'LP6_95SQ':     ['reg', 'mm', 'a4', 6.5, 3, 95, 95, 98, 98, 2, 3, 'rrect'],
    'LP12_65SQ':    ['reg', 'mm', 'a4', 5, 15.5, 65, 65, 67.5, 67, 3, 4, 'rrect'],
    'LP15_51SQ':    ['reg', 'mm', 'a4', 26.6, 17.2, 51, 51, 52.9, 52.9, 3, 5, 'rrect'],
}
# Preset list
# Regular grids defined as:
#       'reg', unit, page_szie, l marg, t marg, X size, Y size,
#       X pitch, Y pitch, Number across, Number down, shapes

# I hate this too, thanks
a5366w = 3 + (7/16)
a5366lm = (8.5 - (a5366w * 2)) / 3
a5160w = 2 + (5/8)
a5160lm = (8.5 - (a5160w * 3)) / 4

PRESETS = {
    # rectangular labels in grid layout
    'A5267':        ['reg', 'in', 'letter', 0.3, 0.5, 1.75, 0.5, (1.75+0.3), 0.5, 4, 20, 'rect'],
    'A5366':        ['reg', 'in', 'letter', a5366lm, 0.5, a5366w, (2/3), a5366w + a5366lm, (2/3), 2, 15, 'rect'],
    'A5160':        ['reg', 'in', 'letter', a5160lm, 0.5, a5160w, 1, a5160w + a5160lm, 1, 3, 10, 'rect']
}

def add_SVG_guide(x, y, orientation, colour, parent):
    """ Create a sodipodi:guide node on the given parent
    """

    try:
        # convert mnemonics to actual orientations
        orientation = {
                'vert': '1,0',
                'horz': '0,1'
        }[orientation]
    except KeyError:
        pass

    attribs = {
            'position': str(x) + "," + str(y),
            'orientation': orientation
    }

    if colour is not None:
        attribs[inkex.addNS('color', 'inkscape')] = colour

    etree.SubElement(
        parent,
        inkex.addNS('guide', 'sodipodi'),
        attribs)


def delete_all_guides(document):
    # getting the parent's tag of the guides
    nv = document.xpath(
            '/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)[0]

    # getting all the guides
    children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',
                              namespaces=inkex.NSS)

    # removing each guides
    for element in children:
        nv.remove(element)


def draw_SVG_ellipse(rx, ry, cx, cy, style, parent, xi, yi):
    xi = str(xi).zfill(2)
    yi = str(yi).zfill(2)
    attribs = {
        'style': simplestyle.formatStyle(style),
        inkex.addNS('cx', 'sodipodi'):   str(cx),
        inkex.addNS('cy', 'sodipodi'):   str(cy),
        inkex.addNS('rx', 'sodipodi'):   str(rx),
        inkex.addNS('ry', 'sodipodi'):   str(ry),
        inkex.addNS('type', 'sodipodi'): 'arc',
        'id':       f"x{xi}-y{yi}",
        'class':    f"x{xi} y{yi}"
    }

    inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), attribs)


def draw_SVG_rect(x, y, w, h, round, style, parent, xi, yi):
    xi = str(xi).zfill(2)
    yi = str(yi).zfill(2)
    attribs = {
        'style':    str(inkex.Style(style)),
        'height':   str(h),
        'width':    str(w),
        'x':        str(x),
        'y':        str(y),
        'id':       f"x{xi}-y{yi}",
        'class':    f"x{xi} y{yi}"
    }

    if round:
        attribs['ry'] = str(round)

    etree.SubElement(parent, inkex.addNS('rect', 'svg'), attribs)


def add_SVG_layer(parent, gid, label):

    layer = etree.SubElement(parent, 'g', {
        'id': gid,
        inkex.addNS('groupmode', 'inkscape'): 'layer',
        inkex.addNS('label', 'inkscape'): label
    })

    return layer


class LabelGuides(inkex.Effect):

    def __init__(self):

        inkex.Effect.__init__(self)

        self.arg_parser.add_argument(
            '--units',
            type=str,
            dest='units', default="in",
            help='The units to use for custom label sizing')

        self.arg_parser.add_argument(
            '--preset_tab',
            type=str,
            dest='preset_tab', default='rrect',
            help='The preset section that is selected'
                 ' (other sections will be ignored)')

        # ROUNDED RECTANGLE PRESET OPTIONS
        self.arg_parser.add_argument(
            '--rrect_preset',
            type=str,
            dest='rrect_preset', default='L7167',
            help='Use the given rounded rectangle preset template')

        self.arg_parser.add_argument(
            '--rrect_radius',
            type=float,
            dest='rrect_radius', default=1,
            help='Rectangle corner radius')

        # RECTANGULAR PRESET OPTIONS
        self.arg_parser.add_argument(
            '--rect_preset',
            type=str,
            dest='rect_preset', default='L7784',
            help='Use the given square-corner rectangle template')

        # CIRCULAR PRESET OPTIONS
        self.arg_parser.add_argument(
            '--circ_preset',
            type=str,
            dest='circ_preset', default='LP2_115R',
            help='Use the given circular template')

        # CUSTOM LABEL OPTIONS
        self.arg_parser.add_argument(
            '--margin_l',
            type=float,
            dest='margin_l', default=8.5,
            help='Left page margin')

        self.arg_parser.add_argument(
            '--margin_t',
            type=float,
            dest='margin_t', default=13,
            help='Top page margin')

        self.arg_parser.add_argument(
            '--size_x',
            type=float,
            dest='size_x', default=37,
            help='Label X size')

        self.arg_parser.add_argument(
            '--size_y',
            type=float,
            dest='size_y', default=37,
            help='Label Y size')

        self.arg_parser.add_argument(
            '--pitch_x',
            type=float,
            dest='pitch_x', default=39,
            help='Label X pitch')

        self.arg_parser.add_argument(
            '--pitch_y',
            type=float,
            dest='pitch_y', default=39,
            help='Label Y pitch')

        self.arg_parser.add_argument(
            '--count_x',
            type=int,
            dest='count_x', default=5,
            help='Number of labels across')

        self.arg_parser.add_argument(
            '--count_y',
            type=int,
            dest='count_y', default=7,
            help='Number of labels down')

        self.arg_parser.add_argument(
            '--shapes',
            type=str,
            dest='shapes', default='rect',
            help='Label shapes to draw')

        # GENERAL DRAWING OPTIONS
        self.arg_parser.add_argument(
            '--delete_existing_guides',
            type=inkex.Boolean,
            dest='delete_existing_guides', default=False,
            help='Delete existing guides from document')

        self.arg_parser.add_argument(
            '--draw_edge_guides',
            type=inkex.Boolean,
            dest='draw_edge_guides', default=True,
            help='Draw guides at label edges')

        self.arg_parser.add_argument(
            '--draw_centre_guides',
            type=inkex.Boolean,
            dest='draw_centre_guides', default=True,
            help='Draw guides at label centres')

        self.arg_parser.add_argument(
            '--inset',
            type=float,
            dest='inset', default=5,
            help='Inset to use for inset guides')

        self.arg_parser.add_argument(
            '--draw_inset_guides',
            type=inkex.Boolean,
            dest='draw_inset_guides', default=True,
            help='Draw guides inset to label edges')

        self.arg_parser.add_argument(
            '--draw_shapes',
            type=inkex.Boolean,
            dest='draw_shapes', default=True,
            help='Draw label outline shapes')

        self.arg_parser.add_argument(
            '--shape_inset',
            type=float,
            dest='shape_inset', default=5,
            help='Inset to use for inset shapes')

        self.arg_parser.add_argument(
            '--draw_inset_shapes',
            type=inkex.Boolean,
            dest='draw_inset_shapes', default=True,
            help='Draw shapes inset in the label outline')

        self.arg_parser.add_argument(
            '--set_page_size',
            type=inkex.Boolean,
            dest='set_page_size', default=True,
            help='Set page size (presets only)')

    def _to_uu(self, val, unit):
        """
        Transform a value in given units to User Units
        """
        return self.svg.unittouu(str(val) + unit)

    def _get_page_size(self, size):
        """
        Get a page size from a definition entry - can be in the form
        [x, y], or a string (one of ['a4'])
        """

        if isinstance(size, (list,)):
            # Explicit size
            return size
        elif size == "a4":
            return [210, 297]
        elif size == "letter":
            # return [215.9, 279.4]
            return [8.5, 11]
        # Failed to find a useful size, None will inhibit setting the size
        return None

    def _set_SVG_page_size(self, document, x, y, unit):
        """
        Set the SVG page size to the given absolute size. The viewbox is
        also rescaled as needed to maintain the scale factor.
        """

        svg = document.getroot()

        # Re-calculate viewbox in terms of User Units
        new_uu_w = self._to_uu(x, unit)
        new_uu_h = self._to_uu(y, unit)

        # set SVG page size
        svg.attrib['width'] = str(x) + unit
        svg.attrib['height'] = str(y) + unit

        svg.attrib['viewBox'] = "0 0 %f %f" % (new_uu_w, new_uu_h)

    def _read_custom_options(self, options):
        """
        Read custom label geometry options and produce
        a dictionary of parameters for ingestion
        """
        unit = options.units

        custom_opts = {
                'units': options.units,
                'page_size': None,
                'margin': {
                    'l': self._to_uu(options.margin_l, unit),
                    't': self._to_uu(options.margin_t, unit)
                },
                'size': {
                    'x': self._to_uu(options.size_x, unit),
                    'y': self._to_uu(options.size_y, unit)
                },
                'pitch': {
                    'x': self._to_uu(options.pitch_x, unit),
                    'y': self._to_uu(options.pitch_y, unit)
                },
                'count': {
                    'x': options.count_x,
                    'y': options.count_y
                },
                'shapes': options.shapes,
                'corner_rad': None,
        }

        return custom_opts

    def _construct_preset_opts(self, preset_type, preset_id, options):
        """Construct an options object for a preset label template
        """
        preset = PRESETS[preset_id]

        unit = preset[1]

        opts = {
                'units': unit,
                'page_size': self._get_page_size(preset[2]),
                'margin': {
                    'l': self._to_uu(preset[3], unit),
                    't': self._to_uu(preset[4], unit)
                 },
                'size': {
                    'x': self._to_uu(preset[5], unit),
                    'y': self._to_uu(preset[6], unit)
                },
                'pitch': {
                    'x': self._to_uu(preset[7], unit),
                    'y': self._to_uu(preset[8], unit)
                },
                'count': {
                    'x': preset[9],
                    'y': preset[10]
                },
                'shapes': preset[11],
                'corner_rad': None,
        }

        # add addtional options by preset type
        if preset_type == "rrect":
            opts["corner_rad"] = self._to_uu(options.rrect_radius, unit)

        return opts

    def _get_regular_guides(self, label_opts, inset):
        """
        Get the guides for a set of labels defined by a regular grid

        This is done so that irregular-grid presets can be defined if
        needed
        """

        guides = {'v': [], 'h': []}

        x = label_opts['margin']['l']

        for x_idx in range(label_opts['count']['x']):

            l_pos = x + inset
            r_pos = x + label_opts['size']['x'] - inset

            guides['v'].extend([l_pos, r_pos])

            # Step over to next label
            x += label_opts['pitch']['x']

        # Horizontal guides, top to bottom
        height = self.svg.unittouu(self.svg.height)

        y = height - label_opts['margin']['t']

        for y_idx in range(label_opts['count']['y']):

            t_pos = y - inset
            b_pos = y - label_opts['size']['y'] + inset

            guides['h'].extend([t_pos, b_pos])

            # Step over to next label
            y -= label_opts['pitch']['y']

        return guides

    def _draw_label_guides(self, document, label_opts, inset, colour):
        """
        Draws label guides from a regular guide description object
        """
        # convert to UU
        inset = self._to_uu(inset, label_opts['units'])

        guides = self._get_regular_guides(label_opts, inset)

        # Get parent tag of the guides
        nv = self.svg.namedview

        # Draw vertical guides
        for g in guides['v']:
            add_SVG_guide(g, 0, 'vert', colour, nv)

        for g in guides['h']:
            add_SVG_guide(0, g, 'horz', colour, nv)

    def _draw_centre_guides(self, document, label_opts, colour):
        """
        Draw guides in the centre of labels defined by the given options
        """

        guides = self._get_regular_guides(label_opts, 0)
        nv = self.svg.namedview

        for g in range(0, len(guides['v']), 2):
            pos = (guides['v'][g] + guides['v'][g + 1]) / 2
            add_SVG_guide(pos, 0, 'vert', colour, nv)

        for g in range(0, len(guides['h']), 2):
            pos = (guides['h'][g] + guides['h'][g + 1]) / 2
            add_SVG_guide(0, pos, 'horz', colour, nv)

    def _draw_shapes(self, document, label_opts, inset):
        """
        Draw label shapes from a regular grid
        """

        style = {
                'stroke': '#333333',
                'stroke-width': self._to_uu(1, "px"),
                'fill': "none"
        }

        inset = self._to_uu(inset, label_opts['units'])

        guides = self._get_regular_guides(label_opts, 0)
        shape = label_opts['shapes']

        shapeLayer = add_SVG_layer(
                self.document.getroot(),
                self.svg.get_unique_id("outlineLayer"),
                "Label outlines")

        # guides start from the bottom, SVG items from the top
        height = self.svg.unittouu(self.svg.height)

        # draw shapes between every set of two guides
        for xi in range(0, len(guides['v']), 2):

            for yi in range(0, len(guides['h']), 2):
                
                if shape == 'circle':
                    cx = (guides['v'][xi] + guides['v'][xi + 1]) / 2
                    cy = (guides['h'][yi] + guides['h'][yi + 1]) / 2

                    rx = cx - guides['v'][xi] - inset
                    ry = guides['h'][yi] - cy - inset

                    draw_SVG_ellipse(rx, ry, cx, height - cy, style, shapeLayer, xi, yi)

                elif shape in ["rect", "rrect"]:

                    x = guides['v'][xi] + inset
                    w = guides['v'][xi + 1] - x - inset

                    y = guides['h'][yi] - inset
                    h = y - guides['h'][yi + 1] - inset

                    rnd = self._to_uu(label_opts['corner_rad'],
                                      label_opts['units'])

                    draw_SVG_rect(x, height - y, w, h, rnd, style, shapeLayer, xi, yi)

    def _set_page_size(self, document, label_opts):
        """
        Set the SVG page size from the given label template definition
        """

        size = label_opts['page_size']
        unit = label_opts['units']

        if size is not None:
            self._set_SVG_page_size(document, size[0], size[1], unit)

    def effect(self):
        """
        Perform the label template generation effect
        """

        preset_type = self.options.preset_tab.strip('"')

        if preset_type == "custom":
            # construct from parameters
            label_opts = self._read_custom_options(self.options)
        else:
            # construct from a preset

            # get the preset ID from the relevant enum entry
            preset_id = {
                    "rrect": self.options.rrect_preset,
                    "rect": self.options.rect_preset,
                    "circ": self.options.circ_preset,
            }[preset_type]

            label_opts = self._construct_preset_opts(preset_type, preset_id,
                                                     self.options)

        if self.options.delete_existing_guides:
            delete_all_guides(self.document)

        # Resize page first, otherwise guides won't be in the right places
        if self.options.set_page_size:
            self._set_page_size(self.document, label_opts)

        if self.options.draw_edge_guides:
            self._draw_label_guides(self.document, label_opts, 0,
                                    GUIDE_COLOURS['edge'])

        if self._draw_centre_guides:
            self._draw_centre_guides(self.document, label_opts,
                                     GUIDE_COLOURS['centre'])

        if self.options.draw_inset_guides and self.options.inset > 0.0:
            self._draw_label_guides(self.document, label_opts,
                                    self.options.inset,
                                    GUIDE_COLOURS['inset'])

        if self.options.draw_shapes:
            self._draw_shapes(self.document, label_opts, 0)

        if self.options.draw_inset_shapes:
            self._draw_shapes(self.document, label_opts,
                              self.options.shape_inset)


if __name__ == '__main__':
    # Create effect instance and apply it.
    effect = LabelGuides()
    effect.run()
