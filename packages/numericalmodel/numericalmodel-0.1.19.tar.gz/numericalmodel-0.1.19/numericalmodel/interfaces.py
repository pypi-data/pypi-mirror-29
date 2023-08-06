#!/usr/bin/env python3
# system modules
import logging
from collections import defaultdict
import inspect
import copy

# internal modules
from . import utils

# external modules
import numpy as np
import scipy.interpolate

logger = logging.getLogger(__name__)


class InterfaceValue(utils.ReprObject):
    """
    Base class for model interface values

    Args:
        name (str, optional): value name
        id (str, optional): unique id
        values (1d :any:`numpy.ndarray`, optional): all values this
            InterfaceValue had in chronological order
        times (1d :any:`numpy.ndarray`, optional): the corresponding times to
            values
        unit (str,optional): physical unit of value
        bounds (list, optional): lower and upper value bounds
        interpolation (str, optional): interpolation kind. See
            :any:`scipy.interpolate.interp1d` for documentation. Defaults to
            "linear".
        time_function (callable, optional): function that returns the model time
            as utc unix timestamp
        remembrance (float, optional): maximum :any:`time` difference to keep
            past :any:`values`
    """
    unit_converters = defaultdict(dict)
    """
    :any:`InterfaceValue` unit converters. Add or update converters with
    :any:`add_unit_converter` or set one directly with

    .. code:: python

        InterfaceValue.unit_converters["FROM"]["TO"] = lambda x: x

    :type: :any:`collections.defaultdict`
    """

    def __init__(self,
                 name=None,
                 id=None,
                 unit=None,
                 time_function=None,
                 interpolation=None,
                 values=None,
                 times=None,
                 bounds=None,
                 remembrance=None,
                 ):
        # set properties
        if time_function is not None:
            self.time_function = time_function
        if name is not None:
            self.name = name
        if unit is not None:
            self.unit = unit
        if id is not None:
            self.id = id
        if bounds is not None:
            self.bounds = bounds
        if values is not None:
            self.values = values
        if times is not None:
            self.times = times
        if interpolation is not None:
            self.interpolation = interpolation
        if remembrance is not None:
            self.remembrance = remembrance

    ####################
    ### Classmethods ###
    ####################
    @classmethod
    def add_unit_converter(cls, from_unit, to_unit, converter):
        """
        Add or update a unit converter to the :any:`unit_converters`

        Args:
            from_unit (str): the unit to convert from
            to_unit (str): the unit to convert to
            converter (callable): the converter, taking as single argument
                values in unit ``from_unit`` and returning values in unit
                ``to_unit``
        """
        assert hasattr(converter, "__call__"), "converter has to be callable"
        cls.unit_converters[from_unit][to_unit] = converter

    @classmethod
    def reset_unit_converters(cls):
        """
        Reset all unit converters
        """
        cls.unit_converters = defaultdict(dict)

    ##################
    ### Properties ###
    ##################
    @property
    def time_function(self):
        try:
            self._time_function  # already defined?
        except AttributeError:
            self._time_function = self._default_time_function
        return self._time_function  # return

    @time_function.setter
    def time_function(self, newtime_function):
        assert hasattr(newtime_function, '__call__'), \
            "time_function has to be callable"
        self._time_function = newtime_function

    @property
    def _default_time_function(self):
        """ Default time_function if none was given. Subclasses should
        overrtime_functione this.
        """
        return utils.utcnow

    @property
    def id(self):
        """
        The unique id

        :type: :any:`str`
        """
        try:
            self._id  # already defined?
        except AttributeError:
            self._id = self._default_id  # default
        return self._id  # return

    @id.setter
    def id(self, newid):
        assert isinstance(newid, str), "id has to be str"
        self._id = newid

    @property
    def _default_id(self):
        """
        Default id if none was given. Subclasses should override this.

        :type: :any:`str`
        """
        return "unnamed_variable"

    @property
    def unit(self):
        """
        The SI-unit.

        :type: :any:`str`, SI-unit
        """
        try:
            self._unit  # already defined?
        except AttributeError:
            self._unit = self._default_unit  # default
        return self._unit  # return

    @unit.setter
    def unit(self, newunit):
        assert isinstance(newunit, str), "unit has to be str"
        self._unit = newunit

    @property
    def _default_unit(self):
        """
        The default unit if none was given.

        :type: :any:`str`, SI-unit
        """
        return "1"

    @property
    def name(self):
        """
        The name.

        :type: :any:`str`
        """
        try:
            self._name  # already defined?
        except AttributeError:
            self._name = self._default_name  # default
        return self._name  # return

    @name.setter
    def name(self, newname):
        assert isinstance(newname, str), "name has to be str"
        self._name = newname

    @property
    def _default_name(self):
        """
        Default name if none was given.

        :type: :any:`str`
        """
        return "unnamed value"

    @property
    def value(self):
        """
        The current value.

        :getter:
            the current value
        :setter:
            When this property is set, the given value is recorded to the
            time given by :any:`next_time`. If this time exists already in
            :any:`times`, the corresponding value in :any:`values` is
            overwritten.  Otherwise, the new time and value are appended to
            :any:`times` and :any:`values`.
            The value is also checked to lie within the :any:`bounds`.
        :type: numeric
        """
        try:
            return self.accumulated_values[-1]  # first try accumulated values
        except IndexError:
            try:
                return self._values[-1]  # then try merged times
            except (AttributeError, IndexError):
                raise IndexError(
                    "{}: no values recorded yet".format(self.name))

    @value.setter
    def value(self, newvalue):
        assert utils.is_numeric(newvalue), "value has to be numeric"
        val = np.asarray(newvalue)  # convert to numpy array
        assert val.size == 1, "value has to be of size one"
        # check if values are inside bounds
        lower, upper = self.bounds
        assert np.all(newvalue >= lower), \
            ("{}: new value is smaller than lower bound {}").format(
                self.name, lower)
        assert np.all(newvalue <= upper), \
            ("{}: new value is greater than upper bound {}").format(
                self.name, upper)
        # append to log
        t = self.next_time  # the next time
        try:
            ind = self._times == t  # indices this next time is already present
        except AttributeError:
            ind = np.array([]) == t
        if np.any(ind):  # time already there?
            try:
                self._values[ind] = val  # replace value
                # logger.debug("time {t} already there, "
                #     "overwriting value to {val}".format(t=t,val=val))
            except AttributeError:
                self._values = val
        else:  # new time
            if t in self.accumulated_times:
                self.accumulated_values[self.accumulated_times.index(t)] = val
            else:
                self.accumulated_times.append(t)
                self.accumulated_values.append(val)
            # logger.debug("time {t} not yet there, "
            #     "appending value {val}".format(t=t,val=val))
        # reset interpolator
        self.interpolator = None

    @property
    def values(self):
        """
        All values this InterfaceValue has ever had in chronological order

        :getter: Return the current values
        :setter: Check if all new values lie within the :any:`bounds`
        :type: :any:`numpy.ndarray`
        """
        try:
            self._values
        except AttributeError:
            self._values = self._default_values  # default
        self.merge_accumulated()
        return self._values  # return

    @values.setter
    def values(self, newvalues):
        newvalues = np.asarray(newvalues)
        assert newvalues.size == np.prod(newvalues.shape), \
            "values have to be one-dimensional"
        # check if values are inside bounds
        lower, upper = self.bounds
        assert np.all(newvalues >= lower), \
            ("{}: new value is smaller than lower bound {}").format(
                self.name, lower)
        assert np.all(newvalues <= upper), \
            ("{}: new value is greater than upper bound {}").format(
                self.name, upper)
        self._values = newvalues
        self.accumulated_values = []
        # reset intepolator
        self.interpolator = None

    @property
    def accumulated_values(self):
        """
        Accumulated values not yet merged into :any:`values` for efficiency.

        :type: :any:`list`
        """
        try:
            self._accumulated_values
        except AttributeError:
            self._accumulated_values = []
        return self._accumulated_values

    @accumulated_values.setter
    def accumulated_values(self, newaccumulated_values):
        self._accumulated_values = list(newaccumulated_values)

    @property
    def accumulated_times(self):
        """
        Accumulated values not yet merged into :any:`values` for efficiency.

        :type: :any:`list`
        """
        try:
            self._accumulated_times
        except AttributeError:
            self._accumulated_times = []
        return self._accumulated_times

    @accumulated_times.setter
    def accumulated_times(self, newaccumulated_times):
        self._accumulated_times = list(newaccumulated_times)

    @property
    def _default_values(self):
        return np.array([])  # empty array

    @property
    def num_records(self):
        """
        Determine the number of time/value pairs

        :type: :any:`int`
        """
        n_merge = 0
        try:
            n_merge += self._times.size
        except AttributeError:
            pass
        return n_merge + len(self.accumulated_times)

    @property
    def next_time(self):
        """
        The next time to use when :any:`value` is set.

        :getter:
            Return the next time to use. Defaults to the value of
            :any:`time_function` if no :any:`next_time` was set.
        :setter:
            Set the next time to use. Set to :any:`None` to unset and use the
            default time in the getter again.
        :type: :any:`float`
        """
        try:
            next_time = self._next_time
        except AttributeError:
            next_time = self.time_function()
        try:
            assert next_time >= self.time, (
                "{}: next_time ({}) has to be later than current time "
                "({})").format(self.id, next_time, self.time)
        except IndexError:
            pass
        return next_time

    @next_time.setter
    def next_time(self, newtime):
        if newtime is None:  # if set to none
            if hasattr(self, "_next_time"):
                del self._next_time  # del attribute
        else:  # set to something else
            assert utils.is_numeric(newtime), "next_time has to be numeric"
            assert np.asarray(newtime).size == 1, \
                "next_time has to be one value"
            if self.num_records:
                assert newtime >= self.time, ("{}: next_time ({}) has to "
                                              "be later than current time ({})").format(
                    self.id, newtime, self.time)
            self._next_time = newtime

    @property
    def time(self):
        """
        The current time

        :getter:
            Return the current time, i.e. the last time recorded in
            :any:`times`.
        :type: :any:`float`
        """
        try:
            return self.accumulated_times[-1]  # first try accumulated times
        except IndexError:
            try:
                return self._times[-1]  # then try merged times
            except (AttributeError, IndexError):
                raise IndexError("{}: no times recorded yet".format(self.name))

    @property
    def times(self):
        """
        All times the :any:`value` has ever been set in chronological
        order

        :type: :any:`numpy.ndarray`
        """
        try:
            self._times
        except AttributeError:
            self._times = self._default_times  # default
        self.merge_accumulated()
        return self._times  # return

    @times.setter
    def times(self, newtimes):
        newtimes = np.asarray(newtimes)
        assert newtimes.size == np.prod(newtimes.shape), \
            "times have to be one-dimensional"
        assert np.all(np.diff(newtimes) >
                      0), "times must be strictly increasing"
        self._times = newtimes
        self.accumulated_times = []
        # reset intepolator
        self.interpolator = None

    @property
    def _default_times(self):
        """
        The default times to use when none were given. Defaults to empty
        :any:`numpy.ndarray`.

        :type: :any:`numpy.ndarray`
        """
        return np.array([])  # empty array

    @property
    def bounds(self):
        """
        The :any:`values`' bounds. Defaults to an infinite interval.

        :getter: Return the current bounds
        :setter: If the bounds change, check if all :any:`values` lie within the
            new bounds.
        :type: :any:`list`, ``[lower, upper]``
        """
        try:
            self._bounds  # already defined?
        except AttributeError:
            self._bounds = self._default_bounds  # default
        return self._bounds  # return

    @bounds.setter
    def bounds(self, newbounds):
        try:
            lower, upper = newbounds
        except (ValueError, TypeError):
            raise ValueError("bounds must be sequence like [lower,upper]")
        assert lower < upper, \
            "new lower bound has to be smaller than upper bound"
        newbounds = (lower, upper)
        if self.bounds != newbounds:  # bounds changed
            # check the values for the new bounds
            assert np.all(self.values >= newbounds[0]), \
                "there are values greater than the new upper bound"
            assert np.all(self.values <= newbounds[1]), \
                "there are values greater than the new upper bound"
        self._bounds = newbounds

    @property
    def _default_bounds(self):
        """
        The default bounds to use when none were given.

        :type: :any:`list`
        """
        return (-np.Inf, np.Inf)  # unlimited

    @property
    def remembrance(self):
        """
        How long should this :any:`InterfaceValue` store it's :any:`values`?
        This is the greatest difference the current :any:`time` may have to the
        smallest :any:`time`. Values earlier than the :any:`remembrance` time
        are discarded. Set to :any:`None` for no limit.

        :type: :any:`float` or :any:`None`
        """
        try:
            self._remembrance  # already defined?
        except AttributeError:
            self._remembrance = self._default_remembrance
        return self._remembrance  # return

    @remembrance.setter
    def remembrance(self, newremembrance):
        if newremembrance is None:
            self._remembrance = newremembrance
        else:
            remembrance = float(newremembrance)
            assert remembrance >= 0, "remembrance has to be positive float"
            self._remembrance = remembrance

    @property
    def _default_remembrance(self):
        """
        Default :any:`remembrance` if none was given.

        :type: :any:`float64`
        """
        return None

    @property
    def interpolation(self):
        """
        The interpolation kind to use in the :any:`__call__` method. See
        :any:`scipy.interpolate.interp1d` for documentation.

        :getter:
            Return the interplation kind.
        :setter:
            Set the interpolation kind. Reset the internal interpolator if the
            interpolation kind changed.

        :type: :any:`str`
        """
        try:
            self._interpolation  # already defined?
        except AttributeError:
            self._interpolation = self._default_interpolation
        return self._interpolation  # return

    @interpolation.setter
    def interpolation(self, newinterpolation):
        assert isinstance(newinterpolation, str), "interpolation has to be str"
        if newinterpolation != self.interpolation:  # really new value
            if hasattr(self, "_interpolator"):
                del self._interpolator  # reset interpolator
        self._interpolation = newinterpolation

    @property
    def _default_interpolation(self):
        """
        Default interpolation if none was given is ``"linear"``, i.e.
        linear interpolation. Subclasses may override this.

        :type: :any:`str`
        """
        return "linear"

    @property
    def interpolator(self):
        """
        The interpolator for interpolation of :any:`values` over :any:`times`.
        Creating this interpolator is costly and thus only performed on demand,
        i.e. when :any:`__call__` is called **and** no interpolator was created
        previously or the previously created interolator was unset before (e.g.
        by setting a new :any:`value` or changing :any:`interpolation`)

        :type: :any:`scipy.interpolate.interp1d`
        """
        try:
            self._interpolator  # try to access internal attribute
        except AttributeError:  # doesn't exist
            self._interpolator = scipy.interpolate.interp1d(
                x=self.times,  # the times
                y=self.values,  # the values
                assume_sorted=True,  # times are already sorted
                copy=False,  # don't copy
                kind=self.interpolation,  # interpolation kind
                bounds_error=False,  # don't escalate on outside values
                fill_value=(self.values[self.times.argmin()],
                            self.values[self.times.argmax()]),  # fill
            )
        return self._interpolator

    @interpolator.setter
    def interpolator(self, value):
        if value is None:  # reset the interpolator
            if hasattr(self, "_interpolator"):
                del self._interpolator
        else:  # pragma: no cover
            assert hasattr(value, "__call__"), "interpolator must be callable"
            self._interpolator = value

    ###############
    ### Methods ###
    ###############
    def merge_accumulated(self):
        """
        Merge the :any:`accumulated_times` and :any:`accumulated_values` into
        :any:`times` and :any:`values`.

        Returns:
            bool : :any:`True` if data was merged, :any:`False` otherwise
        """
        assert len(self.accumulated_times) == len(self.accumulated_values), \
            "length of accumulated times and values don't match"
        if len(self.accumulated_values) > 0:
            logger.debug("{}: merging {} accumulated values...".format(
                self.id, len(self.accumulated_values)))
            try:
                self.times = \
                    np.append(self._times, np.array(self.accumulated_times))
            except AttributeError:
                self.times = np.array(self.accumulated_times)
            try:
                self.values = \
                    np.append(self._values, np.array(self.accumulated_values))
            except AttributeError:
                self.values = np.array(self.accumulated_values)
            # for get old values
            self.forget_old_values()
            return True
        else:  # nothing to do
            return False

    def cut(self, start=None, end=None):
        """
        Drop :any:`values` and :any:`times` outside a given time range.

        Args:
            start, end (float, optional): start and end time to keep data. Use
            ``None`` for no limit in that direction.
        """
        self.merge_accumulated()
        self._times, self._values = self[slice(start, end)]

    def forget_old_values(self):
        """
        Drop :any:`values` and :any:`times` older than :any:`remembrance`.
        """
        try:
            self.cut(self.time - self.remembrance, None)
        except TypeError:  # no remembrance
            pass

    def interpolate(self, times=None):
        """
        Return the value at given times

        Args:
            times (numeric, optional): The times to obtain data from
        """
        assert self.num_records, "{}: no values recorded yet".format(self.name)
        if times is None or np.all(np.asarray(times) == self.time):
            # no time given or only one value there
            try:
                return self.accumulated_values[-1]
            except IndexError:
                return self.value
        assert utils.is_numeric(times), "times have to be numeric"
        times = np.asarray(times)  # convert to numpy array
        if self.num_records == 1:
            return np.ones_like(times) * self.values[-1]

        return self.interpolator(times)  # return

    def copy(self, deep=False, **kwargs):
        """
        Return a copy of this object.

        Args:
            deep (bool, optional): Return a deep copy instead of a shallow one?
            kwargs : further arguments passed to :any:`InterfaceValue`
                constructor

        Returns:
            InterfaceValue : a copy of this object
        """
        initkwargs = self.__initkwargs(deep=deep)
        initkwargs.update(kwargs)
        return self.__class__(**initkwargs)

    def convert(self, unit, **kwargs):
        """
        Create a copy of this :any:`InterfaceValue` converted to another
        ``unit``. Make sure to ``add_unit_converter`` before.

        Args:
            unit (str): The unit to convert to.
            **kwargs: Further update arguments to pass
                to :any:`InterfaceValue.copy`

        Returns:
            InterfaceValue : A copy of this :any:`InterfaceValue` converted to
                ``unit``.

        Raises:
            ValueError: If no converter was found in ``unit_converters`` to
                convert this ``InterfaceValue.unit`` to the desired ``unit``.
        """
        try:
            converter = self.unit_converters[self.unit][unit]
        except KeyError:
            raise ValueError("Don't know how to convert this unit '{this}' to "
                "desired unit '{desired}'. Add a unit converter "
                "via {cls}.{add}('{this}','{desired}',lambda x: ...)".format(
                this=self.unit,desired=unit, cls=self.__class__.__name__,
                add=self.__class__.add_unit_converter.__name__))
        bounds_converted = [converter(np.array(x)) for  x in self.bounds]
        newbounds = [min(bounds_converted),max(bounds_converted)]
        newvalues = converter(self.values)
        copy_kwargs = {}
        copy_kwargs.update(
            {"bounds": newbounds,"values":newvalues,"unit":unit})
        copy_kwargs.update(kwargs)
        my_copy = self.copy(**copy_kwargs)
        return my_copy

    #######################
    ### Special Methods ###
    #######################
    def __getitem__(self, ind):
        """
        When indexed with a slice, return values inside this :any:`times` range.
        When indexed with something numeric, :any:`interpolate`.
        """
        try:  # slice
            start, stop, step = ind.start, ind.stop, ind.step
            start = -np.Inf if start is None else start
            stop = np.Inf if stop is None else stop
            # clear the time span
            keep = np.where(np.logical_and(
                start <= self.times, self.times <= stop))[0]
            return self.times[keep], self.values[keep]
        except AttributeError:  # index
            return self.interpolate(ind)

    def __setitem__(self, ind, value):
        """
        When a single time is set, set the appropriate value.
        When a slice is set, update the range
        """
        value = np.asarray(value)
        try:  # slice
            start, stop, step = ind.start, ind.stop, ind.step
            start = -np.Inf if start is None else start
            stop = np.Inf if stop is None else stop
            # clear the time span
            try:
                indices = np.where(np.logical_and(
                    start <= self.times, self.times <= stop))[0]
                self.values[indices] = value
            except ValueError:  # shape mismatch
                try:
                    times, values = value
                    # determine indices
                    indices_before = np.where(self.times < start)[0]
                    indices_after = np.where(self.times > stop)[0]
                    # set up arrays
                    values_before = self.values[indices_before]
                    times_before = self.times[indices_before]
                    values_after = self.values[indices_after]
                    times_after = self.times[indices_after]
                    shape = list(values_before.shape)
                    shape[0] = values.shape[0]
                    newvalues = values.reshape(shape)
                    newtimes = times
                    # set new values
                    self.values = np.concatenate(
                        [values_before, newvalues, values_after])
                    self.times = np.concatenate(
                        [times_before, newtimes, times_after])
                except ValueError:
                    raise ValueError("Specify tuple (times,values)")
        except AttributeError:  # index
            try:  # try iterable
                for t, v in zip(ind, value):
                    self[t] = v
            except TypeError:  # ind or value not iterable, try single value
                if ind is None:
                    self.value = value
                else:
                    index = np.where(self.times == ind)[0]
                    if index.size == 0:  # index not yet here
                        # determine indices
                        indices_before = np.where(self.times < ind)[0]
                        indices_after = np.where(self.times > ind)[0]
                        # set up arrays
                        values_before = self.values[indices_before]
                        times_before = self.times[indices_before]
                        values_after = self.values[indices_after]
                        times_after = self.times[indices_after]
                        shape = list(values_before.shape)
                        shape[0] = 1
                        newvalue = value.reshape(shape)
                        newtime = np.array(ind).reshape((1,))
                        # set new values
                        self.values = np.concatenate(
                            [values_before, newvalue, values_after])
                        self.times = np.concatenate(
                            [times_before, newtime, times_after])
                    elif index.size == 1:  # exactly one value
                        self.values[index] = value
                    else:
                        raise ValueError(
                            "Time {} present multiple times!".format(ind))

    def __call__(self, times=None):
        """
        When called, :any:`interpolate`.
        """
        return self.interpolate(times)

    def __initkwargs(self, deep=False):
        """
        Return the keyword arguments that can be passed to
        :any:`InterfaceValue.__init__` to create an object equal to this one
        """
        c = copy.deepcopy if deep else copy.copy
        return {
            v: c(
                getattr(
                    self,
                    v)) for v in [
                n for n in inspect.getfullargspec(
                    self.__init__).args if not n == "self"]}

    def __copy__(self):
        """
        Return a shallow copy of this object
        """
        kwargs = self.__initkwargs(deep=False)
        return self.__class__(**kwargs)

    def __deepcopy__(self, memo=None):
        """
        Return a deep copy of this object
        """
        kwargs = self.__initkwargs(deep=True)
        return self.__class__(**kwargs)

    def __str__(self):  # pragma: no cover
        """
        Stringification

        Returns:
            str : a summary
        """
        if self.values.size:
            value = self.value
        else:
            value = "?"
        string = (
            " \"{name}\" \n"
            "--- {id} [{unit}] ---\n"
            "currently: {value} [{unit}]\n"
            "bounds: {bounds}\n"
            "interpolation: {interp} \n"
            "{nr} total recorded values").format(
            id=self.id,
            unit=self.unit,
            interp=self.interpolation,
            name=self.name,
            value=value,
            nr=self.values.size,
            bounds=self.bounds)
        return string


