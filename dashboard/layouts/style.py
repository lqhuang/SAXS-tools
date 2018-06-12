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

LINE_STYLE = {
    'width': 1.0,
}

XLABEL = {
    'linear': r'Scattering Vector, $q$ $(\text{\AA}^{-1})$',
    'log': r'Scattering Vector, $q$ $(\text{\AA}^{-1}) (log scale)$',
    'guinier': r'$q^2$ $(\text{\AA}^{-2})$',
    'kratky': r'Scattering Vector, $q$ $(\text{\AA}^{-1})$',
    'porod': r'$q^4$ $(\text{\AA}^{-4})$',
    'pdf': r'pair distance ($\text{\AA}$)',
}

YLABEL = {
    'linear': 'Intensity (arb. units.)',
    'log': r'$\log(I)$',
    'guinier': r'$\ln(I(q))$',
    'kratky': r'$I(q) \cdot q^2$',
    'porod': r'$I(q) \cdot q^4$',
    'relative_diff': 'Relative Ratio (%)',
    'absolute_diff': 'Absolute Difference (arb. units.)',
    'error': 'Error',
    'error_relative_diff': 'Error Relative Ratio (%)',
    'pdf': 'P(r)',
}

TITLE = {
    'sasprofile': 'Subtracted Profiles',
    'guinier': 'Guinier Profiles',
    'kratky': 'Kratky Profiles',
    'porod': 'Porod Profiles',
    'relative_diff': 'Relative Difference Profiles',
    'absolute_diff': 'Absolute Difference Profiles',
    'error': 'Error Profile',
    'error_relative_diff': 'Error Relative Difference Profile',
    'pdf': 'Pair-wise Distribution',
    'fitting': 'P(r) Distribution Fitting',
}
