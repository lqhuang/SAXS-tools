from __future__ import print_function, division, absolute_import

from dashboard.layouts.sasimage import get_sasimage
from dashboard.layouts.sasprofile import get_sasprofile
from dashboard.layouts.cormap import get_cormap
from dashboard.layouts.series import get_series_analysis
from dashboard.layouts.guinier import get_guinier
from dashboard.layouts.colormap import get_colormap
from dashboard.layouts.gnom import get_gnom

LAYOUT_OPTIONS = (
    ('sasimage', 'SAS Images'),
    ('sasprofile', 'SAS Profile'),
    ('cormap', 'CorMap Analysis'),
    ('series_analysis', 'Series Analysis'),
    ('guinier', 'Guinier Analysis'),
    ('gnom', 'GNOM'),
    ('colormap', 'Colormap and Crossline'),
)

registered_layouts = {
    'sasimage': get_sasimage,
    'sasprofile': get_sasprofile,
    'cormap': get_cormap,
    'series_analysis': get_series_analysis,
    'guinier': get_guinier,
    'gnom': get_gnom,
    'colormap': get_colormap,
}
