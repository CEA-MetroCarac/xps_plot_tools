"""
Example of functions related to plot GUI
NB : These functions are not meant to be used without the GUI
The only purpose of this code is to be able to run tests without a user
"""
from pathlib import Path

from xps_plot_tools.main import XPSApp

DATA_PATH = Path(__file__).parent / "data"


def ex_load_data(display=False):
    """
    Create an app and try to load the data from the data files
    """

    # Create the app
    ex_app = XPSApp()

    # Reset the path entries
    ex_app.display_tab.data_ENTRY.delete(0, 'end')
    ex_app.display_tab.rsf_ENTRY.delete(0, 'end')
    ex_app.plot_tab.data_ENTRY.delete(0, 'end')
    ex_app.plot_tab.config_ENTRY.delete(0, 'end')

    # Set the path entries with data paths
    ex_app.display_tab.data_ENTRY.insert(0, DATA_PATH / "plot_tools_NG2_profile_AsEPI_Cr.txt")
    ex_app.display_tab.rsf_ENTRY.insert(0, DATA_PATH / "plot_tools_RSF_Cr.txt")
    ex_app.plot_tab.data_ENTRY.insert(0, DATA_PATH)
    ex_app.plot_tab.config_ENTRY.insert(0, DATA_PATH / "plot_tools_config.txt")

    # Try to load data
    ex_app.display_tab.load_data()

    if display:
        ex_app.mainloop()

    return ex_app


def ex_update_entries(display=False):
    """
    Create an app load data and try all the plotting
    configuration for the quantification display
    """

    # Create the app and load data
    ex_app = ex_load_data()

    # Select the first sample to test update_orbit_list_and_ref
    ex_app.display_tab.sample_LIST.select_set(0)

    # Try all the plotting configuration
    for j in range(2):

        # With and without the curve option selected
        ex_app.display_tab.is_curve.set(j)

        # For all the different modes
        for i in range(3):
            ex_app.display_tab.calc_type.set(i)
            ex_app.display_tab.update_entries()

    # Run the app
    if display:
        ex_app.mainloop()
    else:
        ex_app.destroy()


def ex_plot_figure(display=False):
    """
    Create an app load data and try to plot
    relative concentration on the quantification display
    and Silicon 2p spectrum in plot frame
    """

    # Create the app and load data
    ex_app = ex_load_data()

    ##################
    # QUANTI DISPLAY #
    ##################

    # Select relative mode
    ex_app.display_tab.calc_type.set(1)

    # Select the samples
    ex_app.display_tab.sample_LIST.select_set(0)
    ex_app.display_tab.sample_LIST.select_set(1)
    ex_app.display_tab.sample_LIST.select_set(2)
    ex_app.display_tab.update_orbit_list_and_ref()

    # Select the desired core levels
    for j in range(10):
        ex_app.display_tab.orbit_LIST.select_set(j)

    for j in range(16, 20):
        ex_app.display_tab.orbit_LIST.select_set(j)
    ex_app.display_tab.orbit_LIST.select_set(21)

    # Plot the figure
    ex_app.display_tab.plot_figure()

    ####################
    # SPECTRUM DISPLAY #
    ####################

    ex_app.plot_tab.plot_figure()

    # Run the app
    if display:
        ex_app.mainloop()
    else:
        ex_app.destroy()


if __name__ == '__main__':
    ex_plot_figure(display=True)
