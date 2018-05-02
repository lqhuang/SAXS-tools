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
XLABEL['linear'] = r'Scattering Vector, $q$ $(\text{\AA}^{-1})$'
XLABEL['log'] = r'Scattering Vector, $q$ $(\text{\AA}^{-1}) (log scale)$'
XLABEL['guinier'] = r'$q^2$ $(\text{\AA}^{-2})$'
XLABEL['kratky'] = r'Scattering Vector, $q$ $(\text{\AA}^{-1})$'
XLABEL['porod'] = r'$q^4$ $(\text{\AA}^{-4})$'
XLABEL['pdf'] = 'pair distance (nm)'

YLABEL = dict()
YLABEL['linear'] = 'Intensity (arb. units.)'
YLABEL['log'] = r'$\log(I)$'
YLABEL['guinier'] = r'$\ln(I(q))$'
YLABEL['kratky'] = r'$I(q) \cdot q^2$'
YLABEL['porod'] = r'$I(q) \cdot q^4$'
YLABEL['relative_diff'] = 'Relative Ratio (%)'
YLABEL['absolute_diff'] = 'Absolute Difference (arb. units.)'
YLABEL['error'] = 'Error'
YLABEL['error_relative_diff'] = 'Error Relative Ratio (%)'
YLABEL['pdf'] = 'P(r)'

TITLE = dict()
TITLE['sasprofile'] = 'Subtracted Profiles'
TITLE['guinier'] = 'Guinier Profiles'
TITLE['kratky'] = 'Kratky Profiles'
TITLE['porod'] = 'Porod Profiles'
TITLE['relative_diff'] = 'Relative Difference Profiles'
TITLE['absolute_diff'] = 'Absolute Difference Profiles'
TITLE['error'] = 'Error Profile'
TITLE['error_relative_diff'] = 'Error Relative Difference Profile'
TITLE['pdf'] = 'Pair-wise Distribution'
TITLE['fitting'] = 'P(r) Distribution Fitting'
