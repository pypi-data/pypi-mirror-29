#!/usr/bin/env python3

# internal modules
from numericalmodel.examples.equations.anemometer import \
    AnemometerAngularMomentumEquation
from numericalmodel.numericalmodel import NumericalModel
from numericalmodel.interfaces import *
from numericalmodel.numericalschemes import *

# external modules
import numpy as np
np.random.seed(42)


class AnemometerModel(NumericalModel):
    """
    A 4-cup anemometer model
    """

    def __init__(self):
        # create a model
        super().__init__()
        self.name = "4-cup anemometer model"
        self.authors = "Yann Büchau <nobodyinperson@gmx.de>, 2017"
        self.initial_time = 0

        # add the values to the model
        self.variables = SetOfInterfaceValues([
            InterfaceValue(id="f", name="frequency", unit="1/s",
                           bounds=[0, np.Inf]),
        ])

        self.parameters = SetOfInterfaceValues([
            InterfaceValue(id="m", name="cup mass", unit="kg",
                           bounds=[0, 0.3]),
            InterfaceValue(id="A", name="cup area", unit="m^2",
                           bounds=[0, 0.1]),
            InterfaceValue(id="R", name="distance cup - rotation axis",
                           unit="m", bounds=[0, np.Inf]),
            InterfaceValue(id="cw1", name="frontal drag value",
                           unit="1", bounds=[0, np.Inf]),
            InterfaceValue(id="cw2", name="back drag value",
                           unit="1", bounds=[0, np.Inf]),
            InterfaceValue(id="F_s", name="stiction anguluar momentum",
                           unit="Nm", bounds=[0, np.Inf]),
            InterfaceValue(id="F_f0", name="friction angular momentum offset",
                           unit="Nm", bounds=[0, np.Inf]),
            InterfaceValue(id="F_fa",
                           name="friction angular momentum linear parameter "
                           "momentum", unit="1/s^2", bounds=[0, np.Inf]),
        ])

        self.forcing = SetOfInterfaceValues([
            InterfaceValue(id="v", name="wind velocity", unit="m/s",
                           bounds=[0, 40]),
            InterfaceValue(id="rho", name="air density", unit="kg/m^3",
                           bounds=[0, np.Inf]),
        ])

        # set interpolation
        for id, iv in self.forcing.items():
            iv.interpolation = "linear"

        # set initial values
        self.variables["f"].value = 0
        self.parameters["R"].value = 0.08
        self.parameters["A"].value = 5e-4
        self.parameters["m"].value = 0.001
        self.parameters["F_s"].value = self.parameters["R"].value * 9.81 * 0.002
        self.parameters["F_f0"].value = self.parameters["F_s"].value * 0.1
        self.parameters["F_fa"].value = 0
        self.parameters["F_s"].bounds = [0, 0.3 * 9.81 * 0.005]
        self.parameters["F_f0"].bounds = self.parameters["F_s"].bounds
        self.parameters["cw1"].value = 1.4
        self.parameters["cw2"].value = 0.4
        self.forcing["v"].value = 0
        self.forcing["rho"].value = 1.2

        # create an equation object
        equation_input = []
        for ivs in self.variables, self.parameters, self.forcing:
            equation_input.extend(ivs.elements)
        equation = AnemometerAngularMomentumEquation(
            variable=self.variables["f"],
            input=SetOfInterfaceValues(equation_input),
        )

        # add the numerical scheme to the model
        self.numericalschemes = SetOfNumericalSchemes(
            [RungeKutta4(equation=equation, fallback_max_timestep=0.1)])


if __name__ == "__main__":
    AnemometerModel().cli()
