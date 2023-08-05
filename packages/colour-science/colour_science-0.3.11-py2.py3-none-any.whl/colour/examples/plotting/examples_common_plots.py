# -*- coding: utf-8 -*-
"""
Showcases common plotting examples.
"""

from colour.plotting import (ColourSwatch, colour_plotting_defaults,
                             multi_colour_swatches_plot,
                             single_colour_swatch_plot)
from colour.utilities import message_box

message_box('Common Plots')

colour_plotting_defaults()

message_box('Plotting a single colour.')
single_colour_swatch_plot(
    ColourSwatch(
        'Neutral 5 (.70 D)', RGB=(0.32315746, 0.32983556, 0.33640183)),
    text_size=32)

print('\n')

message_box('Plotting multiple colours.')
multi_colour_swatches_plot(
    (ColourSwatch('Dark Skin', RGB=(0.45293517, 0.31732158, 0.26414773)),
     ColourSwatch('Light Skin', RGB=(0.77875824, 0.57726450, 0.50453169))),
    spacing=0,
    text_size=32)
