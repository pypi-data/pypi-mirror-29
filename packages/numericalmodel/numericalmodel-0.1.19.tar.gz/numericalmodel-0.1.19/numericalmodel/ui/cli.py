# system modules
import argparse
import logging
import datetime
import textwrap
import itertools
import sys
import re
import os
import json
import locale
import gettext

# internal modules
from numericalmodel.utils import read_csv, write_csv, \
    extract_leading_comment_block
from numericalmodel.interfaces import *
from numericalmodel.ui.plot import plot_interfacevalues
from numericalmodel.ui.utils import GETTEXT_DOMAIN, LOCALEDIR

# from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# external modules
import IPython
import numpy as np

# set up localization
locale.setlocale(locale.LC_ALL, '')
for mod in [locale, gettext]:
    mod.bindtextdomain(GETTEXT_DOMAIN, LOCALEDIR)
gettext.textdomain(GETTEXT_DOMAIN)
gettext.install(GETTEXT_DOMAIN, localedir=LOCALEDIR)

class NumericalModelArgumentParser(argparse.ArgumentParser):
    """
    An :any:`argparse.ArgumentParser` with predefined arguments useful for
    command-line interface of :any:`NumericalModel`.
    """

    def __init__(self, *args, **kwargs):
        instruction_parser = NumericalModelCliInstructionParser()
        parser_kwargs = {
            "description": "NumericalModel cli",
            "epilog": instruction_parser.INSTRUCTIONS_HELP,
            "formatter_class": argparse.RawDescriptionHelpFormatter
        }
        parser_kwargs.update(kwargs)

        super().__init__(*args, **parser_kwargs)

        self.add_argument("-v", "--verbose", help="run verbosely",
                          action="store_true")
        self.add_argument("-d", "-vv", "--debug", help="run with debug output",
                          action="store_true")
        self.add_argument("-i", "--input",
                          help="read instructions from file after processing "
                          "command-line arguments. Set to '-' for STDIN",
                          default=None,)

        self.add_argument("instructions", nargs="*",
                          help="Sequence of control statements.",
                          type=instruction_parser, default=[])


