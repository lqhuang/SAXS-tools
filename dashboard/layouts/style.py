from __future__ import print_function, division

GRAPH_GLOBAL_CONFIG = {'displaylogo': False}

AXIS_OPTIONS = [{
    'label': 'linear',
    'value': 'linear',
}, {
    'label': 'log',
    'value': 'log',
}]

XLABEL = dict()
XLABEL['linear_q'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
XLABEL['log_q'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}}) (log scale)$'
XLABEL['guinier'] = r'$q^2$ $(\mathrm{\AA^{-2}})$'
XLABEL['kratky'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
XLABEL['porod'] = r'$q^4$ $(\mathrm{\AA^{-4}})$'
XLABEL['distance'] = r'pair distance (nm)'

YLABEL = dict()
YLABEL['linear_I'] = r'Intensity (arb. units.)'
YLABEL['log_I'] = r'$\log(I)$'
YLABEL['guinier'] = r'$\ln(I(q))$'
YLABEL['kratky'] = r'$I(q) \cdot q^2$'
YLABEL['porod'] = r'$I(q) \cdot q^4$'
YLABEL['relative_diff'] = r'Relative Ratio (%)'
YLABEL['absolute_diff'] = r'Absolute Difference (arb. units.)'
YLABEL['pr'] = r'pair distance (nm)'

INLINE_LABEL_STYLE = {'display': 'inline-block'}
