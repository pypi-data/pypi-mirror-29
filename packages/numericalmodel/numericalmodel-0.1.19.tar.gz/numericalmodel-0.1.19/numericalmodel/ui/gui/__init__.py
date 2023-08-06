#!/usr/bin/env python3
# system modules
import os
import sys
import time
import re
import tempfile
import logging
import signal
import gettext
import locale
import textwrap
import webbrowser
from pkg_resources import resource_filename

# internal modules
from numericalmodel import utils
from numericalmodel.ui.plot import plot_interfacevalues
from numericalmodel.ui.utils import lim_from_iv, GETTEXT_DOMAIN, LOCALEDIR
from numericalmodel.numericalmodel import NumericalModel
from numericalmodel import __version__

# external modules
import numpy as np

logger = logging.getLogger(__name__)

# set up localization
locale.setlocale(locale.LC_ALL, '')
for mod in [locale, gettext]:
    mod.bindtextdomain(GETTEXT_DOMAIN, LOCALEDIR)
gettext.textdomain(GETTEXT_DOMAIN)
gettext.install(GETTEXT_DOMAIN, localedir=LOCALEDIR)

instructions = textwrap.dedent("""
To install the prerequisites, use your system's package manager and install
at least ``python3-gi`` (might also be called ``pygobject3``). You might also
need ``libffi``.

On Debian/Ubuntu:

.. code:: sh

    sudo apt-get install python3-gi libcffi6 libffi-dev

.. note::

    If you are using `Anaconda <https://conda.io/docs/index.html>`_ you will
    want to install the following packages:

    .. code-block:: sh

        conda install -c conda-forge -c pkgw-forge pygobject
        conda install -c conda-forge -c pkgw-forge gtk3

    If you don't have system privileges to install ``python3-gi`` , there
    is also the (experimental) :mod:`pgi` module on `PyPi
    <https://pypi.python.org/pypi/pgi/>`_ that you can install via::

        pip3 install --user pgi

    Theoretically, the :any:`NumericalModelGui` might work with this package as
    well, but no guarantees...


Then, install :mod:`numericalmodel` with the ``gui`` feature:

.. code:: sh

    pip3 install --user 'numericalmodel[gui]'

""")

__doc__ = \
    """
Graphical user interface for a NumericalModel. This module is only useful
if the system package ``python3-gi`` is installed to provide the :mod:`gi`
module.

""" + instructions

PGI = False
GTK_INSTALLED = False
try:  # try real gi module
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
    GTK_INSTALLED = True  # importing real gi worked
except Exception as e:  # importing real gi didn't work
    logger.info("no 'gi' module found: {}".format(e))
    try:  # try pgi package
        import pgi
        pgi.install_as_gi()
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
        PGI = True
        GTK_INSTALLED = True  # importing pgi worked
        logger.warning("using 'pgi' module instead of 'gi'")
    except BaseException:
        logger.error("Neither 'pgi' nor 'gi' module found!"
                     "The GUI will not work.")


