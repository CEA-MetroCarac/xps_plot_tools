""" Necessary imports for the GUI and different modules for the tabs"""

from tkinter import Tk
from tkinter.ttk import Notebook
from xps_plot_tools.display_frame import DisplayFrame
from xps_plot_tools.plot_frame import PlotFrame
from xps_plot_tools.help_frame import HelpFrame


# from rsf_frame import RSF_Frame


class XPSApp(Tk):
    """Class representing the whole application"""

    def __init__(self):
        """
        Initialize the main window, place all the tabs and run the GUI

        Parameters
        ----------

        Returns
        -------

        """
        ##################
        # TKINTER WINDOW #
        ##################
        Tk.__init__(self)

        # Set the title
        self.title('XPS quantification display')

        # Set the dimensions of the main window
        self.geometry("1100x900")

        ############
        # NoteBook #
        ############

        self.tabs = Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        ######################
        # QUANTI DISPLAY TAB #
        ######################

        self.display_tab = DisplayFrame(self.tabs)
        self.tabs.add(self.display_tab, text='Display Quantification')

        ###################
        # FIT DISPLAY TAB #
        ###################

        self.plot_tab = PlotFrame(self.tabs)
        self.tabs.add(self.plot_tab, text='Fit Plot')

        ############
        # HELP TAB #
        ############

        self.help_tab = HelpFrame(self.tabs)
        self.tabs.add(self.help_tab, text='About / Help')


if __name__ == "__main__":
    app = XPSApp()
    app.mainloop()


def plot_tools_launch():
    """ Entry point for the Metro carac toolbox """

    app = XPSApp()
    app.mainloop()