class NumericalModelCli(object):
    CLI_HELP = "To exit, type 'exit' or 'quit' or press CTRL-D."

    def __init__(self, model=None, argparser=None):
        self.model = model
        self.argparser = argparser

    @property
    def prompt(self):
        """
        The displayed prompt
        """
        return "{} >>>".format(self.model.name)

    @property
    def model(self):
        """
        The :any:`NumericalModel` behind the cli

        :type: :any:`NumericalModel`
        """
        try:
            return self._model
        except AttributeError:
            self._model = NumericalModel()
        return self._model

    @model.setter
    def model(self, newmodel):
        if newmodel is None:
            try:
                del self._model
            except AttributeError:
                pass
        else:
            assert all([hasattr(newmodel, a) for a in
                        ["integrate", "variables", "forcing", "parameters",
                         "observations"]])
            self._model = newmodel

    @property
    def argparser(self):
        """
        The :any:`argparse.ArgumentParser` to use for the cli

        :type: :any:`argparse.ArgumentParser`
        """
        try:
            return self._argparser
        except AttributeError:
            self._argparser = NumericalModelArgumentParser(
                description="command-line interface for {}"
                .format(self.model.name))
        return self._argparser

    @argparser.setter
    def argparser(self, newargparser):
        if newargparser is None:
            try:
                del self._argparser
            except AttributeError:
                pass
        else:
            assert all([hasattr(newargparser, a) for a in
                        ["parse_args", "instructions"]])
            self._argparser = newargparser

    @property
    def logger(self):
        """
        Logger
        """
        return logging.getLogger(self.__class__.__name__)

    @property
    def args(self):
        """
        The parsed arguments
        """
        try:
            return self._args
        except AttributeError:
            self._args = self.argparser.parse_args()
        return self._args

    @property
    def args_loglevel(self):
        """
        The loglevel to use, determined by :any:`args`
        """
        loglevel = logging.WARNING
        if self.args.verbose:
            loglevel = min(loglevel, logging.INFO)
        if self.args.debug:
            loglevel = min(loglevel, logging.DEBUG)
        return loglevel

    def execute_instructions(self, instructions=[]):
        """
        Execute given instructions

        Args:
            instructions (list, optional): The instructions to perform
        """
        def find_iv(ivid):
            iv = self.model.find(ivid)
            if not iv:
                self.logger.warning(
                    "name '{}' not found in model".format(ivid))
            return iv

        def all_ivids():
            res = []
            for a in \
                    ["variables", "parameters", "forcing", "observations"]:
                res.extend(getattr(self.model, a).keys())
            return res

        cp = NumericalModelCliInstructionParser
        for instruction in instructions:
            for action, p in instruction.items():
                self.logger.info("{} {}".format(self.prompt, p[cp.KW_CMD]))
                # variable assignment
                if action == cp.KW_ASSIGNMENT:
                    iv = find_iv(p[cp.KW_ID])  # find InterfaceValue
                    if iv:
                        self.logger.info(
                            "Setting '{}' to {} at time {}".format(
                            iv.id, p[cp.KW_VALUE], p[cp.KW_TIME]))
                        iv[p[cp.KW_TIME]] = p[cp.KW_VALUE]
                # reset
                elif action == cp.KW_RESET:
                    model_ivids = all_ivids()
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids)}
                    self.model.reset( time = p[cp.KW_SECONDS],
                        past_also = p[cp.KW_BOOL], only = only )
                # integration
                elif action == cp.KW_INTEGRATE:
                    if p[cp.KW_SECONDS]:
                        self.model.integrate(seconds=p[cp.KW_SECONDS])
                    else:
                        try:
                            minvartime = min([iv.times.min() \
                                for ivid,iv in self.model.variables.items()])
                            maxvartime = max([iv.times.max() \
                                for ivid,iv in self.model.variables.items()])
                        except ValueError:
                            self.logger.warning("Could not determine variable "
                            "times. Skip integration!".format(time_msg,ivid))
                            continue
                        self.model.reset(minvartime,
                            only=self.model.variables.keys())
                        self.model.integrate(final_time = maxvartime)
                # file input
                elif action == cp.KW_FILEINPUT:
                    import_seconds_offset = 0
                    with open(p[cp.KW_FILE]) as f:
                        comment_content = extract_leading_comment_block(f)
                        if comment_content and not p[cp.KW_NOMETA]:
                            # extract comment block
                            try:
                                metadata = json.loads(comment_content)
                                self.logger.info("metadata: {}"\
                                    .format(metadata))
                                meta_zero_date = \
                                    metadata.get("zero_date")
                                if meta_zero_date:
                                    try:
                                        meta_zero_date = np.datetime64(
                                            meta_zero_date).astype(object)
                                        self.logger.info("Setting the "
                                            "model's zero_date to {}".format(
                                            meta_zero_date))
                                        if self.model.zero_date:
                                            self.logger.info("The model "
                                            "already has a zero_date of '{}'. "
                                            "Ignoring the file's zero_date "
                                            "'{}'.".format(
                                            self.model.zero_date,
                                            meta_zero_date
                                            ))
                                        else:
                                            try:
                                                self.model.zero_date = \
                                                    meta_zero_date
                                            except ValueError as e:
                                                self.logger.warning(
                                                "Could not "
                                                "change the model's zero_date "
                                                "from '{}' to '{}': {}".format(
                                                self.model.zero_date,
                                                meta_zero_date, e))
                                    except ValueError:
                                        meta_zero_date = \
                                            datetime.datetime.now()
                                try:
                                    import_seconds_offset = (meta_zero_date \
                                        - self.model.zero_date).total_seconds()
                                except TypeError: # no model time set
                                    pass
                            except json.JSONDecodeError as e:
                                self.logger.warning("Could not interpret "
                                "the metadata block '{}' of file '{}' as "
                                "JSON: {}. Ignoring it."\
                                .format(comment_content, p[cp.KW_FILE], e))
                        else:
                            self.logger.debug("Skipping metadata block of "
                                "file '{}'".format(p[cp.KW_FILE]))
                        data = read_csv(f)
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else data.keys())}
                    # rename ids in file to ids in model
                    for id_in_file, id_in_model \
                        in p[cp.KW_TRANSLATION].items():
                        try:
                            data[id_in_model] = data.pop(id_in_file)
                        except KeyError:
                            pass
                        try:
                            only[id_in_model] = only.pop(id_in_file)
                        except KeyError:
                            pass
                    for ivid, values in data.items():
                        if ivid == "time":
                            continue
                        if ivid in only:
                            iv = find_iv(ivid)
                            if not iv:
                                continue
                            try:
                                times = data["time"]
                            except KeyError:
                                time_msg = ("File '{}' does not contain 'time'"
                                    " column").format(p["file"])
                                if len(values) == iv.times.size:
                                    times = iv.times
                                elif len(values) == 1:
                                    if iv.times.size:
                                        mi,ma = \
                                            iv.times.min(), iv.times.max()
                                    else:
                                        self.logger.warning("{} and '{}' has "
                                        "no time recorded yet. Using model "
                                        "time {}.".format(time_msg,ivid,
                                            self.model.model_time))
                                        mi,ma = [self.model.model_time]*2
                                    times = np.linspace(mi,ma,len(values))
                                    values = values * np.ones_like(values)
                                else:
                                    self.logger.warning("{} and '{}' has "
                                    "{} times recorded yet but {} "
                                    "should be imported. "
                                    "Skip import!".format(time_msg,ivid,
                                        iv.times.size,len(values)))
                            times = np.array(times)
                            values = np.array(values)
                            if import_seconds_offset:
                                self.logger.info("Offsetting imported '{}' "
                                    "times by {} seconds to match model "
                                    "zero_date".format(
                                    ivid, import_seconds_offset))
                                times = times + import_seconds_offset
                            self.logger.info("Importing '{}'".format(ivid))
                            # set the values
                            if p[cp.KW_REPLACE]:
                                self.logger.debug("Replacing '{}' to {} at "
                                    "times {}".format(ivid, values, times))
                                t_slice = slice(None)
                            else:
                                self.logger.debug("Updating '{}' to {} at "
                                    "times {}".format(ivid, values, times))
                                t_slice = slice(times.min(),times.max())
                            iv[t_slice] = (times,values)
                        else:
                            self.logger.debug("Skipping '{}'".format(ivid))
                            continue
                # file output
                elif action == cp.KW_DUMP:
                    model_ivids = all_ivids()
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids)}
                    ivs = {ivid: find_iv(ivid)
                           for ivid in only if find_iv(ivid)}
                    if ivs:
                        times = np.unique(np.concatenate(
                            [iv.times for ivid, iv in ivs.items()]))
                        # eliminate duplicates due to string conversion
                        times = np.array([float(x[0]) for x in
                                          itertools.groupby([str(i) for i in times])])
                        # only dump until model time
                        times = times[times<=self.model.model_time]
                        d = {ivid: iv(times).flatten()
                             for ivid, iv in ivs.items()}
                        d["time"] = times
                        for id_f, id_m in p[cp.KW_TRANSLATION].items():
                            try:
                                d[id_m] = d.pop(id_f)
                            except KeyError:
                                pass
                        with open(p[cp.KW_FILE], "w") as f:
                            if not p[cp.KW_NOMETA] and self.model.zero_date:
                                metadata = {"zero_date":
                                    self.model.zero_date.isoformat()}
                                self.logger.info("Writing metadata {} to file "
                                    "'{}'..".format(metadata,p[cp.KW_FILE]))
                                jsonblock = json.dumps(
                                    metadata,indent=4,sort_keys=True)
                                commentblock = "\n".join(["# {}".format(l) \
                                    for l in jsonblock.split("\n")])
                                f.write(commentblock + "\n")
                            self.logger.info("Writing {} to file '{}'..."\
                                .format(list(d.keys()), p[cp.KW_FILE]))
                            write_csv(
                                f, d, headersortkey=lambda x: "" if x == "time" else x)
                            self.logger.info("Wrote {} to file '{}'!"\
                                .format(list(d.keys()), p[cp.KW_FILE]))
                # info
                elif action == cp.KW_CUT:
                    model_ivids = all_ivids()
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids)}
                    ivs = {ivid: find_iv(ivid)
                           for ivid in only if find_iv(ivid)}
                    start = p[cp.KW_SLICE][cp.KW_START]
                    end = p[cp.KW_SLICE][cp.KW_END]
                    for ivid, iv in ivs.items():
                        self.logger.info("Only keeping range [{}:{}] of '{}'"
                                         .format(start, end, ivid))
                        iv.cut(start, end)
                # info
                elif action == cp.KW_INFO:
                    iv = find_iv(p[cp.KW_ID])
                    print(repr(iv))
                # gui
                elif action == cp.KW_GUI:
                    self.model.gui(use_fallback=p[cp.KW_FALLBACK])
                # plot
                elif action == cp.KW_PLOT:
                    model_ivids = all_ivids()
                    only = p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids
                    ivs = [find_iv(ivid) for ivid in only if find_iv(ivid)]
                    filename = p[cp.KW_FILE]
                    if not filename:
                        filename = "{}_{}.pdf".format(
                        re.sub(pattern="\W",repl="_",string=self.model.name),
                        datetime.datetime.now().isoformat())
                    fig = plt.figure()
                    self.logger.info("Plotting {} with options {}..."\
                        .format(list([iv.id for iv in ivs]),p[cp.KW_JSON]))
                    given_plot_kwargs = p[cp.KW_JSON].copy()
                    plot_kwargs = {}
                    plot_kwargs.update(
                        {"convert_units":self.model.unit_conversions})
                    plot_kwargs.update(
                        {"zero_date":self.model.zero_date})
                    if given_plot_kwargs.pop("use_variable_time",None):
                        all_times = np.array([])
                        for v in self.model.variables.elements:
                            all_times = np.union1d(all_times, v.times)
                        given_plot_kwargs.update({"times":all_times})
                    plot_kwargs.update(given_plot_kwargs)
                    plot_interfacevalues(
                        figure = fig,
                        interfacevalues = ivs,
                        **plot_kwargs
                        )
                    self.logger.info("Saving plot of {} to file '{}'..."\
                        .format(list([iv.id for iv in ivs]),filename))
                    fig.savefig(filename)
                    self.logger.info("Saved plot of {} to file '{}'!"\
                        .format(list([iv.id for iv in ivs]),filename))
                # ipython
                elif action == cp.KW_IPYTHON:
                    m = self.model
                    model = self.model
                    IPython.embed(
                        header="Use variables 'm' or 'model' to access the model")
                # help
                elif action == cp.KW_HELP:
                    print("{}\n{}"
                          .format(self.CLI_HELP, cp.INSTRUCTIONS_HELP))
                # newobs
                elif action == cp.KW_NEWOBS:
                    iv = None
                    if p[cp.KW_FROM]:
                        self.logger.info("Copying '{}' to new observation "
                                         "'{}' with arguments {}".format(
                                        p[cp.KW_FROM], p[cp.KW_ID],
                                        p[cp.KW_JSON]))
                        old_iv = find_iv(p[cp.KW_FROM])
                        if old_iv:
                            copy_kwargs = {
                                "id":p[cp.KW_ID],
                                "name":"[observation] {}".format(old_iv.name),
                                }
                            copy_kwargs.update(p[cp.KW_JSON])
                            iv = old_iv.copy(**copy_kwargs)
                        else:
                            self.logger.warning("Could not find '{}' in "
                                "model. Skipping.".format(p[cp.KW_FROM]))
                    if not iv:
                        copy_kwargs = {
                            "id":p[cp.KW_ID],
                            "name":"observation",
                            }
                        copy_kwargs.update(p[cp.KW_JSON])
                        self.logger.info("Creating new empty observation "
                                         "'{}' with arguments {}".format(
                                         p[cp.KW_ID],p[cp.KW_JSON]))
                        iv = InterfaceValue(**copy_kwargs)
                    self.model.observations.add_element(iv)
                # zerodate
                elif action == cp.KW_ZERODATE:
                    self.model.zero_date = p[cp.KW_DATE]
                # noop
                elif action == cp.KW_NOOP:
                    pass
                # optimization
                elif action == cp.KW_OPTIMIZE:
                    variate = {}
                    for ivid, nblocks in p[cp.KW_VARIATE].items():
                        iv = find_iv(ivid)
                        if iv:
                            variate.update({iv: int(nblocks)})
                    bring_together = []
                    for group in p[cp.KW_BRING_TOGETHER]:
                        l = []
                        for ivid in group:
                            l.append(find_iv(ivid))
                        bring_together.append(l)
                    # optimize
                    self.model.optimize(
                        bring_together=bring_together,
                        variate=variate,
                        time_start=p[cp.KW_SLICE][cp.KW_START],
                        time_end=p[cp.KW_SLICE][cp.KW_END],
                    )
                # exit
                elif action == cp.KW_EXIT:
                    sys.exit(0)

    def read_instructions(self, f=sys.stdin):
        """
        Read instructions from file

        Args:
            f (filehandle, optional): the file handle to read from
        """
        instruction_parser = NumericalModelCliInstructionParser()
        while True:
            sys.stdout.write("{} ".format(self.prompt))
            sys.stdout.flush()
            try:
                line = next(f)
                if not f.isatty():
                    sys.stdout.write(line)
                    sys.stdout.flush()
                if line.strip():
                    try:
                        self.execute_instructions(
                            [instruction_parser(line.strip())])
                    except argparse.ArgumentTypeError as e:
                        print(str(e))
            except StopIteration:
                break
            except KeyboardInterrupt:
                break

    def run(self, instructions=None):  # pragma: no cover
        """
        Run the command-line interface

        Args:
            instructions (list, optional): The instructions to perform
        """
        logging.basicConfig(level=self.args_loglevel)
        for n, l in logging.Logger.manager.loggerDict.items():
            l.level = self.args_loglevel

        self.logger.info("Model:\n{}".format(self.model))

        if instructions is None:
            instructions = self.args.instructions

        # execute command-line instructions
        self.execute_instructions(instructions)

        # read input file commands if desired
        f = None
        if self.args.input is not None:
            if self.args.input == '-':
                f = sys.stdin
            else:
                f = open(self.args.input, "r")
        elif not instructions:  # without arguments, drop into shell
            f = sys.stdin
        if f:
            self.read_instructions(f)


