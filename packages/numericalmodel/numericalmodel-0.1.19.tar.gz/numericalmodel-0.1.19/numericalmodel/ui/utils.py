#!/usr/bin/env python3
# system modules
import locale
import gettext
from pkg_resources import resource_filename
import numericalmodel.ui

# external modules
import numpy as np

def lim_from_iv(iv):
    """
    Given an :any:`InterfaceValue`, determine sensible lower and upper lims

    Args:
        iv (InterfaceValue): the :any:`InterfaceValue`

    Returns:
        lower, upper: sensible bounds
    """
    values = iv.values[np.isfinite(iv.values)]
    lower, upper = iv.bounds
    if np.isfinite([lower, upper]).all():
        pass
    elif np.isfinite(lower):
        upper = max(max(lower, max(values)), 1) * 2
    elif np.isfinite(upper):
        lower = - min(min(upper, min(values)), 1) * 2
    else:
        lower, upper = [-2 * abs(min(iv.values)), 2 * abs(max(iv.values))]
    return lower, upper


GETTEXT_DOMAIN = 'numericalmodelgui'
LOCALEDIR = resource_filename(numericalmodel.ui.__name__, "locale")
