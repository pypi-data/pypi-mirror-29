#!/usr/bin/env python3
# system modules
import logging
import warnings
import inspect
import re
import json
import datetime
import collections
import itertools
import csv

# internal modules

# external modules
import numpy as np


######################
### util functions ###
######################
def extract_leading_comment_block(f, comment_regex = r"^#\s*(.*)$",
    only_content = True):
    """
    Extract a leading comment block from a file. If no comment block was
    found, the file handle is reset to where it was before. Trailing whitespace
    is removed.

    Args:
        f (filehandle): file handle
        comment_regex (str, optional): the regular expression defining what is
            treated as a comment. Should capture a single group of text which
            is then used further on. Defaults to shell-like comments.
        only_content (bool, optional): Whether to return only the content of
        the comment block, i.e. the ``comment_regex`` matched group or the
        whole comment block. Defaults to ``True``.

    Returns:
        str : the leading comment block

    Raises:
        ValueError : if the ``comment_regex`` does not capture a group and
            ``only_content=True``.
    """
    comment_regex = re.compile(comment_regex)
    content = []
    current_position = f.tell()
    line = f.readline()
    while line:
        line = line.rstrip()
        m = comment_regex.match(line)
        if m:
            if only_content:
                try:
                    content.append(m.group(1))
                except IndexError:
                    f.seek(current_position)
                    raise ValueError("Given comment_regex '{}' does not "
                        "capture a group which is required if "
                        "only_content=True".format(comment_regex.pattern))
            else:
                content.append(line)
        else:
            f.seek(current_position)
            break
        current_position = f.tell()
        line = f.readline()
    return "\n".join(content)

def read_csv(f, *args, **kwargs):
    """
    Read CSV from file and return a dict

    Args:
        f (filehandle): file handle
        args, kwargs: arguments passed to :any:`csv.DictReader`

    Returns:
        dict : keys are column names, values are column data
    """
    d = {}
    csvreader = csv.DictReader(f, *args, **kwargs)

    def tofloat(x):
        try:
            return float(x)
        except ValueError:
            return x
    d = dictlist_to_listdict(csvreader, fun=tofloat)
    return d


def write_csv(f, d, headersortkey=lambda x: x, *args, **kwargs):
    """
    Write CSV dict to file

    Args:
        f (filehandle): writeable file handle
        headersortkey (callable): ``key`` argument to :any:`sorted` to sort the
            header columns
        args, kwargs: arguments passed to :any:`csv.DictWriter`
    """
    csvwriter = csv.DictWriter(
        f, fieldnames=sorted(d.keys(), key=headersortkey), *args, **kwargs)
    l = listdict_to_dictlist(d)
    csvwriter.writeheader()
    for row in l:
        csvwriter.writerow(row)


def listdict_to_dictlist(d):
    """
    Convert a :any:`dict` of lists to a list of dicts

    Args:
        d (dict): the dict of lists

    Returns:
        list : list of dicts
    """
    return [dict(zip(d, t)) for t in zip(*d.values())]


def dictlist_to_listdict(l, fun=lambda x: x):
    """
    Convert a list of dicts to a dict of lists

    Args:
        l (list): the list of dicts
        fun (callable): callable to manipulate the values

    Returns:
        dict : dict of lists
    """
    d = collections.defaultdict(list)
    for e in l:
        for k, v in e.items():
            d[k].append(fun(v))
    return dict(d)


def is_numeric(x):
    """
    Check if a given value is numeric, i.e. whether numeric operations can be
    done with it.

    Args:
        x (any): the input value

    Returns:
        bool: ``True`` if the value is numeric, ``False`` otherwise
    """
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(x, attr) for attr in attrs)


def utcnow():
    """
    Get the current utc unix timestamp, i.e. the utc seconds since 01.01.1970.

    Returns:
        float : the current utc unix timestamp in seconds
    """
    ts = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
          ).total_seconds()
    return ts


def rmse(a, b):
    """
    RMSE (root mean squared error)
    """
    return np.sqrt(np.mean((a - b)**2))


def multi_rmse(*args):
    """
    RMSE (root mean squared error) for more than 2 elements
    """
    return np.mean([rmse(a, b) for a, b in itertools.combinations(args, 2)])

def multi_func(*args,f,norm=False):
    """
    Multi func
    """
    for n,v in enumerate(args):
        try: res = f(res,v)
        except NameError: res = v
    return res / (n + 1) if norm else res

def linear_regression(x, y, fit_intercept=True, return_stats=False):
    """
    Fit :math:`y = a * x + b`

    Args:
        x (numpy.ndarray): the x values. Will be flattened.
        y (numpy.ndarray): the y values. Will be flattened.
        fit_intercept (bool, optional): Fit an intercept? Defaults to ``False``.


    Returns:
        float, float : if return_stats is ``False``,
            :math:`a` and :math:`b`. If ``fit_intercept=False``,
            :math:`b` is ``0``.
        float, float, numpy.ndarray, float: if return_stats is
            ``True``, :math:`a`, :math:`b`, the predicted values and the
            :math:`R^2` value.

    """
    A = x.reshape((x.size, 1))
    if fit_intercept:
        A = np.hstack([A, np.ones_like(A)])
        a, b = np.linalg.lstsq(A, y)[0]
    else:
        a, b = np.linalg.lstsq(A, y)[0], 0
    if return_stats:
        prediction = a * x + b
        SS_tot = np.sum( (y - np.mean(y)) ** 2 )
        SS_res = np.sum( (y - prediction) ** 2 )
        R_squared = 1 - SS_res / SS_tot
        return float(a), float(b), prediction, float(R_squared)
    else:
        return float(a), float(b)


