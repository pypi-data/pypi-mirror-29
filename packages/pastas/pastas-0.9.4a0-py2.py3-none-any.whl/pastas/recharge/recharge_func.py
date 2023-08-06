"""recharge_func module
Contains the classes for the different models that are available to calculate the
recharge from evaporation and precipitation data.

Each Recharge class contains at least the following:

Attributes
----------
nparam: int
    Number of parameters needed for this model.

Functions
---------
set_parameters(self, name)
    A function that returns a Pandas DataFrame of the parameters of the
    recharge function. Columns of the dataframe need to be ['value', 'pmin',
    'pmax', 'vary']. Rows of the DataFrame have names of the parameters. Input
    name is used as a prefix. This function is called by a Tseries object.
simulate(self, evaporation, precipitation, p=None)
    A function that returns an array of the simulated recharge series.

References
----------
[1] R.A. Collenteur [2016] Non-linear time series analysis of deep groundwater
levels: Application to the Veluwe. MSc. thesis, TU Delft.
http://repository.tudelft.nl/view/ir/uuid:baf4fc8c-6311-407c-b01f-c80a96ecd584/
"""

from __future__ import print_function, division

import numpy as np
import pandas as pd

from .recharge import pref, perc, comb


class Linear:
    """
    Linear recharge model

    The recharge to the groundwater is calculated as:
    R = P - f * E

    """

    def __init__(self):
        self.nparam = 1

    def set_parameters(self, name):
        parameters = pd.DataFrame(
            columns=['initial', 'pmin', 'pmax', 'vary', 'name'])
        parameters.loc[name + '_f'] = (-1.0, -5.0, 0.0, 1, name)
        return parameters

    def simulate(self, precip, evap, p=None):
        recharge = precip + p * evap
        return recharge


class Preferential:
    """
    Preferential flow recharge model

    The water balance for the root zone is calculated as:
    dS / dt = Pe * (1 - (Sr / Srmax)**Beta)- Epu * min(1, Sr / (0.5 * Srmax))

    """

    def __init__(self):
        self.nparam = 3
        self.dt = 1  # Has to be 1 right now.
        self.solver = 1  # 1 = implicit, 2 = explicit

    def set_parameters(self, name):
        parameters = pd.DataFrame(
            columns=['initial', 'pmin', 'pmax', 'vary', 'name'])
        parameters.loc[name + '_Srmax'] = (0.26, np.nan, np.nan, 0, name)
        parameters.loc[name + '_Beta'] = (3.0, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Imax'] = (1.5e-3, np.nan, np.nan, 0, name)
        return parameters

    def simulate(self, precip, evap, p=None):
        t = np.arange(len(precip))
        recharge = pref(t, precip, evap, p[0], p[1], p[2],
                        self.dt, self.solver)[0]
        return recharge


class Percolation:
    """
    Percolation flow recharge model

    Other water balance for the root zone s calculated as:

    dS/dt = Pe - Kp * (Sr / Srmax)**Gamma - Epu * min(1, Sr / (0.5 * Srmax))

    """

    def __init__(self):
        self.nparam = 4
        self.dt = 1
        self.solver = 1

    def set_parameters(self, name):
        parameters = pd.DataFrame(
            columns=['initial', 'pmin', 'pmax', 'vary', 'name'])
        parameters.loc[name + '_Srmax'] = (0.26, np.nan, np.nan, 0, name)
        parameters.loc[name + '_Kp'] = (1.0e-2, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Gamma'] = (3.0, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Imax'] = (1.5e-3, 0.0, np.nan, 0, name)
        return parameters

    def simulate(self, precip, evap, p=None):
        t = np.arange(len(precip))
        recharge = perc(t, precip, evap, p[0], p[1], p[2], p[3],
                        self.dt, self.solver)[0]
        return recharge


class Combination:
    """
    Combination flow recharge model

    Other water balance for the root zone is calculated as:

    dS/ dt = Pe[t] * (1 - (Sr[t] / Srmax)**Beta) - Kp * (Sr / Srmax)**Gamma -
    Epu * min(1, Sr/ (0.5 * Srmax))

    """

    def __init__(self):
        self.nparam = 5
        self.dt = 1
        self.solver = 1

    def set_parameters(self, name):
        parameters = pd.DataFrame(
            columns=['initial', 'pmin', 'pmax', 'vary', 'name'])
        parameters.loc[name + '_Srmax'] = (0.26, np.nan, np.nan, 0, name)
        parameters.loc[name + '_Kp'] = (1.0e-2, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Beta'] = (3.0, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Gamma'] = (3.0, 0.0, np.nan, 1, name)
        parameters.loc[name + '_Imax'] = (1.5e-3, 0.0, np.nan, 0, name)
        return parameters

    def simulate(self, precip, evap, p=None):
        t = np.arange(len(precip))
        Rs, Rf = comb(t, precip, evap, p[0], p[1], p[2], p[3],
                      p[4], self.dt, self.solver)[0:2]
        recharge = Rs + Rf  # Slow plus fast recharge
        return recharge
