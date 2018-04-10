from __future__ import print_function, division

INLINE_LABEL_STYLE = {
    'display': 'inline-block',
}
GRAPH_GLOBAL_CONFIG = {
    'displaylogo': False,
    'modeBarButtonsToRemove': ['sendDataToCloud'],
}

AXIS_OPTIONS = ({
    'label': 'linear',
    'value': 'linear',
}, {
    'label': 'log',
    'value': 'log',
})

ERRORBAR_OPTIONS = ({
    'label': 'True',
    'value': True,
}, {
    'label': 'False',
    'value': False,
})

XLABEL = dict()
XLABEL['linear'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
XLABEL['log'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}}) (log scale)$'
XLABEL['guinier'] = r'$q^2$ $(\mathrm{\AA^{-2}})$'
XLABEL['kratky'] = r'Scattering Vector, $q$ $(\mathrm{\AA^{-1}})$'
XLABEL['porod'] = r'$q^4$ $(\mathrm{\AA^{-4}})$'
XLABEL['pdf'] = r'pair distance (nm)'

YLABEL = dict()
YLABEL['linear'] = r'Intensity (arb. units.)'
YLABEL['log'] = r'$\log(I)$'
YLABEL['guinier'] = r'$\ln(I(q))$'
YLABEL['kratky'] = r'$I(q) \cdot q^2$'
YLABEL['porod'] = r'$I(q) \cdot q^4$'
YLABEL['relative_diff'] = r'Relative Ratio (%)'
YLABEL['absolute_diff'] = r'Absolute Difference (arb. units.)'
YLABEL['pdf'] = r'P(r)'

TITLE = dict()
TITLE['sasprofile'] = 'Subtracted Profiles'
TITLE['guinier'] = 'Guinier Profiles'
TITLE['kratky'] = 'Kratky Profiles'
TITLE['porod'] = 'Porod Profiles'
TITLE['pdf'] = 'Pair-wise Distribution'
TITLE['relative_diff'] = 'Relative Difference Profiles'
TITLE['absolute_diff'] = 'Absolute Difference Profiles'
