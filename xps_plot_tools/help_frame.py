""" Module to implement the help tab """

from tkinter import Frame, TOP, Label, Button
import os

class HelpFrame (Frame):

    """ Class representing the help tab """

    def __init__(self,  master=None, **kw):

        """
    Initialize the frame and place all the elements
    Parameters
    ----------
    master: Tkinter() or Tkinter.Frame()
        Master which contains the frame

    Returns
    -------

    """

        ##############
        # FRAME INIT #
        ##############

        super().__init__(master, **kw)

        ###########
        # CREDITS #
        ###########

        # Credit labels
        Label(self, text='Credits', font = ('Arial', 20, 'bold')).pack(side=TOP)
        Label(self, text='This software have been developped in the context of a M2 Internship by Alexandre Boyer in 2024',
              font = ('Arial', 15)).pack(side=TOP)


        ########
        # HELP #
        ########

        # File path for the help
        self.help_path  = "S:/205-Caracterisation_Metrologie/205.01-C_Analyse_de_Surface/06-Protocoles/Python/XPS Plot_Operating Manual.pptx"

        # Text
        Label(self, text='For any questions please contact Oliver Renault at oliver.renault@cea.fr or Nicolas Gauthier at nicolas.gauthier@cea.fr',\
                          font = ('Arial', 15)).pack(side=TOP)

        # Button
        Label(self, text='Operating manuel', font = ('Arial', 20, 'bold')).pack(side=TOP)
        Label(self, text=self.help_path, font = ('Arial', 15)).pack(side=TOP)
