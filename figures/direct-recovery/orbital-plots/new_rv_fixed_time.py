"""Radial Velocity Orbit.

Goals
-----
To calculate when the radial velocity is different by a certain value.
Plot radial velocity phase curves. Indicating obtained measurement locations.


This extension is to create the plots for thesis. Period 89


#TODO :
Extend this to request for a given period number

E.g Period 89
    Period 92
"""
import argparse
import logging
import sys
from datetime import datetime
from typing import Dict, List, Any, Union
import matplotlib
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.constants import c
from mpl_toolkits.axes_grid1 import host_subplot

from utils.parse import parse_paramfile
from utils.rv_utils import RV, JulianDate, prepare_mass_params, generate_companion_label
from utils.rv_utils import strtimes2jd, join_times, check_core_parameters

c_km_s = c.to(u.kilometer / u.second)  # Speed of light in km/s
from matplotlib import style
style.use("thesis")

def parse_args(args: List[str]) -> argparse.Namespace:
    """RV Argparse parser."""
    parser = argparse.ArgumentParser(description='Radial velocity plotting')
    parser.add_argument('params', help='RV parameters filename', type=str)
    parser.add_argument('-d', '--date', default=None,
                        help='Reference date in format YYYY-MM-DD [HH:MM:SS]. Default=None uses time of now.')
    # parser.add_argument('-r', '--rv_diff', help='RV difference threshold to find')
    parser.add_argument('-o', '--obs_times', help='Times of previous observations YYYY-MM-DD format',
                        nargs='+', default=None)
    parser.add_argument('-l', '--obs_list', help='File with list of obs times.', type=str, default=None)

    parser.add_argument("--save_only", help="Only save the figure, do not show it.", action="store_true")
    parser.add_argument("--debug", help="Turning on debug output", action='store_true')
    return parser.parse_args(args)


def main(params, mode="phase", obs_times=None, obs_list=None, date=None,
         cycle_fraction=1, phase_center=0, save_only=False):  # obs_times=None, mode='phase', rv_diff=None
    # type: (Dict[str, Union[str, float]], str, List[str], str, str, bool) -> None
    r"""Radial velocity displays.

    Parameters
    ----------
    params: str
        Filename for text file containing the rv parameters. Format of 'param = value\n'.
    mode: str
        Mode for script to use. Phase, time.
    obs_times: list of str
        Dates of observations added manually at command line of format YYYY-MM-DD.
    obs_list: str
        Filename for list which contains obs_times (YYY-MM-DD HH:MM:SS).
    date: str
        Reference date for some modes. Defaults=None)
    """

    # Load in params and store as a dictionary
    parameters = parse_paramfile(params)

    parameters = prepare_mass_params(parameters, only_msini=True)

    parameters = check_core_parameters(parameters)

    # combine obs_times and obs_list and turn into jd.
    if obs_times:
        if (".txt" in obs_times) or (".dat" in obs_times):
            raise ValueError("Filename given instead of dates for obs_times.")

    obs_times = join_times(obs_times, obs_list)
    obs_jd = strtimes2jd(obs_times)

    test_jd = obs_jd[0] if isinstance(obs_jd, (list, tuple)) else obs_jd

    if ((str(parameters["tau"]).startswith("24") and not str(test_jd).startswith("24")) or
        (not(str(parameters["tau"]).startswith("24")) and str(test_jd).startswith("24"))):
        raise ValueError("Mismatch between Tau parameter '{0}' and times used '{1}'.".format(parameters["tau"], obs_jd))

    date_split = JulianDate.now().jd if date is None else JulianDate.from_str(date).jd

    past_obs = [obs for obs in obs_jd if obs <= date_split]

    host_orbit = RV.from_dict(parameters)
    companion_orbit = host_orbit.create_companion()

    fig = binary_time_curve_fixed_limits(host_orbit, companion_orbit, t_past=past_obs)

    save_name = (params.split("/")[-1]).split("_")[0] + "_p89.pdf"
    save_name2 = (params.split("/")[-1]).split("_")[0] + "_p89.png"
    fig.savefig(save_name)
    fig.savefig(save_name2, dpi=400)
    if not save_only:
        plt.show(fig)

    return fig


