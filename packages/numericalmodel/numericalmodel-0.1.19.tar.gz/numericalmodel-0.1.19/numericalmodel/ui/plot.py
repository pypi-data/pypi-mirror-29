#!/usr/bin/env python3
# system modules
from collections import deque
import re
import logging
import hashlib
import datetime
import sys

# internal modules
from numericalmodel import utils
from numericalmodel.utils import multi_func
from numericalmodel.interfaces import InterfaceValue
from numericalmodel.ui.utils import lim_from_iv

# external modules
import numpy as np
from scipy.stats.stats import pearsonr
import statsmodels.api as sm

from matplotlib.dates import *


interval2locator = {
    "microsecond":SecondLocator,
    "second":SecondLocator,
    "minute":MinuteLocator,
    "hour":HourLocator,
    "day":DayLocator,
    "week":WeekdayLocator,
    "month":MonthLocator,
    "year":YearLocator,
    }

def plot_interfacevalues(
        interfacevalues,
        figure,
        times=None,
        only_available_times=None,
        scatter=False,
        consistent_colors=False,
        equal_axes=False,
        identity_line=False,
        split_units=True,
        linear_fit=False,
        robust_linear_fit=False,
        hist2d=False,
        plot_method="none",
        zero_date=None,
        time_as_date=False,
        date_ticks_every=None,
        autofmt_xdate=True,
        date_format=None,
        show_colorbar=True,
        reverse=False,
        hist2d_bins=20,
        hist2d_normed=True,
        hist2d_mask_empty=True,
        fit_intercept=True,
        ids_as_tex=True,
        bounds_lim=False,
        roll=0,
        convert_units={},
        model_time=None,
        show_stats=False,
        show_title_stats=True,
        show_legend_stats=True,
        show_yaxis_stats=True,
        show_xaxis_stats=True,
        show_model_time=True,
        **kwargs):
    """
    Plot one or more :any:`InterfaceValue` instances onto a given Figure

    Args:
        interfacevalues (list): the :any:`InterfaceValue` s to plot
        figure (matplotlib.figure.Figure): the
            :any:`matplotlib.figure.Figure` to plot onto
        times (numpy.ndarray, optional): Times to plot. If left unspecified,
            plot the times that are available.
        only_available_times (bool, optional): When plotting quantities against
            each other, use only the available times? Otherwise values will be
            interpolated. Defaults to ``False`` which means to interpolate.
        scatter (bool, optional): Use scatterplots where possible? Defaults
            to ``False``.
        zero_date (datetime-like, optional): The date to interpret the times
            from. Has to be something that :any:`numpy.datetime64` can parse.
            Defaults to the current time.
        time_as_date (bool, optional): Show the date according to ``zero_date``
            instead of seconds.
        reverse (bool, optional): Reverse the order of quantities?
        autofmt_xdate (bool, optional): Run
            :any:`matplotlib.figure.Figure.autofmt_xdate`? Defaults to
            ``True``.
        date_format (str, optional): The date format to use. If left
            unspecified, an automatic format is used.
        date_ticks_every (str, optional): Draw ticks every
            {"microsecond","second","minute","hour","day","month","year"}. If
            left unspecified, an automatic value is used.
        hist2d (bool, optional): Use 2-dimenstional histogram instead of plain
            scatter plots? Defaults to ``False``.
        hist2d_bins (int, optional): How man bins to use for hist2d plot.
            Defaults to ``20``.
        hist2d_normed (bool, optional): Normalize the hist2d plot?
            Defaults to ``True``.
        hist2d_mask_empty (bool, optional): Mask empty bins in hist2d plot?
            Defaults to ``True``.
        plot_method (str, optional): The plot type. One of ``"none"``
            (default), ``"difference"``, ``"sum"``, ``"product"``,
            ``"quotient"`` or ``"mean"``.
        show_colorbar (bool, optional): Show a colorbar in the hist2d plot?
            Defaults to ``True``.
        consistent_colors (bool, optional): Use consistent colors for all
            plots, i.e. determine the color from the :any:`InterfaceValue`
            's metadata? Defaults to ``False``.
        identity_line (bool, optional): If ``scatter`` is ``True``, draw an
            identity line? Defaults to ``False``.
        equal_axes (bool, optional): If ``scatter`` is ``True``, use an
            aspect ratio of ``1:1`` for the x/y-axis? Defaults to ``False``.
        split_units (bool, optional): Put values of matching units into
            separate plots? Defaults to ``True``.
        ids_as_tex (bool, optional): Render the :any:`InterfaceValue.id` as
            math. Defaults to ``True``.
        linear_fit (bool, optional): If ``scatter=True``, display a linear
            fit? Defaults to ``False``.
        robust_linear_fit (bool, optional): If ``linear_fit=True``, do a robust
            linear fit.
        fit_intercept (bool, optional): If ``linear_fit=True``, fit an
            intercept? Defaults to ``True``.
        bounds_lim (bool, optional): If ``True``, base the axis limits
            on :any:`InterfaceValue.bounds`
        show_stats, show_xaxis_stats, show_yaxis_stats, show_title_stats,
            show_legend_stats (bool, optional): If ``True``, show common
            statistical values.
        roll (int, optional): Roll list of :any:`InterfaceValue` s by this
            number to manipulate the order of plotted content
        convert_units (dict(str), optional): Convert :any:`InterfaceValue` s
            according to this converting dict. See also
            :any:`InterfaceValue.unit_converters`.
    """
    # somehow matplotlib breaks if converting datetimes for scatter plots...
    # (see https://github.com/matplotlib/matplotlib/issues/9211)
    if scatter:
        time_as_date_original = time_as_date
        time_as_date = False

    def convert_if_wanted(iv):
        try:
            to_unit = convert_units[iv.unit]
            logging.debug("Converting {} to {}...".format(iv.id,to_unit))
            return iv.convert(to_unit)
        except KeyError:
            return iv
        except ValueError as e:
            logging.warning("Could not convert '{}' to '{}': {}"\
                .format(iv.id,to_unit,e))

    logging.debug("Given list of InterfaceValues: {}".format(
        [iv.id for iv in interfacevalues]))
    interfacevalues = [convert_if_wanted(iv) for iv in interfacevalues]
    logging.debug("Given list of InterfaceValues converted: {}".format(
        [iv.id for iv in interfacevalues]))

    units = {}
    if split_units:
        for interfacevalue in interfacevalues:
            try:
                units[interfacevalue.unit].append(interfacevalue)
            except KeyError:
                units[interfacevalue.unit] = [interfacevalue]
    else:
        units = {"] [".join(set([iv.unit for iv in interfacevalues])):
                 interfacevalues}

    def display_id(s,math_env=True):
        return ("${}$" if math_env else "{}").format(str2tex(s)) \
            if ids_as_tex else s
    def axes_stats(iv,times,group=False):
        iv_val = iv(times)
        return (r"{mean_varid}$={mean:.3f}$"
            r", {std_varid}$={std:.3f}$").format(
            mean_varid=r"$\overline{{{}}}$".format(display_id(iv.id,False)) \
            if ids_as_tex else r"mean {}".format(iv.id),
            std_varid=r"${{{}}}_{{\mathrm{{(std)}}}}$".format(
                ("({})" if group else "{}").format(display_id(iv.id,False)) \
                    if ids_as_tex else r"{} std".format(iv.id)),
            mean=np.mean(iv_val), std=np.std(iv_val))
    def scatter_stats(iv1,iv2,times):
        iv1_val = iv1(times)
        iv2_val = iv2(times)
        corr = pearsonr(iv1_val,iv2_val)[0] if times.size>1 else np.nan
        corr_text = "{:.3f}".format(corr) if np.isfinite(corr) else "?"
        return (r"${{\mathrm{{RMSE}}}}={rmse:.3f}$"
            r", ${{R_{{\mathrm{{corr}}}}}}={corr}$"
            ).format(rmse=utils.rmse(iv1_val,iv2_val),corr=corr_text)

    zero_date = np.datetime64(zero_date) if zero_date \
        else np.datetime64(datetime.datetime.now())
    def seconds2datetime(seconds):
        return zero_date + np.array(seconds).astype("timedelta64[s]")

    interp2drawstyle = {}
    if times is None:
        interp2drawstyle = {'linear': 'default', 'nearest': 'steps-mid',
                            'zero': 'steps-post', }


    hist2d_kwargs = {"bins":hist2d_bins,"normed":hist2d_normed}
    if hist2d_mask_empty:
        hist2d_kwargs.update({"cmin":sys.float_info.min})

    i = 1
    axes = {}
    model_time_shown = False
    for unit, ivlist in sorted(units.items()):
        ivlist = deque(ivlist)
        if reverse:
            ivlist.reverse()
        ivlist.rotate(roll)
        logging.debug("Sorted InterfaceValues of unit '{}': {}".format(unit,
            [iv.id for iv in ivlist]))
        try:
            axes[unit]
        except KeyError:
            if scatter:
                axes[unit] = figure.add_subplot(len(units), 1,
                                                len(units) - i + 1)
            else:
                try:
                    axes[unit] = figure.add_subplot(
                        len(units), 1, len(units) - i + 1, sharex=xaxis_shared)
                except NameError:
                    axes[unit] = figure.add_subplot(len(units), 1,
                                                    len(units) - i + 1)
                    xaxis_shared = axes[unit]
        ax = axes[unit]
        plot_kwargs_all = {"zorder": 5}
        if times is None:
            all_times = np.array([])
            for v in ivlist:
                all_times = np.union1d(all_times, v.times)
        else:
            all_times = times
        plot_method_functions = {
            "mean":       lambda l:multi_func(*l,f=lambda x,y: x+y,norm=True),
            "difference": lambda l:multi_func(*l,f=lambda x,y: x-y),
            "quotient":   lambda l:multi_func(*l,f=lambda x,y: x/y),
            "product":    lambda l:multi_func(*l,f=lambda x,y: x*y),
            "sum":        lambda l:multi_func(*l,f=lambda x,y: x+y),
            }
        plot_method_exprs = {
            "mean":       lambda l:
                "( {} ) / {}".format(" + ".join(l),len(l)),
            "difference": lambda l:" - ".join(l),
            "quotient":   lambda l:" / ".join(l),
            "product":    lambda l:" * ".join(l),
            "sum":        lambda l:" + ".join(l),
            }
        plot_method_func = plot_method_functions.get(plot_method)
        plot_method_expr = plot_method_exprs.get(plot_method,
            "{}({})".format(plot_method, lambda l:" , ".join(l)))
        apply_plot_method = hasattr(plot_method_func, "__call__") \
            and len(ivlist)>(1+int(scatter))
        if apply_plot_method:
            merge_ivs = list(ivlist)[1:] if scatter else ivlist
            merged_values = \
                plot_method_func([iv(all_times) for iv in merge_ivs])
            assert all_times.size == merged_values.size
            merged_iv = InterfaceValue(
                id = "{formula}".format(method=plot_method,
                    formula=plot_method_expr(list(iv.id for iv in merge_ivs))),
                name = "{} of {}".format(plot_method," and ".join(
                    display_id(iv.id) for iv in merge_ivs)),
                times = all_times,
                values = merged_values,
                unit = "] [".join(set(iv.unit for iv in merge_ivs)),
                )
            ivlist = [ivlist[0], merged_iv] if scatter else [merged_iv]
        if scatter:
            if len(ivlist) == 1:
                # 1-1 scatterplot
                plot_kwargs = plot_kwargs_all.copy()
                iv = ivlist[0]
                plot_kwargs.update(
                    {"label": "{} ({}) {} {}".format( iv.name,
                        display_id(iv.id), _("vs."), _("itself"))})
                if consistent_colors:
                    plot_kwargs.update(
                        {"color": string2color(iv.name + iv.id)})
                if times is None:
                    times = iv.times
                if hist2d:
                    count,xedges,yedges,image = \
                        ax.hist2d(
                            iv(times).reshape(-1),
                            iv(times).reshape(-1),
                            **hist2d_kwargs)
                    if show_colorbar:
                        cb = figure.colorbar(mappable = image, ax = ax)
                        cb.set_label(
                            _("density") if hist2d_normed else _("count"))
                else:
                    ax.scatter(iv(times), iv(times), **plot_kwargs)
                xlabel = "{} [{}]".format(display_id(iv.id), iv.unit)
                ylabel = "{} [{}]".format(display_id(iv.id), iv.unit)
                if show_stats:
                    if show_xaxis_stats:
                        xlabel = "{}, {}".format(xlabel,axes_stats(iv,times))
                    if show_yaxis_stats:
                        ylabel = xlabel
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                if bounds_lim:
                    lower, upper = lim_from_iv(iv)
                    ax.set_ylim(lower, upper)
                    ax.set_xlim(lower, upper)
            else: # multiscatter plot
                multiscatter_units = []
                if bounds_lim:
                    # determine lower/upper bounds
                    lowlim, uplim = 0, 0
                    for iv in ivlist:
                        l, u = lim_from_iv(iv)
                        try:
                            main_iv
                        except NameError:
                            main_iv = iv
                            mainlowlim, mainuplim = l, u
                            continue
                        lowlim, uplim = min(lowlim, l), max(uplim, u)
                    del main_iv
                else:
                    if hist2d:
                        ivlist = list(ivlist)[:2]
                for iv in ivlist:
                    plot_kwargs = plot_kwargs_all.copy()
                    if consistent_colors:
                        plot_kwargs.update(
                            {"color": string2color(iv.name + iv.id)})
                    # stacked scatterplot
                    try:
                        main_iv
                        times = np.intersect1d(
                            main_iv.times if all_times is None else all_times,
                            iv.times) \
                                if only_available_times else all_times
                        multiscatter_units.append(iv.unit)
                        label = "{} ({}) {} {} ({})".format(
                            iv.name, display_id(iv.id), _("vs."),
                            main_iv.name, display_id(main_iv.id))
                        if show_stats:
                            if show_legend_stats:
                                label = "{}, {}".format(label,
                                    scatter_stats(main_iv,iv,times))
                        plot_kwargs.update({"label": label})
                        if hist2d:
                            logging.info("Doing hist2d plot...")
                            count,xedges,yedges,image = \
                                ax.hist2d(
                                    main_iv(times).reshape(-1),
                                    iv(times).reshape(-1),
                                    **hist2d_kwargs)
                            logging.info("hist2d plot done!")
                            if show_colorbar:
                                cb = figure.colorbar(mappable = image, ax = ax)
                                cb.set_label(_("density") \
                                    if hist2d_normed else _("count"))
                            title = ""
                            title += "{} - {}".format(
                                seconds2datetime(times.min())\
                                    .astype(object).isoformat(),
                                seconds2datetime(times.max())
                                    .astype(object).isoformat(),
                                ) if time_as_date_original \
                                else "{} {} {}".format(
                                times.max()-times.min(),
                                _("seconds"),_("total"))
                            if show_stats:
                                if show_title_stats:
                                    title += ", {} bins per axis, {}"\
                                        .format( hist2d_bins,
                                        scatter_stats(main_iv,iv,times))
                            ax.set_title(title)
                        else:
                            ax.scatter(
                                main_iv(times), iv(times), **plot_kwargs)
                        if bounds_lim:
                            ax.set_ylim(lowlim, uplim)
                        # linear fit
                        if linear_fit:
                            x_in, y_in = main_iv(times), iv(times)
                            if fit_intercept:
                                x_in = sm.add_constant( x_in )
                            if robust_linear_fit:
                                logging.info("Robust linear regression of {} "
                                    "data points...".format(y_in.size))
                                reg = sm.RLM(y_in, x_in).fit()
                                R2 = sm.WLS(y_in, x_in,
                                    weights=reg.weights).fit().rsquared
                                logging.info("Robust linear regression done!")
                            else:
                                reg = sm.OLS(y_in, x_in).fit()
                                R2 = reg.rsquared
                            b,a = reg.params if fit_intercept \
                                else (0,reg.params)
                            plot_kwargs.update(
                                {
                                    "label": r"{dep_var} = {gain:.4f} "
                                    "$\\cdot$ {indep_var} {offset}{stats}"\
                                        .format(
                                        dep_var=display_id(iv.id),
                                        gain=float(a),
                                        indep_var=display_id(main_iv.id),
                                        offset=r"${}{:.4f}$".format(
                                            "+ " if b > 0 else "",
                                            float(b)) if fit_intercept \
                                            else "",
                                        stats=r" ({type}), {weighted}"
                                            r"$R^2={{{R2:.3f}}}$"\
                                            .format(type=_("robust") if
                                            robust_linear_fit \
                                                else
                                                "ordinary",R2=R2,
                                                weighted="weighted " \
                                                if robust_linear_fit else "") \
                                            if (show_stats and \
                                                show_legend_stats) else ""),
                                    "zorder": plot_kwargs["zorder"] + 1,
                                })
                            low, high = ax.get_xlim()
                            x = np.linspace(low, high, 1000)
                            y = a * x + b
                            ax.plot(x, y, **plot_kwargs)
                    except NameError:
                        main_iv = iv
                        if bounds_lim:
                            ax.set_xlim(mainlowlim, mainuplim)
                    xlabel = main_iv.name if hist2d else ""
                    ylabel = iv.name if hist2d else ""
                    xlabel = "{} {} [{}]".format(xlabel,
                            display_id(main_iv.id), main_iv.unit)
                    ylabel = ylabel + " " + \
                        (display_id(iv.id) if not apply_plot_method \
                            else "({})".format(display_id(iv.id)) \
                            +" " if len(ivlist)==2 else "") +\
                        " "+"["+"] [".join(set(multiscatter_units)) + "]"
                    if show_stats:
                        if show_xaxis_stats:
                            xlabel="{}, {}".format(
                                xlabel,axes_stats(main_iv,times))
                        if len(set(multiscatter_units)) == 1 \
                            and len(ivlist) == 2:
                            if show_yaxis_stats:
                                ylabel = "{}, {}".format(
                                    ylabel,axes_stats(iv,times,
                                        group=apply_plot_method))
                    ax.set_xlabel(xlabel)
                    ax.set_ylabel(ylabel)
            if equal_axes:
                ax.set_aspect("equal", "datalim")
            if identity_line:
                xl, xu = ax.get_xlim()
                yl, yu = ax.get_ylim()
                plot_kwargs = plot_kwargs_all.copy()
                plot_kwargs.update({"zorder": 10, "c": "k", "linestyle": "--",
                                    "label": _("identity")})
                low, high = min(xl, yl), max(xu, yu)
                ax.plot([low, high], [low, high], **plot_kwargs)
        else:  # no scatter plot
            if times is None:
                all_times = np.array([])
                for v in ivlist:
                    all_times = np.union1d(all_times, v.times)
            else:
                all_times = times
            if bounds_lim:
                # determine lower/upper bounds
                lowlim, uplim = 0, 0
                for iv in ivlist:
                    l, u = lim_from_iv(iv)
                    lowlim, uplim = min(lowlim, l), max(uplim, u)
            if show_model_time and model_time is not None \
                    and times is None:
                axvline_kwargs = {"linestyle": "--", "color": "r"}
                if not model_time_shown:
                    axvline_kwargs.update(
                        {"label": _("model time ({:.2f})").format(model_time)})
                    model_time_shown = True
                ax.axvline(x=model_time, **axvline_kwargs)
            for iv in ivlist:
                times = iv.times if only_available_times else all_times
                plot_kwargs = plot_kwargs_all.copy()
                if times is None:
                    x = iv.times
                    y = iv.values
                else:
                    x = times
                    y = iv(times)

                if time_as_date:
                    x = seconds2datetime(x).astype(object)

                plot_kwargs.update({"label":
                    "{} ({})".format(iv.name, display_id(iv.id))})
                if consistent_colors:
                    plot_kwargs.update(
                        {"color": string2color(iv.name + iv.id)})
                if np.array(x).size > 1:
                    plot_kwargs.update({"drawstyle": interp2drawstyle.get(
                        iv.interpolation, "default"), })
                    ax.plot(x, y, **plot_kwargs)
                else:
                    ax.scatter(x, y, **plot_kwargs)
                if bounds_lim:
                    ax.set_ylim(lowlim, uplim)
            ax.set_ylabel("[{}]".format(unit))
        if time_as_date:
            locator = interval2locator.get(
                date_ticks_every,AutoDateLocator)()
            ax.xaxis.set_major_locator(locator)
            formatter = DateFormatter(date_format) if date_format \
                else AutoDateFormatter(locator)
            ax.xaxis.set_major_formatter(formatter)
            if autofmt_xdate:
                figure.autofmt_xdate()
        ax.tick_params(direction="in")
        ax.grid(zorder=0)
        ax.legend()
        i += 1

    for unit, ax in axes.items():
        try:
            if ax == xaxis_shared:
                xlabel = _("time")
                if not time_as_date:
                    xlabel += " [{}]".format(_("seconds"))
                ax.set_xlabel(xlabel)
            else:
                ax.tick_params(bottom=True, left=True, top=True,
                               right=True, labelbottom=False,)
        except NameError as e:
            ax.tick_params(bottom=True, left=True, top=True,
                           right=True, labelbottom=True,)


def str2tex(s):
    """
    Make sure a given string can be displayed in tex (e.g. for matplotlib)

    Args:
        s (str): the string to convert

    Returns:
        str : the string modified to be displayable in tex
    """
    for i in range(0,10):
        s1=re.sub(pattern=r"([^_]+)_(?!\{)(\S+)(?!\})",repl=r"\1_{\2}",string=s)
        if s1==s: break
        s=s1
    return s

def string2color(string):
    """
    Convert a string to a hex HTML color string

    Args:
        string (str): the string to use

    Returns:
        string : an HTML color string (e.g. #34df12)
    """
    return "#" + hashlib.md5(string.encode("utf-8")).hexdigest()[:6]