class NumericalModelCliInstructionParser(object):
    """
    Parser for instructions
    """
    # Keywords
    KW_ASSIGNMENT = "assign"
    KW_INTEGRATE = "integrate"
    KW_FILEINPUT = "fileinput"
    KW_FILE = "file"
    KW_GUI = "gui"
    KW_TIME = "time"
    KW_VALUE = "value"
    KW_ID = "id"
    KW_FALLBACK = "fallback"
    KW_DUMP = "dump"
    KW_SECONDS = "seconds"
    KW_INFO = "info"
    KW_KEYWORD = "keyword"
    KW_CMD = "cmd"
    KW_HELP = "help"
    KW_IPYTHON = "ipython"
    KW_EXIT = "exit"
    KW_OPTIMIZE = "optimize"
    KW_BOOL = "bool"
    KW_ONLY = "only"
    KW_TRANSLATION = "translation"
    KW_VARIATE = "variate"
    KW_BRING_TOGETHER = "bring_together"
    KW_NOOP = "noop"
    KW_NEWOBS = "newobs"
    KW_REPLACE = "replace"
    KW_DATE = "date"
    KW_ZERODATE = "zerodate"
    KW_RESET = "reset"
    KW_FROM = "from"
    KW_CUT = "cut"
    KW_PLOT = "plot"
    KW_JSON = "json"
    KW_SLICE = "slice"
    KW_START = "start"
    KW_NOMETA = "nometa"
    KW_END = "end"
    # Regexes
    REGEXES = {
        KW_ASSIGNMENT: re.compile(
            r"^(?P<{id}>\S+?)(?:\[(?P<{time}>\d+(?:\.\d+)?)\])?"
            "=(?P<{value}>\d+(?:\.\d+)?)$"
            .format(time=KW_TIME, id=KW_ID, value=KW_VALUE),
            flags=re.IGNORECASE),
        KW_RESET: re.compile(
            r"^(?P<{keyword}>reset)"
            r"(:?:(?P<{seconds}>\d+(?:\.\d+)?))?"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{bool}>past(?:.also)?)\])?$"
            .format(keyword=KW_KEYWORD, bool=KW_BOOL,
                seconds=KW_SECONDS, only=KW_ONLY), flags=re.IGNORECASE),
        KW_INTEGRATE: re.compile(
            r"^(?P<{keyword}>int(?:egrate)?)"
            r"(:?:(?P<{seconds}>\d+(?:\.\d+)?))?$"
            .format(keyword=KW_KEYWORD, seconds=KW_SECONDS),
            flags=re.IGNORECASE),
        KW_INFO: re.compile(
            r"^(?P<{keyword}>info|show):(?P<{id}>\S+)$"
            .format(keyword=KW_KEYWORD, id=KW_ID),
            flags=re.IGNORECASE),
        KW_FILEINPUT: re.compile(
            r"^(?P<{keyword}>import|(?:file)?input|read(?:file)?):"
            r"(?P<{file}>[^[]+?)"
            r"(?:\[(?P<{replace}>replace)?\])?"
            r"(?:\[(?P<{nometa}>nometa)?\])?"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{trans}>\S+=\S+?(?:,\S+?=\S+?)*)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, trans=KW_TRANSLATION,
                    file=KW_FILE,nometa=KW_NOMETA,replace=KW_REPLACE),
            flags=re.IGNORECASE),
        KW_CUT: re.compile(
            r"^(?P<{keyword}>cut)"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{slice}>\S*?:\S*?)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, slice=KW_SLICE),
            flags=re.IGNORECASE),
        KW_DUMP: re.compile(
            r"^(?P<{keyword}>dump|(?:file)?output|write(?:file)?):"
            r"(?P<{file}>\S+?)"
            r"(?:\[(?P<{nometa}>nometa)?\])?"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{trans}>\S+=\S+?(?:,\S+?=\S+?)*)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, trans=KW_TRANSLATION,
                    file=KW_FILE,nometa=KW_NOMETA),
            flags=re.IGNORECASE),
        KW_ZERODATE: re.compile(
            r"^(?P<{keyword}>zerodate):(?P<{date}>.*)$"
            .format(keyword=KW_KEYWORD, date=KW_DATE),
            flags=re.IGNORECASE),
        KW_GUI: re.compile(
            r"^(?P<{keyword}>gui)(?:\[(?P<{fallback}>fallback)\])?$"
            .format(keyword=KW_KEYWORD, fallback=KW_FALLBACK),
            flags=re.IGNORECASE),
        KW_HELP: re.compile(
            r"^(?P<{keyword}>(?:h(?:elp)?|\?))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_NEWOBS: re.compile(
            r"^(?P<{keyword}>(?:new(?:obs(?:ervation)?)?)):(?P<{id}>\S+?)"
            r"(?:\[from:(?P<{fr}>\S+?)\])?"
            r"(?P<{json}>\{{.*\}})?"
            r"$"
            .format(keyword=KW_KEYWORD, id=KW_ID, fr=KW_FROM, json=KW_JSON),
            flags=re.IGNORECASE),
        KW_IPYTHON: re.compile(
            r"^(?P<{keyword}>(?:ipython|interactive|shell))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_PLOT: re.compile(
            r"^(?P<{keyword}>(?:plot|graph))"
            r"(?::(?P<{file}>\S+?))?"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?P<{json}>\{{.*\}})?"
            r"$".format(keyword=KW_KEYWORD, json=KW_JSON, file=KW_FILE,
                only=KW_ONLY),
            flags=re.IGNORECASE),
        KW_EXIT: re.compile(
            r"^(?P<{keyword}>(?:q(?:uit)?|exit))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_OPTIMIZE: re.compile(
            r"^(?P<{keyword}>\S+)/"
            r"(?P<{bring_together}>\S+?=\S+(?:,\S+?=\S+?)*)/"
            r"(?P<{variate}>\S+?:\S+?(?:,\S+?:\S+?)*)"
            r"(?:\[(?P<{slice}>\S+?:\S+?)\])?$"
            .format(keyword=KW_KEYWORD, variate=KW_VARIATE,
                    bring_together=KW_BRING_TOGETHER, slice=KW_SLICE),
            flags=re.IGNORECASE),
        KW_NOOP: re.compile(r"^((\s*)|((#*\s*)*)|(\s*(#+\s*)+.*))$"),
    }
    # Examples
    INSTRUCTIONS_HELP = textwrap.dedent("""
        Example Instructions:

        Open GUI:

            "gui"

        Open GUI in fallback mode:

            "gui[fallback]"

        Re-integrate the current variable time range

            "integrate"

        Integrate 60 seconds:

            "integrate:60"

        Set variable VARIABLE to value 64.1 at current time:

            "VARIABLE=64.1"

        Set variable VARIABLE to value 64.1 at time 42.5:

            "VARIABLE[42.5]=64.1"

        Read values from file DATA.csv:

            "input:DATA.csv" or
            "read:DATA.csv"

        Read only variables "T" and "f" from file DATA.csv:

            "read:DATA.csv[only:T,f]"

        Read variables "T" and "v" from file DATA.csv,
            but use them as "T_a" and "v_a" in the model:

            "read:DATA.csv[only:T,v][T=T_a,v=v_a]"

        Dump all data to file DATA.csv:

            "dump:DATA.csv"

        Dump variables "T" and "v" to file DATA.csv,
            but as "T_a" and "v_a" in the model:

            "dump:DATA.csv[only:T,v][T=T_a,v=v_a]"

        Create new observation "T_obs":

            "newobs:T_obs"

        Create new observation "T_obs" by copying "T_sim":

            "newobs:T_obs[from:T_sim]"

        Cut variable 'T_s' and only keep values between times 0 and 10:

            "cut[only:T_s][0:10]"

        Delete all values later than time 10:

            "cut[10:]"

        Reset the model to time 10:

            "reset:10"

        Reset only variable 'T_s' completely to time 10:

            "reset:10[only:T_s][past also]"

        Reset the model completely to time 10:

            "reset:10[past also]"

        Optimize parameter "a" to match "T_sim" and "T_obs" best:

            "optimize/T_sim=T_obs/a:1"

        Optimize forcing "v" with 10 values to match "T_sim" and "T_obs" best
            in time range 0 to 20:

            "optimize/T_sim=T_obs/v:10[0:20]"

        Open an interactive IPython session to manipulate the model:

            "ipython" or
            "shell"
        """)

    def __call__(self, arg):
        """
        Parse an instruction string

        Args:
            arg (str): the string to parse

        Returns:
            dict : the parsed instruction
        """
        try:
            for keyword, regex in self.REGEXES.items():
                m = regex.match(arg)
                if m:
                    d = m.groupdict()
                    # post-processing
                    for k, v in d.items():
                        if k in [self.KW_SECONDS, self.KW_VALUE, self.KW_TIME]:
                            if v is not None:
                                d[k] = float(v)
                        if k in [self.KW_FALLBACK, self.KW_BOOL,
                            self.KW_NOMETA, self.KW_REPLACE]:
                            d[k] = bool(v)
                        if k in [self.KW_TRANSLATION]:
                            d[k] = dict([p.split("=") for p in v.split(",")]) \
                                if v else {}
                        if k in [self.KW_BRING_TOGETHER]:
                            d[k] = [p.split("=") for p in v.split(",")] \
                                if v else []
                        if k in [self.KW_VARIATE]:
                            d[k] = dict([p.split(":") for p in v.split(",")]) \
                                if v else {}
                        if k in [self.KW_DATE]:
                            d[k] = np.datetime64(v).astype(object)
                        if k in [self.KW_JSON]:
                            if v is None:
                                j = {}
                            else:
                                try:
                                    j = json.loads(v)
                                except json.JSONDecodeError:
                                    raise ValueError("{} does not look like "
                                        "valid JSON".format(v))
                            assert hasattr(j,"items"), ("given JSON {} "
                                "could not be converted to dict".format(j))
                            d[k] = j
                        if k in [self.KW_ONLY]:
                            d[k] = v.split(",") if v else []
                        if k in [self.KW_SLICE]:
                            s = {self.KW_START: None, self.KW_END: None}
                            if v:
                                for l, m in zip((self.KW_START, self.KW_END),
                                                v.split(":")):
                                    try:
                                        s[l] = float(m)
                                    except ValueError:
                                        s[l] = None
                            d[k] = s

                    d.update({self.KW_CMD: arg})
                    return {keyword: d}
                else:
                    continue
            # if we reach this point, this instruction is unknown
            assert False, "unknown instruction '{}'".format(arg)
        except (ValueError, AttributeError, AssertionError) as e:
            msg = "'{}' is no instruction: {}\n\n{}".format(
                arg, e, self.INSTRUCTIONS_HELP)
            raise argparse.ArgumentTypeError(msg)