##############################
### Set of InterfaceValues ###
##############################
class SetOfInterfaceValues(utils.SetOfObjects):
    """
    Base class for sets of interface values

    Args:
        elements (:any:`list` of :any:`InterfaceValue`, optional): the list of
            elements
    """

    def __init__(self, elements=[]):
        super().__init__(  # call SetOfObjects constructor
            elements=elements,
            element_type=lambda x: isinstance(x, InterfaceValue)
        )

    @property
    def time_function(self):
        """
        The time function of all the :any:`InterfaceValue` s in the set.

        :getter:
            Return a :any:`list` of time functions from the elements
        :setter:
            Set the time function of each element
        :type: (:any:`list` of) callables
        """
        return [e.time_function for e in self.elements]

    @time_function.setter
    def time_function(self, newfunc):
        assert hasattr(newfunc, '__call__'), "time_function has to be callable"
        for e in self.elements:  # set every element's time_function
            e.time_function = newfunc

    ###############
    ### Methods ###
    ###############
    def _object_to_key(self, obj):
        """ key transformation function.

        Args:
            obj (object): the element

        Returns:
            key (str): the unique key for this object. The
            :any:`InterfaceValue.id` is used.
        """
        return obj.id

    def __call__(self, id):
        """
        Get the value of an :any:`InterfaceValue` in this set

        Args:
            id (str): the id of an :any:`InterfaceValue` in this set

        Returns:
            float : the :any:`value` of the corresponding :any:`InterfaceValue`
        """
        return self[id].value