####################
### util classes ###
####################


class ReprObject(object):
    """
    Simple base class that defines a :any:`__repr__` method based on an object's
    ``__init__`` arguments and properties that are named equally. Subclasses of
    :any:`ReprObject` should thus make sure to have properties that are named
    equally as their ``__init__`` arguments.
    """
    @classmethod
    def _full_variable_path(cls, var):
        """ Get the full string of a variable

        Args:
            var (any): The variable to get the full string from

        Returns:
            str : The full usable variable string including the module
        """
        if inspect.ismethod(var):  # is a method
            string = "{module}.{cls}.{name}".format(
                name=var.__name__, cls=var.__self__.__class__.__name__,
                module=var.__module__)
        else:
            name = var.__name__
            module = var.__module__
            if module == "builtins":
                string = name
            else:
                string = "{module}.{name}".format(name=name, module=module)
        return(string)

    def __repr__(self):
        """
        Python representation of this object

        Returns:
            str : a Python representation of this object based on its
            ``__init__`` arguments and corresponding properties.
        """
        indent = "    "
        # the current "full" classname
        classname = self._full_variable_path(self.__class__)

        # get a dict of {'argname':'property value'} from init arguments
        init_arg_names = inspect.getfullargspec(self.__init__).args
        init_args = {}  # start with empty dict
        for arg in init_arg_names:
            if arg == "self":
                continue  # TODO hard-coded 'self' is bad
            try:
                attr = getattr(self, arg)  # get the attribute
                try:
                    string = self._full_variable_path(attr)
                except BaseException:
                    string = repr(attr)

                # indent the arguments
                init_args[arg] = re.sub(
                    string=string,
                    pattern="\n",
                    repl="\n" + indent,
                )
            except AttributeError:  # no such attribute
                warnstr = (
                    "class {cls} has no property or attribute "
                    "'{arg}' like the argument in its __init__. Cannot include "
                    "argument '{arg}' into __repr__.").format(
                    cls=classname, arg=arg)
                warnings.warn(warnstr)

        # create "arg = {arg}" string list for reprformat
        args_kv = []
        for arg in init_args.keys():
            args_kv.append(indent + "{arg} = {{{arg}}}".format(arg=arg))

        # create the format string
        if args_kv:  # if there are arguments
            reprformatstr = "\n".join([
                "{____classname}(", ",\n".join(args_kv), indent + ")", ])
        else:  # no arguments
            reprformatstr = "{____classname}()"

        # add classname to format args
        reprformatargs = init_args.copy()
        reprformatargs.update({"____classname": classname})

        reprstring = (reprformatstr).format(**reprformatargs)
        return reprstring


class SetOfObjects(ReprObject, collections.MutableMapping):
    """
    Base class for sets of objects
    """

    def __init__(self, elements=[], element_type=object):
        self.store = dict()  # empty dict

        # set properties
        self.element_type = element_type
        self.elements = elements

    ##################
    ### Properties ###
    ##################
    @property
    def elements(self):
        """
        return the list of values

        :getter:
            get the list of values
        :setter:
            set the list of values. Make sure, every element in the list is an
            instance of (a subclass of) :any:`element_type`.
        :type: :any:`list`
        """
        return [self.store[x] for x in sorted(self.store)]

    @elements.setter
    def elements(self, newelements):
        assert isinstance(newelements, collections.Iterable), (
            "elements have to be list")
        # re-set the dict and fill it with new data
        tmp = dict()  # temporary empty dict
        for i, elem in enumerate(newelements):
            assert self.element_type(elem), \
                "new element nr. {} does not match type".format(i)
            key = self._object_to_key(elem)  # get the key
            assert key not in tmp, \
                "element '{}' present multiple times".format(key)
            tmp.update({key: elem})  # add to temporary dict

        self.store = tmp.copy()  # set internal dict

    @property
    def element_type(self):
        """
        Function to check if a given element is okay. Takes the new element as
        single argument and returns ``True`` if yes, ``False`` otherwise.

        :setter: If set to a class, it is set to ``lambda x:
            isisntance(x,class)``
        """
        try:
            self._element_type
        except AttributeError:
            self._element_type = lambda x: True  # default
        return self._element_type

    @element_type.setter
    def element_type(self, newtype):
        f = (lambda x: isinstance(x, newtype)) \
            if inspect.isclass(newtype) else newtype
        assert hasattr(f, "__call__"), "element_type has to be callable"
        self._element_type = f

    ###############
    ### Methods ###
    ###############
    def _object_to_key(self, obj):
        """ key transformation function. Subclasses should override this.

        Args:
            obj (object): object

        Returns:
            str : the unique key for this object. Defaults to ``repr(obj)``
        """
        return repr(obj)  # by default, return the object's repr

    def add_element(self, newelement):
        """
        Add an element to the set

        Args:
            newelement : the new element
        """
        tmp = self.elements.copy()  # TODO does this destroy references?
        tmp.append(newelement)
        self.elements = tmp

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        assert self.element_type(value), "new value does not match type"
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__, attr))

    def __str__(self):  # pragma: no cover
        """
        Stringification

        Returns:
            str : a summary
        """
        string = "\n\n".join(str(x) for x in self.elements)
        if string:
            return string
        else:
            return "none"