def binary_time_curve_fixed_limits(host, companion, ignore_mean=False, t_past=False):
    # type: (RV, RV, float, bool, Any, Any, Any) -> int
    """Plot RV phase curve centered on zero.

    Parameters
    ----------
    host: RV
        RV class for system.

    ignore_mean: bool
        Remove the contribution from the systems mean velocity. (Default=False)
    t_past: float, array-like
        Times of past observations in julian days.

    Returns
    -------
    exit_status: bool
        Returns 0 if successful.

        Displays matplotlib figure.
    """
    # Fixing limits to 2012-04-01 to 2012-09-30
    t_start = JulianDate.from_str("2012-04-01").jd
    tend = JulianDate.from_str("2012-09-30").jd

    companion_present = companion is not None


    # Specify 100 points per period
    num_points = 500

    t_space = np.linspace(t_start, tend,      num_points)

    start_dt = JulianDate(t_start).to_datetime()
    if (start_dt.hour == 0) and (start_dt.minute == 0) and (start_dt.second == 0):
        start_string = datetime.strftime(start_dt, "%Y-%m-%d")
    else:
        start_string = datetime.strftime(start_dt, "%Y-%m-%d %H:%M:%S")  # Issue with 00:00:01 not appearing

    fig = plt.figure(figsize=(5, 4))
    fig.subplots_adjust()
    ax1 = host_subplot(111)

    host.ignore_mean = ignore_mean
    host_rvs = host.rv_at_times(t_space)
    ax1.plot(t_space - t_start, host_rvs, label="Host", lw=2, color="k")
    # Determine rv max amplitudes.
    amp1 = host.max_amp()
    # Adjust axis limits
    ax1.set_ylim(host.gamma - (amp1 * 1.1), host.gamma + (amp1 * 1.1))
    ax1.axhline(host.gamma, color="black", linestyle="-.", alpha=0.5)
    ax1.set_xlabel("Days from {!s}".format(start_string))
    ax1.set_ylabel("Host RV (km/s)")

    if companion_present:
        companion.ignore_mean = ignore_mean
        companion_rvs = companion.rv_at_times(t_space)
        companion_label = generate_companion_label(companion)
        ax2 = ax1.twinx()
        ax2.plot(t_space - t_start, companion_rvs, '--', label=companion_label, lw=2)
        # Adjust axis limits
        amp2 = companion.max_amp()
        # Determine rv max amplitudes.
        ax2.set_ylim(companion.gamma - (amp2 * 1.1), companion.gamma + (amp2 * 1.1))
        #ax2.axhline(companion.gamma, color="black", linestyle="-.", alpha=0.5)
        ax2.set_ylabel("Companion RV (km/s)")

    if t_past:
        t_past = np.asarray(t_past)
        rv_star = host.rv_at_times(t_past)
        ax1.plot(t_past - t_start, rv_star, "x", markersize=8, markeredgewidth=2, alpha=0.7)
        if companion_present:
            rv_planet = companion.rv_at_times(t_past)
            ax2.plot(t_past - t_start, rv_planet, "r*", markersize=8, markeredgewidth=2, alpha=0.7)


    if 'name' in host._params.keys():
        if ("companion" in host._params.keys()) and (companion_present):
            plt.title("Period 89: {} {}".format(host._params['name'].upper(), host._params['companion']))
        else:
            plt.title("Period 89: {}".format(host._params['name'].upper()))
    else:
        plt.title("Radial Velocity Curve")
    plt.legend(loc=0)

    return fig


if __name__ == '__main__':
    args = vars(parse_args(sys.argv[1:]))
    debug = args.pop('debug')
    opts = {k: args[k] for k in args}

    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(levelname)s %(message)s')

    fig = main(**opts)