class FigureCanvasFile(Gtk.EventBox):
    """
    Class to mimic a
    :class:`matplotlib.backends.backend_gtk3agg.FigureCanvasGTK3Agg` as a
    fallback solution with a primitive file-based approach.

    Args:
        figure (matplotlib.figure.Figure): the figure to show
        args,kwargs : further arguments passed to the :class:`Gtk.EventBox`
            constructor
    """

    def __init__(self, figure, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figure = figure
        self.scrolledwindow.add(self.image)
        self.add(self.scrolledwindow)

    @property
    def scrolledwindow(self):
        """
        The underlying :class:`Gtk.ScrolledSindow`

        :type: :class:`Gtk.ScrolledSindow`
        """
        try:
            self._scrolledwindow
        except AttributeError:
            self._scrolledwindow = Gtk.ScrolledWindow()
        return self._scrolledwindow

    @property
    def image(self):
        """
        The underlying :class:`Gtk.Image`

        :type: :class:`Gtk.Image`
        """
        try:
            self._image
        except AttributeError:
            self._image = Gtk.Image()
        return self._image

    @property
    def figure(self):
        """
        The underlying figure

        :type: :class:`matplotlib.figure.Figure`
        :setter: sets the figure and calls :meth:`load`
        """
        try:
            self._figure
        except AttributeError:
            self._figure = Figure()
        return self._figure

    @figure.setter
    def figure(self, newfigure):
        assert isinstance(newfigure, Figure)
        if newfigure.canvas is None:
            newfigure.canvas = FigureCanvasAgg(newfigure)
        self._figure = newfigure

    @property
    def imagefile(self):
        """
        The path to the underlying image

        :type: :any:`str`
        :getter: Creates new temporary hidden file in the current folder if none
            was specified yet
        :setter: Sets the new path, removing the old file if necessary
        """
        try:
            self._imagefile
        except AttributeError:
            n, path = tempfile.mkstemp(
                dir=os.path.curdir, suffix=".png", prefix=".")
            logger.debug("Created new temporary file '{}'".format(path))
            self._imagefile = path
        return self._imagefile

    @imagefile.setter
    def imagefile(self, newimagefile):
        try:
            self._imagefile
            logger.debug("Removing old image '{}'".format(self._imagefile))
            os.remove(self._imagefile)
        except AttributeError:
            pass
        self._imagefile = str(newimagefile)

    ###############
    ### Methods ###
    ###############
    def save(self, width, height):
        """
        Save the current figure to :any:`imagefile`

        Args:
            width, height (int): width and height in pixels
        """
        DPI = self.figure.get_dpi()
        self.figure.set_size_inches(width / DPI, height / DPI)
        self.figure.savefig(self.imagefile)

    def load(self):
        """
        (Re)load the underlying :any:`imagefile`
        """
        logger.debug("Reading image '{}'".format(self.imagefile))
        self.image.set_from_file(self.imagefile)

    def display(self, width, height):
        """
        Get the content of the current figure displayed by calling :meth:`save`
        and :any:`load`.

        Args:
            width, height (int): width and height in pixels
        """
        self.save(width=width, height=height)
        self.load()

    def remove_imagefile(self):
        """
        Remove the :any:`imagefile`
        """
        try:
            self._imagefile
            logger.debug("Removing temporary image '{}'".format(
                self._imagefile))
            os.remove(self.imagefile)
        except AttributeError:
            pass

    #######################
    ### Special Methods ###
    #######################
    def __del__(self):
        """
        Class destructor. Deletes the :any:`imagefile`.
        """
        self.remove_imagefile()


from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
try:
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg \
        as FigureCanvas
except BaseException:
    FigureCanvas = FigureCanvasFile
    logger.error("matplotlib seems to not have a working Gtk3 backend. "
                 "Falling back to file-based backend.")


MODEL_CONTENT = ["variables", "forcing", "parameters", "observations"]


class NumericalModelGui(object):
    """
    class for a GTK gui to run a :any:`NumericalModel` interactively

    Args:
        numericalmodel (NumericalModel): the NumericalModel to run
        custom_plots (dict, optional): custom plots. This is a :any:`dict` like
            ``custom_plots[name]=function(model,figure,**gui_plot_options)``.
            The ``gui_plot_options`` will be set to :any:`plot_settings`. The
            function should just take the figure (a
            :any:`matplotlib.figure.Figure`) and add plots to it as if it was
            newly created. The data can be taken from the ``model`` argument,
            which will be set to :any:`NumericalModelGui.model`.
        use_fallback (bool, optional): use the file-based
            :class:`FigureCanvasFile` as file-based backend? This may help if
            there are problems with the GTK/matplotlib-interaction. Defaults
            to ``False`` .
    """

    def __init__(self, numericalmodel, custom_plots=None,
                 use_fallback=False):
        if not GTK_INSTALLED:
            raise Exception(
                "Gtk3.0 bindings seem not installed.\n" + instructions)

        self.setup_signals(
            signals=[signal.SIGINT, signal.SIGTERM, signal.SIGHUP],
            handler=self.quit
        )

        self.dragtargets = Gtk.TargetList.new([])
        self.dragtargets.add_text_targets(80)

        self.use_fallback = use_fallback

        self.model = numericalmodel
        if custom_plots is not None:
            self.custom_plots = custom_plots

    ##################
    ### Properties ###
    ##################
    @property
    def model(self):
        """
        The :any:`NumericalModel` behind the gui

        :type: :any:`NumericalModel`
        """
        try:
            return self._model
        except AttributeError:
            self._model = NumericalModel()
        return self._model

    @model.setter
    def model(self, newmodel):
        assert all([hasattr(newmodel, a) for a in ["integrate",
                                                   "variables", "forcing", "parameters", "observations"]])
        self._model = newmodel

    @property
    def builder(self):
        """
        The gui's :code:`GtkBuilder`. This is a read-only property.

        :getter: Return the :class:`GtkBuilder`, load the :any:`gladefile` if
            necessary.
        :type: :class:`GtkBuilder`
        """
        try:
            self._builder
        except AttributeError:
            builder = Gtk.Builder()  # new builder
            # set translation domain
            builder.set_translation_domain(GETTEXT_DOMAIN)
            # load the gladefile
            builder.add_from_file(self.gladefile)
            # set internal attribute
            self._builder = builder
        return self._builder

    @property
    def gladefile(self):
        """
        The gui's Glade file. This is a read-only property.

        :type: :any:`str`
        """
        return resource_filename(__name__, "gui.glade")

    @property
    def figures(self):
        """
        The gui's :any:`matplotlib.figure.Figure` for plotting

        :type: :any:`dict` of :any:`matplotlib.figure.Figure`
        :getter: returns the gui's :any:`matplotlib.figure.Figure`, create one
            if necessary
        """
        try:
            self._figures
        except AttributeError:
            self._figures = {n: Figure(tight_layout=True)
                             for n in MODEL_CONTENT}
            self._figures.update({n: Figure(tight_layout=True)
                                  for n in self.custom_plots.keys()})
        return self._figures

    @property
    def figures_content(self):
        """
        The :any:`figures` ' content as abstract dict

        :type: :any:`dict` of :any:`str`
        :getter: returns the :any:`figures` ' current content template, create
            new template if none was set yet
        :setter: sets the :any:`figures` ' content template and reloads the
            current plot. Resets the content template if set to ``None``.
        """
        try:
            self._figures_content
        except AttributeError:
            # default figure content
            self._figures_content = {}
            for tab in MODEL_CONTENT:
                self._figures_content[tab] = {}
                self._figures_content[tab][tab] = \
                    {k: v for k, v in sorted(getattr(self.model, tab).items())}
        return self._figures_content

    @figures_content.setter
    def figures_content(self, newcontent):
        if newcontent is None:
            del self._figures_content
        else:
            assert hasattr(newcontent, "items")
            self._figures_content = newcontent
        # changing the figures' content means replotting
        self.update_current_plot()

    @property
    def custom_plots(self):
        """
        Custom plots

        :type: :any:`dict`
        """
        try:
            self._custom_plots
        except AttributeError:
            self._custom_plots = {}
        return self._custom_plots

    @custom_plots.setter
    def custom_plots(self, newcustom_plots):
        assert hasattr(newcustom_plots, "items"), \
            "custom_plots have to be dict"
        self._custom_plots = newcustom_plots

    @property
    def logo_pixbuf(self):
        """
        The logo as :class:`GdkPixbuf.Pixbuf`

        :type: :class:`GdkPixbuf.Pixbuf`
        """
        try:
            self._logo_pixbuf
        except AttributeError:
            logo_path = resource_filename(__name__, "media/logo.png")
            logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo_path)
            self._logo_pixbuf = logo_pixbuf
        return self._logo_pixbuf

    @property
    def scales(self):
        """
        The :class:`GtkScale` used to manipulate model data

        :type: :any:`dict` of :class:`GtkScale`
        :getter: return the gui's :class:`GtkScale` s, create new if necessary
        """
        try:
            self._scales
        except AttributeError:
            self._scales = {}
            for attr in MODEL_CONTENT:
                self._scales[attr] = {}
                grid = Gtk.Grid()
                grid.props.hexpand = True
                grid.props.column_spacing = 10
                grid.props.row_spacing = 5
                i = 0
                for ivid, iv in sorted(getattr(self.model, attr).items()):
                    self._scales[attr][ivid] = {}
                    self._scales[attr][ivid]["initial"] = \
                        iv[self.model.model_time]
                    lower, upper = iv.bounds
                    adj = self.adjustment_from_iv(iv)
                    scale = Gtk.Scale(
                        orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
                    scale.props.draw_value = False
                    scale.set_size_request(width=100, height=-1)
                    digits = num_decimals(
                        scale.get_adjustment().get_step_increment())
                    scale.props.digits = digits
                    scale.props.hexpand = True
                    scale.add_mark(self._scales[attr][ivid]["initial"],
                                   Gtk.PositionType.TOP, None)
                    spinbutton = Gtk.SpinButton.new(
                        scale.get_adjustment(),
                        climb_rate=scale.get_adjustment().get_step_increment(),
                        digits=scale.props.digits
                    )
                    spinbutton.set_tooltip_markup(
                        _("The value used in "
                          "the model might have a higher accuracy.") +
                        "\n" +
                        _("The initial value when the GUI was launched "
                          "was <b>{}</b>.").format(
                            float(self._scales[attr][ivid]["initial"])) +
                        "\n" +
                        _("Drag'n'Drop the name <b>{}</b> onto the plot area "
                          "to see the actual value.").format(ivid))
                    eventbox = Gtk.EventBox()
                    namelabel = Gtk.Label()
                    namelabel.set_markup("<b>{}</b>".format(ivid))
                    namelabel.props.halign = Gtk.Align.END

                    eventbox.drag_source_set(
                        Gdk.ModifierType.BUTTON1_MASK,
                        [],
                        Gdk.DragAction.COPY
                    )
                    eventbox.drag_source_set_target_list(self.dragtargets)

                    def on_drag_get(widget, context, data, info, time, *args):
                        modelpart, ivid = args
                        string = "{}:::{}".format(modelpart, ivid)
                        data.set_text(string, len(string))
                    eventbox.connect("drag-data-get", on_drag_get, attr, ivid)
                    eventbox.add(namelabel)
                    unitlabel = Gtk.Label.new(iv.unit)
                    unitlabel.props = Gtk.Align.START
                    for w in [unitlabel, scale]:
                        w.set_tooltip_markup("<b>{}</b>\n".format(iv.name) + _(
                            "Drag'n'Drop the name "
                            "<b>{}</b> onto the plot area to add it").format(
                            ivid))
                    for w in [namelabel]:
                        w.set_tooltip_markup("<b>{}</b>\n".format(iv.name) + _(
                            "Drag'n'Drop this onto the plot area to add it"))

                    grid.attach(scale, 1, i, 1, 1)
                    grid.attach_next_to(
                        eventbox, scale, Gtk.PositionType.LEFT, 1, 1)
                    grid.attach_next_to(
                        spinbutton, scale, Gtk.PositionType.RIGHT, 1, 1)
                    grid.attach_next_to(
                        unitlabel, spinbutton, Gtk.PositionType.RIGHT, 1, 1)
                    self._scales[attr][ivid]["scale"] = scale
                    i += 1
                self._scales[attr]["grid"] = grid
        return self._scales

    @property
    def plot_settings(self):
        """
        Current settings from the plot settings page.

        :type: :any:`dict`
        """
        plot_settings = {}
        plot_settings["use_variable_time"] = \
            self["settings_plot_usevariabletime_checkbutton"].get_active()
        plot_settings["consistent_colors"] = \
            self["settings_plot_consistent_colors_checkbutton"].get_active()
        plot_settings["scatter"] = \
            self["settings_plot_scatterplot_checkbutton"].get_active()
        plot_settings["equal_axes"] = \
            self["settings_plot_equal_axes_checkbutton"].get_active()
        plot_settings["identity_line"] = \
            self["settings_plot_show_identity_checkbutton"].get_active()
        plot_settings["split_units"] = \
            self["settings_plot_split_units_checkbutton"].get_active()
        plot_settings["linear_fit"] = \
            self["settings_plot_linear_fit_checkbutton"].get_active()
        plot_settings["fit_intercept"] = \
            self["settings_plot_fit_intercept_checkbutton"].get_active()
        plot_settings["bounds_lim"] = \
            self["settings_plot_bounds_lim_checkbutton"].get_active()
        plot_settings["roll"] = int(
            self["settings_plot_roll_spinbutton"]
            .get_adjustment().get_value())
        plot_settings["show_model_time"] = \
            self["settings_plot_show_model_time_checkbutton"].get_active()
        plot_settings["ids_as_tex"] = \
            self["settings_plot_ids_as_tex_checkbutton"].get_active()
        plot_settings["reverse"] = \
            self["settings_plot_reverse_checkbutton"].get_active()
        plot_settings["show_stats"] = \
            self["settings_plot_show_stats_checkbutton"].get_active()
        plot_settings["model_time"] = self.model.model_time
        plot_settings["convert_units"] = self.model.unit_conversions \
            if self["settings_plot_convert_units_checkbutton"].get_active() \
            else {}
        plot_settings["hist2d"] = \
            self["settings_plot_hist2d_checkbutton"].get_active()
        plot_settings["hist2d_normed"] = \
            self["settings_plot_hist2d_density_checkbutton"].get_active()
        plot_settings["hist2d_bins"] = \
            int(self["hist2d_bin_adjustment"].get_value())
        plot_settings["hist2d_mask_empty"] = \
            self["settings_plot_hist2d_mask_empty_checkbutton"].get_active()
        plot_settings["only_available_times"] = \
            self["settings_plot_only_available_times_checkbutton"].get_active()
        plot_settings["time_as_date"] = \
            self["settings_plot_time_as_date_checkbutton"].get_active()
        plot_settings["plot_method"] = \
            self["settings_plot_type_combobox"].get_active_id()
        plot_settings["robust_linear_fit"] = \
            self["settings_plot_robust_linear_fit_checkbutton"].get_active()
        plot_settings["zero_date"] = self.model.zero_date
        return plot_settings

    ###############
    ### Methods ###
    ###############
    def adjustment_from_iv(self, iv, nsteps=1000):
        """
        Set up a sensible :any:`Gtk.Adjustment` from an :any:`InterfaceValue`

        Args:
            iv (InterfaceValue): the :any:`InterfaceValue`
            nsteps (int, optional): in how many steps to use. Defaults to
                ``1000``.
        """
        # determine sensible lower and upper bounds
        lower, upper = lim_from_iv(iv)
        # now lower and upper are numbers
        # get accurate step width
        stepdiff = (upper - lower) / nsteps
        # count step width decimal places
        stepdiff_nice = 10**-pos_significant_decimal(stepdiff)
        return Gtk.Adjustment(
            value=iv[self.model.model_time], lower=lower, upper=upper,
            step_increment=stepdiff_nice)

    def setup_signals(self, signals, handler):
        """
        This is a workaround to signal.signal(signal, handler)
        which does not work with a ``GLib.MainLoop`` for some reason.
        Thanks to: http://stackoverflow.com/a/26457317/5433146

        Args:
            signals (list): the signals (see :any:`signal` module) to
                connect to
            handler (callable): function to be executed on these signals
        """
        def install_glib_handler(sig):  # add a unix signal handler
            GLib.unix_signal_add(GLib.PRIORITY_HIGH,
                                 sig,  # for the given signal
                                 handler,  # on this signal, run this function
                                 sig  # with this argument
                                 )

        for sig in signals:  # loop over all signals
            GLib.idle_add(  # 'execute'
                install_glib_handler, sig,  # add a handler for this signal
                priority=GLib.PRIORITY_HIGH)

    def apply_data_from_settings(self, *args, **kwargs):
        """
        Read the data from the settings and feed it into the model
        """
        self.add_status("settings", _("Applying new data settings..."))
        for what, d in self.scales.items():
            for ivid, widgets in sorted(d.items()):
                if ivid == "grid":
                    continue
                iv = getattr(self.model, what)[ivid]
                value = widgets["scale"].get_adjustment().get_value()
                if not iv[self.model.model_time] == value:
                    logger.info("{} was changed from {} to {}".format(
                        iv.id, iv[self.model.model_time], value))
                    try:
                        if not self["settings_plot_data_value_insert_"
                                    "checkbutton"].get_active():
                            iv.cut(end=self.model.model_time)
                        iv[self.model.model_time] = value
                    except Exception as e:
                        problem = _("Could not update {} to {}").format(
                            iv.id, value)
                        self.error(
                            main=problem, secondary="<i>{}</i>".format(e))
                        self.add_status("settings", problem, important=True)
                        logger.warning(problem)
                        raise
                    widgets["scale"].get_adjustment().set_value(
                        iv[self.model.model_time])
        # reset model
        model_time_gui = self["model_time_adjustment"].get_value()
        reset_only_variables = self[
            "settings_plot_data_reset_only_variables_checkbutton"].get_active()
        if not model_time_gui == self.model.model_time:
            if reset_only_variables:
                logger.info("Resetting model (only variables) to time {}"
                            .format(model_time_gui))
                only = self.model.variables.values()
            else:
                logger.info("Resetting whole model to time {}".format(
                    model_time_gui))
                only = self.model.content
            self.model.reset(time=model_time_gui,
                             only=[iv.id for iv in only])
            self.apply_model_data_to_settings()

        self.add_status("settings", _("New data fed into model!"))

    def apply_model_data_to_settings(self, *args, **kwargs):
        """
        Read the data from the model and feed it into the settings
        """
        self.add_status("settings", _("Applying model data to settings..."))
        for what, d in self.scales.items():
            for ivid, widgets in sorted(d.items()):
                if ivid == "grid":
                    continue
                iv = getattr(self.model, what)[ivid]
                adj = widgets["scale"].get_adjustment()
                modelvalue = iv[self.model.model_time]
                lower, upper = adj.props.lower, adj.props.upper
                if modelvalue < lower:
                    adj.props.lower = modelvalue - abs(modelvalue - lower)
                elif modelvalue > upper:
                    adj.props.upper = modelvalue + abs(modelvalue - upper)
                adj.set_value(modelvalue)
        # set model time adjustment
        adj = self["model_time_adjustment"]
        model_time = self.model.model_time
        min_model_time = \
            min(min([min(iv.times) for iv in self.model.content]), model_time)
        max_model_time = \
            max(max([max(iv.times) for iv in self.model.content]), model_time)
        lower, upper = adj.props.lower, adj.props.upper
        if min_model_time < lower:
            adj.props.lower = min_model_time - abs(min_model_time - lower)
        elif max_model_time > upper:
            adj.props.upper = max_model_time + abs(max_model_time - upper)
        adj.set_value(model_time)
        self.add_status("settings", _("Model data fed into settings!"))

    def reset_scales(self, what=None):
        """
        Reset scales

        Args:
            what (list, optional): Reset what scales? Sublist of
                ``["variables","forcing","parameters","observations"]`` .
                Reset all if left unspecified.
        """
        if what is None:
            what = self.scales.keys()
        for whatscale in what:
            for ivid, widgets in self.scales[what].items():
                if ivid == "grid":
                    continue
                widgets["scale"].set_value(widgets["initial"])

    def update_current_plot(self, *args, **kwargs):
        """
        Update the current plot
        """
        plot_interfacevalues_kwargs = self.plot_settings
        if plot_interfacevalues_kwargs["use_variable_time"]:
            all_times = np.array([])
            for v in self.model.variables.elements:
                all_times = np.union1d(all_times, v.times)
            plot_interfacevalues_kwargs["times"] = all_times

        current_tab = self["plot_notebook"].get_current_page()
        current_box = self["plot_notebook"].get_nth_page(current_tab)
        current_canvas = current_box.get_children()[0]
        current_figure = current_canvas.figure
        for ax in current_figure.axes:
            current_figure.delaxes(ax)
        for title, plotter in self.custom_plots.items():
            if self.figures.get(title) == current_figure:
                try:
                    plotter(model=self.model, figure=current_figure,
                            **self.plot_settings)
                except Exception as e:
                    self.error(_("Plotting error"), str(e))
                    raise

        for tab, content in self.figures_content.items():
            if self.figures.get(tab) == current_figure:
                self.add_status("plot", _("Plotting..."), important=True)
                interfacevalues = []
                for modelpart, ivs in content.items():
                    interfacevalues.extend(ivs.values())
                try:
                    plot_interfacevalues(
                        interfacevalues,
                        current_figure,  # onto this figure
                        **plot_interfacevalues_kwargs
                    )
                except ValueError as e:
                    if str(e) == \
                            "Width and height specified must be non-negative":
                        self.error(_("Plot area is too small"),
                                   _(
                            "This is a known plotting issue with the fallback "
                            "file-based backend that is used here because "
                            "something didn't work with the GTK/matplotlib "
                            "interaction."
                            "\n\n"
                            "To prevent this, next time you open this GUI, "
                            "make sure the window is big enough for the plots."
                            "\n\n"
                            "This plot seems to be broken from now on...")
                        )
                    else:
                        self.error(_("Plotting error"), str(e))
                        raise
                except Exception as e:
                    self.error(_("Plotting error"), str(e))
                    raise

        current_figure.canvas.draw()

        # if this is a fallback file canvas, tell it to update
        if isinstance(current_canvas, FigureCanvasFile):
            width = current_canvas.get_allocation().width
            height = current_canvas.get_allocation().height
            current_canvas.display(width=width, height=height)
            self.wait_for_gui()

        self.add_status("plot", _("Plot updated!"), important=True)

    ###################
    ### Gui methods ###
    ###################
    def setup_gui(self):
        """
        Set up the GTK gui elements
        """
        def reset_variables(action, *args, **kwargs):
            self.reset_scales("variables")

        def reset_forcing(action, *args, **kwargs):
            self.reset_scales("forcing")

        def reset_params(action, *args, **kwargs):
            self.reset_scales("parameters")

        def reset_observations(action, *args, **kwargs):
            self.reset_scales("observations")

        def feedmodel(action, *args, **kwargs):
            self.apply_data_from_settings()
            self.update_current_plot()

        def reset_plots(action, *args, **kwargs):
            for attr in MODEL_CONTENT:
                label = self["plot_{}_notebook_label".format(attr)]
                italictext = re.sub(
                    string=label.get_text(),
                    pattern=r"^(?:<b><i>)?([^<]+)(?:</i></b>)?$",
                    repl=r"\1")
                label.set_markup(italictext)
            self.figures_content = None

        def show_about_dialog(action, *args, **kwargs):
            self.show_about_dialog()

        def show_hide_hist2d_options(widget, *args, **kwargs):
            for e in [
                "settings_plot_hist2d_bin_label",
                "settings_plot_hist2d_bin_spinbutton",
                "settings_plot_hist2d_density_checkbutton",
                "settings_plot_hist2d_mask_empty_checkbutton",
            ]:
                self[e].set_sensitive(
                    self["settings_plot_hist2d_checkbutton"].get_active() \
                    and \
                    self["settings_plot_scatterplot_checkbutton"].get_active())

        def show_hide_scatter_options(widget, *args, **kwargs):
            for e in [
                "settings_plot_show_identity_checkbutton",
                "settings_plot_equal_axes_checkbutton",
                "settings_plot_linear_fit_checkbutton",
                "settings_plot_show_stats_checkbutton",
                "settings_plot_hist2d_checkbutton",
            ]:
                self[e].set_sensitive(
                    self["settings_plot_scatterplot_checkbutton"].get_active())
                show_hide_linear_fit_options(widget, *args, **kwargs)
                show_hide_hist2d_options(widget, *args, **kwargs)

        def show_hide_model_time_shower_options(widget, *args, **kwargs):
            for e in [
                "settings_plot_show_model_time_checkbutton",
            ]:
                self[e].set_sensitive(not self[
                    "settings_plot_usevariabletime_checkbutton"].get_active())

        def show_hide_linear_fit_options(widget, *args, **kwargs):
            for e in [
                "settings_plot_fit_intercept_checkbutton",
                "settings_plot_robust_linear_fit_checkbutton",
            ]:
                self[e].set_sensitive(
                    self["settings_plot_linear_fit_checkbutton"]
                    .get_active() and
                    self["settings_plot_scatterplot_checkbutton"]
                    .get_active()
                )

        def online_help(action, *args, **kwargs):
            webbrowser.open("https://nobodyinperson.gitlab.io/"
                            "python3-numericalmodel/gui.html")

        def save_plot(action, *args, **kwargs):
            filename = self.save_current_plot_dialog()
            if filename:
                nb = self["plot_notebook"]
                canvas = nb.get_nth_page(
                    nb.get_current_page()).get_children()[0]
                self.add_status("plot", text=_(
                    "Saving the current plot to '{}'..."
                ).format(filename), important=True)
                try:
                    canvas.figure.savefig(filename)
                except Exception as e:
                    self.error(main=_("Error saving plot"), secondary=str(e))
                    raise
                self.add_status(
                    "plot",
                    text=_("Current plot was saved to '{}'!").format(filename),
                    important=True)

        # connect signals
        self.handlers = {
            "CloseApplication": self.quit,
            "Integrate": self.integrate,
            "UpdatePlot": self.update_current_plot,
            "ShowAbout": show_about_dialog,
            "ShowHideScatterOptions": show_hide_scatter_options,
            "ShowHideLinearFitOptions": show_hide_linear_fit_options,
            "ShowHideHist2dOptions": show_hide_hist2d_options,
            "SavePlot": save_plot,
            "ResetParams": reset_params,
            "OnlineHelp": online_help,
            "ResetForcing": reset_forcing,
            "ResetVariables": reset_variables,
            "ResetObservations": reset_observations,
            "ResetPlots": reset_plots,
            "FeedModel": feedmodel,
            "ShowHideModelTimeShowerOptions":
                show_hide_model_time_shower_options,
        }
        self.builder.connect_signals(self.handlers)

        ### Plot ###
        # add the Figure to the plot box in the gui
        def on_drag_motion(widgt, context, x, y, time, *args):
            Gdk.drag_status(context, Gdk.DragAction.COPY, time)
            return True

        def on_drag_drop(widget, context, x, y, time, *args):
            widget.drag_get_data(context, context.list_targets()[-1], time)
            return True

        def on_drag_data_received(widget, context, x, y, data, info, time,
                                  user_data):
            try:
                attr, ivid = data.get_text().split(":::")
            except ValueError:
                self.error(main=_("Strange dropped content!"),
                           secondary=_("Whatever you dropped into here "
                                       "doesn't work :-)"))
                Gtk.drag_finish(context, False, False, time)
                return False

            figures_content = self.figures_content.copy()
            newdict = {ivid: getattr(self.model, attr)[ivid]}
            try:
                figures_content[user_data]
            except KeyError:
                figures_content[user_data] = {}
            try:
                figures_content[user_data][attr].update(newdict)
            except KeyError:
                figures_content[user_data][attr] = newdict
            nb = self["plot_notebook"]
            label = nb.get_tab_label(nb.get_nth_page(nb.get_current_page()))
            italictext = re.sub(
                string=label.get_text(),
                pattern=r"^(?:<b><i>)?([^<]+)(?:</i></b>)?$",
                repl=r"<b><i>\1</i></b>")
            label.set_markup(italictext)
            self.figures_content = figures_content
            Gtk.drag_finish(context, True, False, time)

        def on_event(widget, event):
            if event.type == Gdk.EventType.BUTTON_PRESS \
                    and event.button.button == 3:
                self["plot_menu"].popup(
                    None, None, None, None, event.button.button, event.time)

        # set up default figures
        for n, fig in self.figures.items():
            box = self["plot_{}_box".format(n)]
            if box:
                if self.use_fallback:
                    canvas = FigureCanvasFile(fig)
                else:
                    canvas = FigureCanvas(fig)
                canvas.drag_dest_set(0, [], Gdk.DragAction.COPY)
                canvas.drag_dest_set_target_list(self.dragtargets)
                canvas.connect("drag-motion", on_drag_motion)
                canvas.connect("drag-drop", on_drag_drop)
                canvas.connect("drag-data-received", on_drag_data_received, n)
                canvas.connect("event", on_event)
                box.pack_start(canvas, True, True, 0)
        # set up custom figures
        for title, plotter in sorted(self.custom_plots.items()):
            fig = self.figures.get(title)
            if self.use_fallback:
                canvas = FigureCanvasFile(fig)
            else:
                canvas = FigureCanvas(fig)
            box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
            box.pack_start(canvas, True, True, 0)
            label = Gtk.Label(title)
            self["plot_notebook"].append_page(box, label)

        ### Fill the settings dialog ###
        for what, d in sorted(self.scales.items()):
            expander_box = self["{}_slider_box".format(what)]
            expander_box.pack_start(d["grid"], True, True, 3)

        for value, text in zip(
            [60, 10 * 60, 30 * 60, 60 * 60],
            [_("1 min"), _("10 min"), _("30 min"), _("1 hour")]
        ):
            self["time_scale"].add_mark(value, Gtk.PositionType.TOP, text)

        self.add_status("general", _("Running a NumericalModel interactively"))

        self["main_applicationwindow"].props.icon = self.logo_pixbuf
        # show everything
        self["main_applicationwindow"].set_title(self.model.name)
        self["main_applicationwindow"].show_all()

        self.apply_model_data_to_settings()

        self.update_current_plot()

    def error(self, main, secondary=None):
        """
        Display a error dialog

        Args:
            main (str): the main text to display
            secondary (str, optional): the secondary text to display
        """
        dialog = Gtk.MessageDialog(
            self["main_applicationwindow"],
            0,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK,
            main
        )
        if secondary is not None:
            dialog.format_secondary_markup(secondary)
        dialog.run()
        dialog.destroy()

    def wait_for_gui(self):
        """
        Wait for the gui to process all pending events
        """
        while Gtk.events_pending():
            Gtk.main_iteration()

    def integrate(self, *args, **kwags):
        """
        Integrate the underlying model by the step defined in the
        ``time_adjustment``.
        """
        start_time = utils.utcnow()
        self.apply_data_from_settings()
        step = self["time_adjustment"].get_value()
        self.add_status("model", _("Integrating..."), important=True)
        integration_start_time = utils.utcnow()
        try:
            model_time_before_integration = self.model.model_time
            self.model.integrate(final_time=self.model.model_time + step)
            model_time_after_integration = self.model.model_time
            self.add_status("model", _("Integration was successful!"),
                            important=True)
        except Exception as e:
            self.add_status("model", _("Integration FAILED!"), important=True)
            self.error(main=_("Integration failed!"),
                       secondary="<i>{}</i>".format(e))
            raise
        integration_end_time = utils.utcnow()
        self.apply_model_data_to_settings()
        plot_start_time = utils.utcnow()
        self.update_current_plot()
        plot_end_time = utils.utcnow()
        end_time = utils.utcnow()
        self.add_status(
            "model",
            _(
                "Performance: integration ({:.3f} s, "
                "model/realtime-ratio: {:.3f}), "
                " plotting ({:.3f} s), total ({:.3f} s)").format(
                integration_end_time -
                integration_start_time,
                (model_time_after_integration-model_time_before_integration) \
                    /(integration_end_time - integration_start_time),
                plot_end_time -
                plot_start_time,
                end_time -
                start_time),
            important=True)

    def add_status(self, context, text, important=False):
        """
        Add a status to the statusbar

        Args:
            context (str): the context in which to display the text
            text (str): the text to display
            important (bool, optional): Make sure the text is **really**
                displayed by calling :any:`wait_for_gui`. Defaults to ``False``.
                Enabling this can slow down the gui.
        """
        logger.info("[{}] {}".format(context, text))
        context_id = self["statusbar"].get_context_id(context)
        self["statusbar"].push(context_id, text)
        if important:
            self.wait_for_gui()

    ###############
    ### Dialogs ###
    ###############
    def show_about_dialog(self):
        """
        Show the about dialog
        """
        dialog = self["aboutdialog"]
        logopixbuf = self.logo_pixbuf.scale_simple(
            200, 200, GdkPixbuf.InterpType.BILINEAR)
        dialog.set_logo(logopixbuf)
        dialog.set_version(__version__)
        dialog.run()
        dialog.hide()

    def save_current_plot_dialog(self):
        """
        Display a dialog to select a plot saving destination

        Returns:
            :any:`str` or ``False``: the path to save to or ``False``
        """
        # create a dialog
        dialog = Gtk.FileChooserDialog(
            _("Please select a saving destination"),  # title
            self["main_applicationwindow"],  # parent
            Gtk.FileChooserAction.SAVE,  # Action
            # Buttons (obviously not possible with glade!?)
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )

        # add the filter
        filters = {
            _("PDF files"): ["application/pdf"],
            _("PNG files"): ["image/png"]
        }
        plotmimetypes = []
        for name, mimetypes in filters.items():
            plotmimetypes.extend(mimetypes)
        allfilters = [(_("Plot files"), plotmimetypes)]
        allfilters.extend(sorted(filters.items()))
        for name, mimetypes in allfilters:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(name)
            for mimetype in mimetypes:
                filefilter.add_mime_type(mimetype)
            dialog.add_filter(filefilter)

        response = dialog.run()  # run the dialog
        if response == Gtk.ResponseType.OK:  # file selected
            filename = dialog.get_filename()
            logger.debug("File '{}' selected".format(filename))
        elif response == Gtk.ResponseType.CANCEL:  # cancelled
            filename = False
            logger.debug("File selection cancelled")
        else:  # something else
            filename = False
            logger.debug("File selection dialog was closed")

        dialog.destroy()  # destroy the dialog, we don't need it anymore
        return filename

    def run(self):
        """
        Run the gui
        """
        # set up the gui
        self.setup_gui()
        # run the gui
        logger.debug("starting mainloop")
        Gtk.main()
        logger.debug("mainloop is over")

    def quit(self, *args):
        """
        Stop the gui
        """
        logger.debug("received quitting signal")
        logger.debug("stopping mainloop...")
        Gtk.main_quit()
        logger.debug("mainloop stopped")

    #######################
    ### Special methods ###
    #######################
    def __getitem__(self, key):
        """
        When indexed, return the corresponding Glade gui element

        Args:
            key (str): the Glade gui element name
        """
        return self.builder.get_object(key)


def num_decimals(x):
    """
    Deterine the number of digits after the decimal point

    Args:
        x (float): the number of interest

    Returns:
        int : the number of digits after the decimal point or 0 there are none
    """
    string = str(x)
    match = re.match(string=string, pattern=r"^\de([+-]\d+)$")
    if match:
        decimals = -int(match.groups()[0])
    else:
        nonulls = re.sub(string=string, pattern=r"0+$", repl="")
        decimals = nonulls[::-1].find(".")
    return max(decimals, 0)


def pos_significant_decimal(x):
    """
    Deterine the position of the most significant digit after the decimal point

    Args:
        x (float): the number of interest

    Returns:
        int : the position of the most significant digit after the decimal
            point or 0 there are none
    """
    string = "{:.30f}".format(x)
    match = re.match(string=string, pattern=r"^.*?\.(0*)[1-9]\d*$")
    if match is None:
        return 0
    else:
        return len(match.groups()[0]) + 1
