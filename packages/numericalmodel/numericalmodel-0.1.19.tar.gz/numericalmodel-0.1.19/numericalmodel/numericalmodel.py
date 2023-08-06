#!/usr/bin/env python3
# system modules
import logging
import datetime
import textwrap
import collections
import itertools

# internal modules
from .genericmodel import GenericModel
from . import interfaces
from . import numericalschemes
from . import utils

# external modules
import numpy as np
import scipy.optimize

logger = logging.getLogger(__name__)


class NumericalModel(GenericModel):
    """
    Class for numerical models

    Args:
        name (str, optional): the model name
        version (str, optional): the model version
        description (str): a short model description
        long_description (str): an extended model description
        authors (:any:`str`, :any:`list` or :any:`dict`, optional):
            the model author(s). One of

            :any:`str`:
                name of single author
            :any:`list` of :any:`str`:
                :any:`list` of author names
            :any:`dict`:
                :any:`dict` of ``{'task': ['name1','name1']}`` pairs
        initial_time (float): initial model time (UTC unix timestamp)
        observations (SetOfInterfaceValues, optional): observations
        parameters (SetOfInterfaceValues, optional): model parameters
        forcing (SetOfInterfaceValues, optional): model forcing
        variables (SetOfInterfaceValues, optional): model state variables
        numericalschemes (SetOfNumericalSchemes, optional): model schemes with
            equation
        unit_conversions (dict(str), optional): mapping of units to convert
            before presenting data (e.g. plotting). See also
            :any:`InterfaceValue.unit_converters`.
    """

    def __init__(self,
                 name=None,
                 version=None,
                 description=None,
                 long_description=None,
                 authors=None,
                 initial_time=None,
                 parameters=None,
                 observations=None,
                 forcing=None,
                 variables=None,
                 numericalschemes=None,
                 unit_conversions=None,
                 zero_date=None,
                 ):
        # GenericModel constructor
        GenericModel.__init__(self,
                              name=name,
                              version=version,
                              description=description,
                              long_description=long_description,
                              authors=authors,
                              )

        self.logger = logging.getLogger(__name__)  # logger

        # set properties
        if initial_time is not None:
            self.initial_time = initial_time
        if parameters is not None:
            self.parameters = parameters
        if forcing is not None:
            self.forcing = forcing
        if observations is not None:
            self.observations = observations
        if variables is not None:
            self.variables = variables
        if numericalschemes is not None:
            self.numericalschemes = numericalschemes
        if unit_conversions is not None:
            self.unit_conversions = unit_conversions
        if zero_date is not None:
            self.zero_date = zero_date

    ##################
    ### Properties ###
    ##################
    @property
    def initial_time(self):
        """
        The initial model time

        :type: :any:`float`
        """
        try:
            self._initial_time
        except AttributeError:
            self._initial_time = self._default_initial_time
        return self._initial_time

    @initial_time.setter
    def initial_time(self, newtime):
        assert utils.is_numeric(newtime), "initial_time has to be numeric"
        assert np.array(newtime).size == 1, "initial_time has to be one value"
        self._initial_time = newtime

    @property
    def _default_initial_time(self):
        """
        Default initial model time if none was given

        :type: :any:`float`
        """
        return utils.utcnow()

    @property
    def _default_name(self):
        """
        Default name if none was given

        :type: :any:`str`
        """
        return "numerical model"

    @property
    def _default_description(self):
        """
        Default description if none was given

        :type: :any:`str`
        """
        return "a numerical model"

    @property
    def _default_long_description(self):
        """
        Default long_description if none was given

        :type: :any:`str`
        """
        return "This is a numerical model."

    @property
    def zero_date(self):
        """
        The date at time zero

        :type: :any:`datetime.datetime`
        """
        try:
            self._zero_date  # already defined?
        except AttributeError:
            self._zero_date = None
        return self._zero_date  # return

    @zero_date.setter
    def zero_date(self, newzero_date):
        self._zero_date = np.datetime64(newzero_date).astype(object)

    @property
    def unit_conversions(self):
        """
        The unit conversions applied before presenting data

        :type: :any:`dict`
        """
        try:
            self._unit_conversions  # already defined?
        except AttributeError:
            self._unit_conversions = {}
        return self._unit_conversions  # return

    @unit_conversions.setter
    def unit_conversions(self, newunit_conversions):
        conv = {}
        for f,t in newunit_conversions.items():
            try:
                interfaces.InterfaceValue.unit_converters[f][t]
            except KeyError:
                self.logger.warning("Required unit conversion from '{}' to "
                    "'{}' is undefined. This may cause problems.".format(f,t))
            conv[f] = t
        self._unit_conversions = conv

    @property
    def observations(self):
        """
        The model observations

        :type: :any:`SetOfInterfaceValues`
        """
        try:
            self._observations  # already defined?
        except AttributeError:
            self._observations = self._default_observations
        return self._observations  # return

    @observations.setter
    def observations(self, newobservations):
        assert issubclass(newobservations.__class__,
                          interfaces.SetOfInterfaceValues),\
            "observations has to be object of subclass of SetOfInterfaceValues"
        self._observations = newobservations
        self._observations.time_function = self.get_model_time  # time function

    @property
    def _default_observations(self):
        """
        Default observations if none were given

        :type: :any:`SetOfInterfaceValues`
        """
        return interfaces.SetOfInterfaceValues()

    @property
    def parameters(self):
        """
        The model parameters

        :type: :any:`SetOfInterfaceValues`
        """
        try:
            self._parameters  # already defined?
        except AttributeError:
            self._parameters = self._default_parameters
        return self._parameters  # return

    @parameters.setter
    def parameters(self, newparameters):
        assert issubclass(newparameters.__class__,
                          interfaces.SetOfInterfaceValues),\
            "parameters has to be object of subclass of SetOfInterfaceValues"
        self._parameters = newparameters
        self._parameters.time_function = self.get_model_time  # time function

    @property
    def _default_parameters(self):
        """
        Default parameters if none were given

        :type: :any:`SetOfInterfaceValues`
        """
        return interfaces.SetOfInterfaceValues()

    @property
    def forcing(self):
        """
        The model forcing

        :type: :any:`SetOfInterfaceValues`
        """
        try:
            self._forcing  # already defined?
        except AttributeError:
            self._forcing = self._default_forcing
        return self._forcing  # return

    @forcing.setter
    def forcing(self, newforcing):
        assert issubclass(newforcing.__class__,
                          interfaces.SetOfInterfaceValues),\
            "forcing has to be object of subclass of SetOfInterfaceValues"
        self._forcing = newforcing
        self._forcing.time_function = self.get_model_time  # set time function

    @property
    def _default_forcing(self):
        """
        Default forcing if none was given

        :type: :any:`SetOfInterfaceValues`
        """
        return interfaces.SetOfInterfaceValues()

    @property
    def variables(self):
        """
        The model variables

        :type: :any:`SetOfInterfaceValues`
        """
        try:
            self._variables  # already defined?
        except AttributeError:  # default
            self._variables = interfaces.SetOfInterfaceValues()
        return self._variables  # return

    @variables.setter
    def variables(self, newvariables):
        assert issubclass(newvariables.__class__,
                          interfaces.SetOfInterfaceValues), \
            "variables has to be object of subclass of SetOfInterfaceValues"
        self._variables = newvariables
        self._variables.time_function = self.get_model_time  # set time function

    @property
    def _default_variables(self):
        """
        Default variables if none were given

        :type: :any:`SetOfInterfaceValues`
        """
        return interfaces.SetOfInterfaceValues()

    @property
    def numericalschemes(self):
        """
        The model numerical schemes

        :type: :any:`str`
        """
        try:
            self._numericalschemes  # already defined?
        except AttributeError:
            self._numericalschemes = self._default_numericalschemes
        return self._numericalschemes  # return

    @numericalschemes.setter
    def numericalschemes(self, newnumericalschemes):
        assert isinstance(newnumericalschemes,
                          numericalschemes.SetOfNumericalSchemes),\
            "numericalschemes has to be instance of SetOfNumericalSchemes"
        self._numericalschemes = newnumericalschemes

    @property
    def _default_numericalschemes(self):
        """
        Default numerical schemes if none were given

        :type: :any:`SetOfNumericalSchemes`
        """
        return numericalschemes.SetOfNumericalSchemes()

    @property
    def model_time(self):
        """
        The current model time

        :type: :any:`float`
        """
        try:
            self._model_time  # already defined?
        except AttributeError:
            self._model_time = self.initial_time  # default
        return float(self._model_time)  # return

    @model_time.setter
    def model_time(self, newtime):
        assert utils.is_numeric(newtime), "model_time has to be numeric"
        assert np.array(newtime).size == 1, "model_time has to be one value"
        self._model_time = float(newtime)

    @property
    def content(self):
        """
        List of all :any:`InterfaceValue` s in this model

        :type: list
        """
        res = []
        for n in ["variables", "parameters", "forcing", "observations"]:
            s = getattr(self, n)
            res.extend(s.values())
        return res

    ###############
    ### Methods ###
    ###############
    def find(self, ivid):
        """
        Find an :any:`InterfaceValue` by its id in any part of this model

        Args:
            ivid (str): the :any:`InterfaceValue.id` to search for

        Returns:
            InterfaceValue or False: the :any:`InterfaceValue`, ``False`` on
                failure
        """
        for n in ["variables", "parameters", "forcing", "observations"]:
            try:
                return getattr(self, n)[ivid]
            except KeyError:
                pass
        return False

    def reset(self, time=None, past_also = False, only=None):
        """
        Reset all model data to a time. If no time was given, reset to the
        earliest time available.

        Args:
            time (float, optional): Time to reset to. Defaults to the earliest
                available time.
            only (list, optional): List of :any:`InterfaceValue.id` s. Only
                these :any:`InterfaceValue` s will be reset. Defaults to
                everything in this model.
            past_also (bool, optional): Reset past values as well? Defaults to
                ``False``.
        """
        only = self.content if only is None else [self.find(i) for i in only]

        if time is None:
            time = min([min(iv.times) for iv in self.content])

        for iv in only:
            old = iv[time]
            if past_also:
                iv[:] = (np.array([time]),np.array([old]))
            else:
                iv.cut(end=time)
                iv[time] = old

        self.model_time = time

    def get_model_time(self):
        """
        The current model time

        Returns:
            float: current model time
        """
        return self.model_time

    def integrate(self, final_time=None, seconds=None):
        """
        Integrate the model until final_time

        Args:
            final_time (float): time to integrate until. Conflicts with
                ``seconds``.
            seconds (float): seconds to integrate. Conflicts with
                ``final_time``.
        """
        # reset variables to model time
        self.reset(time=self.model_time,
                   only=[iv.id for iv in self.variables.values()])
        self.logger.info("start integration")
        if final_time is not None and seconds is None:
            pass
        elif final_time is None and seconds is not None:
            final_time = self.model_time + seconds
        else:
            raise ValueError("Specify either 'final_time' or 'seconds'")
        self.numericalschemes.integrate(
            start_time=self.model_time,
            final_time=final_time,
        )
        self.model_time = final_time
        self.logger.info("end of integration")

    def optimize(self, bring_together, variate, time_start=None,
                 time_end=None, **kwargs):
        """
        Optimize the :any:`InterfaceValue` s in ``variate`` such that the
        :any:`InterfaceValue` s in ``bring_together`` fit best.

        .. note::

            This method repeatedly **deletes** the data in the given time span
            and simulates it again with slightly modified input.

        Args:
            bring_together (list): The :any:`InterfaceValue` s to bring
                together. This is a :any:`list` like
                ``[[InterfaceValue(),...],[InterfaceValue(),...]]``.
            variate (dict): The :any:`InterfaceValue` s to variate and optimize.
                This is a :any:`dict` like
                ``variate[InterfaceValue()]=n_blocks`` where ``n_blocks`` is an
                :any:`int` specifying how many blocks are used across the time
                span to optimize this :any:`InterfaceValue`. Use ``1`` to
                optimize a constant (e.g. a parameter that doesn't change
                in time) and greater values for temporally variable values.
            time_start (float, optional): The time to start optimizing. Defaults
                to the earliest variable time in ``variate``.
            time_end (float, optional): The time to end optimizing. Defaults
                to the :any:`model_time`

        Kwargs:
            kwargs (dict, optional): further arguments passed to
            :any:`scipy.optimize.minimize`. ``method`` defaults to
            ``L-BFGS-B``.

        Returns:
            optimization result
        """
        minimize_kwargs = {"method": "L-BFGS-B"}
        minimize_kwargs.update(kwargs)
        # fix order of values to optimize
        variate = collections.OrderedDict(variate)
        for iv, nblocks in variate.items():
            assert nblocks > 0

        # determine time range to use
        if time_start is None:
            time_start = min(
                min([min(iv.times) for iv in variate.keys()]),
                min([min(iv.times) for iv in self.variables.values()]),
            )
        if time_end is None:
            time_end = max(
                self.model_time,
                max([max(iv.times) for iv in variate.keys()]),
                max([max(iv.times) for iv in self.variables.values()]),
            )
        if time_start >= time_end:
            logger.warning(
                "Optimization start time ({}) is not earlier than "
                "end time ({})! Setting end time to one second later "
                "than start time.".format(
                    time_start, time_end))
            time_end = time_start + 1
        logger.info("Optimize in time range {} to {}"
                    .format(time_start, time_end))

        # residual function
        def residual(state, *args):
            # check input for bounds
            for i, v in enumerate(state):
                lower, upper = bounds[i]
                if state[i] < lower:
                    logger.warning(
                        "scipy.optimize.minimize specified a value "
                        "smaller than the lower bound ({} > {})".format(
                            state[i], lower))
                    state[i] = max(state[i], lower)
                elif state[i] > upper:
                    logger.warning(
                        "scipy.optimize.minimize specified a value "
                        "greater than the upper bound ({} > {})".format(
                            state[i], upper))
                    state[i] = min(state[i], upper)

            # clear the time span
            self.reset(
                time=time_start,
                only=[
                    iv.id for iv in itertools.chain(
                        self.variables.values(),
                        variate.keys())])

            # set new state
            stateiter = iter(state)
            newstate = []
            for iv, nblocks in variate.items():
                iv.merge_accumulated()
                iv_newstate = []
                for i in range(nblocks):
                    iv_newstate.append(next(stateiter))
                newstate.append(iv_newstate)
            for iv, data in zip(variate.keys(), newstate):
                times = np.linspace(time_start, time_end, len(data))
                self.logger.info("Setting {} to {} at times {}".format(
                    iv.id, data, times))
                iv[slice(time_start, time_end)] = (times, data)

            # simulate
            self.integrate(final_time=time_end)

            # calculate residual
            res = 0

            for ivlist in bring_together:
                times = np.unique(np.concatenate(
                    [iv[slice(time_start, time_end)][0] for iv in ivlist]))
                res += utils.multi_rmse(*[iv(times) for iv in ivlist])

            logger.info("residual is {}".format(res))

            return res

        # first guess is current model state
        first_guess = []
        for iv, nblocks in variate.items():
            first_guess.extend(
                iv(np.linspace(time_start, time_end, nblocks)).flatten())
        logger.debug("first_guess: {}".format(first_guess))

        # get bounds
        bounds = []
        for iv, nblocks in variate.items():
            bounds.extend([iv.bounds] * nblocks)
        logger.debug("bounds: {}".format(bounds))

        # optimize
        try:
            result = scipy.optimize.minimize(
                fun=residual,
                x0=first_guess,
                bounds=bounds,
                **kwargs
            )
        except (KeyboardInterrupt, StopOptimization):
            self.reset(time=time_start,
                       only=[iv.id for iv in self.variables.values()])
            return False

        logger.debug("Optimization result:\n{}".format(result))

        for iv, nblocks in variate.items():
            values = iv[slice(time_start, time_end)][1]
            nlow, nhigh = (np.isclose(values, t).sum() for t in iv.bounds)
            if nlow:
                logger.warning("{} close to lower bound {}".format(
                    "{} is ".format(iv.id) if nlow == 1 else
                    "There are {} of {} values in '{}' that are ".format(
                        nlow, values.size, iv.id),
                    iv.bounds[0]))
            if nhigh:
                logger.warning("{} close to upper bound {}".format(
                    "{} is ".format(iv.id) if nhigh == 1 else
                    "There are {} of {} values in {} that are ".format(
                        nhigh, values.size, iv.id),
                    iv.bounds[1]))

        return result

    def gui(self, *args, **kwargs):  # pragma: no cover
        """
        Open a GTK window to interactively run the model:

        - change the model variables, parameters and forcing on the fly
        - directly see the model output
        - stepwise integration

        Args:
            args, kwargs : arguments passed to :any:`NumericalModelGui`
        """
        from numericalmodel.ui.gui import NumericalModelGui
        # create a gui
        gui = NumericalModelGui(numericalmodel=self,
                                *args, **kwargs)
        # run the gui
        gui.run()

    def cli(self, *args, **kwargs):
        """
        Command-line interface to run this :any:`NumericalModel`

        Args:
            args, kwargs : arguments passed to :any:`NumericalModelCli`
        """
        from numericalmodel.ui.cli import NumericalModelCli
        # create a cli
        cli = NumericalModelCli(model=self, *args, **kwargs)
        # run the cli
        cli.run()

    def __str__(self):  # pragma: no cover
        """
        Stringification

        Returns:
            str : a summary
        """
        # GenericModel stringificator
        gm_string = GenericModel.__str__(self)

        string = textwrap.dedent(
            """
            {gm_string}

            ##################
            ### Model data ###
            ##################

            initial time: {initialtime}

            #################
            ### Variables ###
            #################

            {variables}

            ##################
            ### Parameters ###
            ##################

            {parameters}

            ###############
            ### Forcing ###
            ###############

            {forcing}

            ####################
            ### Observations ###
            ####################

            {observations}

            ###############
            ### Schemes ###
            ###############

            {schemes}

            """
        ).strip().format(
            initialtime=self.initial_time,
            gm_string=gm_string,
            parameters=self.parameters,
            variables=self.variables,
            forcing=self.forcing,
            schemes=self.numericalschemes,
            observations=self.observations,
        )

        return string


class StopOptimization(RuntimeError):
    pass
