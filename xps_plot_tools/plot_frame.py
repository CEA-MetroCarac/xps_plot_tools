""" Module to implement fit plotting """

from glob import glob
from os import path
from tkinter import Frame, LabelFrame, BOTTOM, LEFT, TOP, Label, Button, Entry, StringVar, BooleanVar, Checkbutton
from tkinter.messagebox import showerror
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from tkinter.ttk import Combobox
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PolyCollection
from carac.xps.plot_tools.toolbar import ExpendedToolbar

class PlotFrame (Frame):

    """ Class representing the frame used to plot spectrum and fits """

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

        #################
        # DISPLAY FRAME #
        #################

        # Create and display the frame
        self.display_FRAME = LabelFrame(self, text = "Display", height=20,width=20)
        self.display_FRAME.pack(side = BOTTOM, padx=5, pady=2)

        # Create the figure and link it to the canvas
        self.fig = plt.Figure(figsize = (11, 7.2), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.display_FRAME)

        # Set the different variables
        self.current_ax = 0
        self.nb_plots = 0
        self.nb_new_orbit = 0
        self.all_files = []
        self.compound_dict = {}

        # set the color order to be ploted
        self.color = ['r', 'b', 'g', 'm', 'orange', 'c', 'brown', 'teal', 'y',
                'purple', 'pink', 'k', 'lightcoral', 'gold', 'crimson', 'peru']

        # Draw the canvas
        self.canvas.draw()

        # create the Matplotlib toolbar
        self.toolbar = ExpendedToolbar(self.canvas, self.display_FRAME, self.fig)
        self.toolbar.pack()
        self.toolbar.update()

        # Place the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

        ################
        # CONFIG FRAME #
        ################

        self.config_FRAME = Frame(self)
        self.config_FRAME.pack(side=TOP)

            ##############
            # PATH FRAME #
            ##############

        # Frame
        self.path_FRAME = LabelFrame(self.config_FRAME, borderwidth=2, text = "Chose the files")
        self.path_FRAME.pack(side=LEFT, padx=5, pady=5)

        # Side labels
        Label(self.path_FRAME, text="Casa file").grid(row = 1, column=1, padx=2, pady=2)
        Label(self.path_FRAME, text="Config file").grid(row = 2, column=1, padx=2, pady=2)

        # Variable for each path
        self.data_path = StringVar()
        self.config_path = StringVar()

        # Entry for each path
        self.data_ENTRY = Entry(self.path_FRAME, textvariable = self.data_path, width=30)
        self.data_ENTRY.grid(row = 1, column=2, padx=2, pady=2)
        self.config_ENTRY = Entry(self.path_FRAME, textvariable = self.config_path, width=30)
        self.config_ENTRY.grid(row = 2, column=2, padx=2, pady=2)

        # Browse button for data path
        Button(master = self.path_FRAME,
               height = 1,
               width = 1,
               text = "...",
               command = lambda : self.ask_path('data'))\
               .grid(row = 1, column=3, padx=2, pady=2)

        Button(master = self.path_FRAME,
               height = 1,
               width = 1,
               text = "...",
               command = lambda : self.ask_path('config'))\
               .grid(row = 2, column=3, padx=2, pady=2)

            ##############
            # REST OF IT #
            ##############

        # Combobox for Counts / CPS
        self.data_type_CB = Combobox(self.config_FRAME, width = 7)
        self.data_type_CB.pack(side = LEFT,padx=5, pady=2)
        self.data_type_CB['values'] = ['CPS', 'Counts']
        self.data_type_CB.current(0)

        # Variables for the CheckBoxes
        self.is_filled = BooleanVar() # True if you want to fill the space between the cruve and the background
        self.is_residuals = BooleanVar() # True if you want to display the residuals
        self.is_background = BooleanVar() # True if you want to remove the background

        # Checkboxes
        Checkbutton(self.config_FRAME,
                    text = 'Filled components',
                    variable=self.is_filled,
                    onvalue=True,
                    offvalue=False)\
                    .pack(side = LEFT)

        Checkbutton(self.config_FRAME,
                    text = 'Residuals',
                    variable=self.is_residuals,
                    onvalue=True,
                    offvalue=False)\
                    .pack(side = LEFT)

        Checkbutton(self.config_FRAME,
                    text = 'Remove background',
                    variable=self.is_background,
                    onvalue=True,
                    offvalue=False)\
                    .pack(side = LEFT)

        # Save figures Button
        Button(self.config_FRAME,
                    text = 'Save figures',
                    command=self.save_fig)\
                    .pack(side = LEFT)

        # Propagate Button
        Button(master = self.config_FRAME,
               height = 1,
               width = 10,
               text = "Propagate",
               command = self.propagate_params)\
               .pack(side=LEFT, padx= 5, pady= 5)

        # Save Config Button
        Button(master = self.config_FRAME,
               height = 1,
               width = 10,
               text = "Save Config",
               command = self.save_config)\
               .pack(side=LEFT, padx= 5, pady= 5)

        # Plot Button
        Button(master = self.config_FRAME,
               height = 1,
               width = 5,
               text = "Plot",
               command = self.plot_figure)\
               .pack(side=LEFT, padx= 5, pady= 5)

        # Navigation buttons
        Button(master = self.config_FRAME,
               height = 1,
               width = 3,
               text = "<",
               command = lambda : self.switch(0))\
               .pack(side=LEFT, padx = 5)

        Button(master = self.config_FRAME,
               height = 1,
               width = 3,
               text = ">",
               command = lambda : self.switch(1))\
               .pack(side=LEFT)

    def ask_path(self, val):

        """
        Open a windows explorer to get the location of the folder
        containing the required data and store it into the associtated entry
        ----------
        val : str
            'data' for the csv folder and config file for any other string
        Returns
        -------
        """

        # Update the variable according to the val selected
        if val == 'data':
            filepath = askdirectory(title="Select " + val +" folder ")
            self.data_path.set(filepath)
        else:
            filepath = askopenfilename(title="Select " + val +" file ",
                                       filetypes=[('txt files','.txt'),('all files','.*')])
            self.config_path.set(filepath)

    def plot_figure(self):

        """ Create and plot the axes for all the csv files contained in the folder """

        # Ajust the current index
        if self.nb_plots*2 == len(self.fig.get_axes()) and not self.is_residuals.get():
            self.current_ax = int(self.current_ax/2)

        if self.nb_plots == len(self.fig.get_axes()) and self.is_residuals.get():
            self.current_ax = int(self.current_ax*2)


        # Get all the csv files in the folder
        self.all_files = glob(path.join(self.data_path.get(), "*.csv"))
        self.nb_plots = len(self.all_files)

        # Check if there is a csv file in the folder
        if not self.nb_plots:
            showerror("No file", "Please select a folder with csv files")
            return None

        # Clear the figure
        self.fig.clf()

        # If there is a config file load it
        if self.config_path.get():

            # Read the JSON string from the config file
            with open(self.config_path.get(), "r", encoding="utf-8") as file:
                dict_string = file.read()

            # Convert the JSON string to a dictionary
            self.compound_dict = json.loads(dict_string)

        # Else reset the dict
        else:
            self.compound_dict = {}

        # Reset the number of new orbits
        self.nb_new_orbit = 0

        # For all files found
        for csv in self.all_files:

            # Extract the data from the csv
            header = pd.read_csv(csv, skiprows=2, nrows=4, sep=',').dropna(axis=1)
            components_data = pd.read_csv(csv, skiprows=7, sep=',').dropna(axis=1)

            # Get the axes
            self.plot_indiv(components_data, header.shape[1] - 1)

        # Update the canvas
        self.update_axes()

    def plot_indiv(self, dftoplot, nb_comp):

        """ Create the axes and plot the curves associated with the csv file 
         Parameters
        ----------
        dftoplot: panda dataframe
            Contains all the data to plot
        nb_comp: int
            number of components in the axes
        Returns
        -------
        """

        # Create the axe(s) according to the selection of the user
        if self.is_residuals.get():
            ax_res, ax_data  = self.fig.subplots(2, 1, gridspec_kw={'height_ratios': [1, 4]})
        else:
            ax_res, ax_data = None, self.fig.subplots()

        # Selection between Counts vs CPS

        # Data
        dftoplot['y'] = dftoplot['Counts'] * self.data_type_CB.current()\
                      + dftoplot['CPS'] * (1-self.data_type_CB.current())

        # Background
        dftoplot['Background y'] = dftoplot['Background'] * self.data_type_CB.current()\
                                 + dftoplot['Background CPS'] * (1-self.data_type_CB.current())

        # Envelope
        dftoplot['Envelope y'] = dftoplot['Envelope'] * self.data_type_CB.current()\
                               + dftoplot['Envelope CPS'] * (1-self.data_type_CB.current())

        # Store the index of the first component
        first_comp = 2 + (4 + nb_comp) * (1-self.data_type_CB.current())

        # Change the y label according to the choice of the user
        y_labelis = "Counts" * self.data_type_CB.current()\
                  + "CPS" * (1-self.data_type_CB.current())

        # Get the different value from background
        diff_meas_sim = dftoplot[(dftoplot['y'] - dftoplot['Background y']) != 0]

        # Remove or not the background
        dftoplot['Background_remove'] = dftoplot['Background y'] * self.is_background.get()

        # Plot the intensity
        intensity = ax_data.plot(dftoplot['B.E.'],
                                 dftoplot['y'] - dftoplot['Background_remove'],
                                 'o',
                                 color='black',
                                 markersize=5, markerfacecolor='white',
                                 markeredgewidth=1.2,
                                 markeredgecolor='grey', label='_intensity')

        # Check if the intensity is already registered
        if '_intensity' in self.compound_dict:
            self.apply_params(intensity[0])
        else :
            self.load_params(intensity[0])

        # Plot the envelope
        envelope = ax_data.plot(dftoplot['B.E.'],
                    dftoplot['Envelope y'] - dftoplot['Background_remove'],
                    c='k',
                    linewidth=2,
                    label='_Envelope',
                    alpha = 0.5)

        # Check if the Envelope is already registered
        if '_Envelope' in self.compound_dict:
            self.apply_params(envelope[0])
        else:
            self.load_params(envelope[0])

        #######################
        # plot each component #
        #######################

        # Array to store if we have already see the orbit for the label
        already_seen = []

        for j in range(nb_comp):

            # Get the index of the component
            comp_data = dftoplot.iloc[:, first_comp + j]

            # Get the indexes where the component differ from the background
            indexes = (abs(comp_data - dftoplot['Background y']) >= 0.1).values.flatten()

            # Get the name of the component
            comp_name = re.sub(r'\.\d+$', '',comp_data.name)

            # If we don't have the orbit in the config file we add it
            if not comp_name in self.compound_dict:

                # Plot the line
                orbit = ax_data.plot(dftoplot[indexes]['B.E.'],
                                    comp_data[indexes] - dftoplot[indexes]['Background_remove'],
                                    c = self.color[self.nb_new_orbit % 16],
                                    linewidth = 3,
                                    label = comp_name)

                # Init the params from the line
                self.load_params(orbit[0],comp_name)

                # Update the number of the color
                self.nb_new_orbit += 1

                # Add the component ot All ready seen
                already_seen.append(comp_name)
            else:
                # If we already seen the orbit (spin orbit doublet) we disable the legend
                first_instance = not comp_name in already_seen

                # Plot the line
                orbit = ax_data.plot(dftoplot[indexes]['B.E.'],
                                    comp_data[indexes] - dftoplot[indexes]['Background_remove'],
                                    label = '_' * (1-first_instance) + comp_name)

                # Init the params from the line
                self.apply_params(orbit[0],comp_name)

                # Add the component ot All ready seen
                if first_instance:
                    already_seen.append(comp_name)

            # Fill between component data and background if asked
            if self.is_filled.get():
                ax_data.fill_between(dftoplot['B.E.'],
                                        comp_data - dftoplot['Background_remove'],
                                        dftoplot['Background y'] - dftoplot['Background_remove'],
                                        facecolor=self.compound_dict[comp_name][4],
                                        alpha=0.1,
                                        label = '_' +  comp_name)

        # Plot the background
        background = ax_data.plot(dftoplot['B.E.'],
                    dftoplot['Background y'] - dftoplot['Background_remove'],
                    c='k',
                    linewidth=2,
                    alpha=1,
                    label='_Background')

        # Check if the background is already registered
        if '_Background' in self.compound_dict:
            self.apply_params(background[0])
        else:
            self.load_params(background[0])


        #################################
        # grid, axis label, size,legend #
        #################################

        # grid
        ax_data.minorticks_on()
        ax_data.tick_params(top=True, right=True, which='major', direction='in', width=1.5)
        ax_data.tick_params(top=True, right=True, which='minor', direction='in', width=1)

        # define automaticcaly the region to plot
        # invert the axis as represented in XPS plots

        ax_data.set_xlim(diff_meas_sim['B.E.'].max(), diff_meas_sim['B.E.'].min())

        # x and y label for data
        ax_data.set_ylabel(y_labelis, fontsize=15)
        ax_data.set_xlabel("Binding Energy (eV)", fontsize=15)

        # legend
        legend_properties = {'weight': 'bold', 'style': 'italic'}
        ax_data.legend(loc='best', title_fontproperties = legend_properties)

        ####################
        # Residual and STD #
        ####################

        if self.is_residuals.get():

            # Residual plot
            lim = (dftoplot['y'] - dftoplot['Background y']) != 0
            residuals = ax_res.plot(dftoplot['B.E.'],
                        dftoplot['Envelope y'] - dftoplot['y'],
                        c='k', linewidth=2,
                        label="_Residual")

            # Using a fake curve to add the value in the legend
            std = ax_res.plot(dftoplot['B.E.'],
                        dftoplot['Envelope y'] - dftoplot['y'],
                        c='k', linewidth=2,
                        label=f"STD = {self.calc_res_std(dftoplot[lim]):.2f}",
                        alpha = 0)

            # Update the component dict
            if '_Residual' in self.compound_dict:
                self.apply_params(residuals[0])
            else:
                self.load_params(residuals[0])

            # STD is never store in the config file
            self.load_params(std[0])

            # Set xlim
            ax_res.set_xlim(diff_meas_sim['B.E.'].max(), diff_meas_sim['B.E.'].min())

            # Get the range of the y axis
            y_range = (  (dftoplot['Envelope y'] - dftoplot['y']).max() \
                       - (dftoplot['Envelope y'] - dftoplot['y']).min() \
                      ) * 0.6

            # Set ylim
            ax_res.set_ylim((dftoplot['Envelope y'] - dftoplot['y']).min() - y_range,
                            (dftoplot['Envelope y'] - dftoplot['y']).max() + y_range)

            # Ticks and legend
            ax_res.minorticks_on()
            ax_res.tick_params(top=True, right=True, which='major', direction='in', width=1.5)
            ax_res.tick_params(top=True, right=True, which='minor', direction='in', width=1)
            ax_res.legend(loc = "upper left")


    def calc_res_std(self, df):

        """ Compute the std of the envelope regarding the data
         Parameters
        ----------
        side: df
            0 if goes backward and 1 if it goes forward
        Returns
        -------
        res_STD: float
            return the std
        """

        # Compute the difference
        diff = df['Counts'] - df['Envelope']

        # Get the STD
        res_STD = np.sqrt((1 / (df.shape[0])) * np.sum(np.square(diff / np.sqrt(df['Counts']))))

        return res_STD

    def switch(self,side):

        """ Update the current ax plotted
         Parameters
        ----------
        side: int
            0 if goes backward and 1 if it goes forward
        Returns
        -------
        """

        # Set the current axes according to the button pressed and the residuals
        if self.is_residuals.get():
            self.current_ax = (self.current_ax + 4*side - 2) % (self.nb_plots*2)
        else:
            self.current_ax = (self.current_ax + 2*side - 1) % self.nb_plots

        # Update the axes
        self.update_axes()

    def update_axes(self):

        """ Update the axes plotted according to the current axes index """

        # Disable all the axes
        for ax in self.fig.get_axes():
            ax.set_visible(False)

        # Enable the selected axe
        self.fig.get_axes()[self.current_ax].set_visible(True)

        # If residuals are enable plot both axes
        if self.is_residuals.get():
            self.fig.get_axes()[self.current_ax + 1].set_visible(True)

        # Set the title
        self.fig.suptitle(re.split('[\\\\/]',
                          self.all_files[int(self.current_ax / (1 + self.is_residuals.get()))])[-1][:-4],
                          fontsize = 20)

        # Update the canvas
        self.canvas.draw()

    def save_fig(self):

        """ Save all the figues created """

        # Store the current axes to restore at the end
        former_current_axes = self.current_ax

        # Check is there is any axe plot
        if not self.fig.get_axes():
            showerror("No figures", "Please press plot before saving the figures")
            return None

        # For all the plots
        for i in range(self.nb_plots):

            # Update the display with the good axe
            self.current_ax = i*(1+self.is_residuals.get())
            self.update_axes()

            # Store the figure
            self.fig.savefig(self.all_files[i][:-4] + '.png', format= 'png')

        # Restore the former current axe displayed
        self.current_ax = former_current_axes
        self.update_axes()

    def propagate_params(self):
        """ Update the color, shape... of the elements according
        to the modifications done to the displayed axe """

        # Get all the components from the current axes
        comps = self.fig.get_axes()[self.current_ax].get_lines()

        # If enable get the residual comp
        res = self.fig.get_axes()[self.current_ax + 1].get_lines() if self.is_residuals.get() else []

        # Blinker for residuals vs compounds
        is_residual = True

        # Update all the parameter in the compound_dict
        for comp in (comps + res):
            self.load_params(comp)

        # Apply the new params
        for ax in self.fig.get_axes():

            # Get the filled comp if enable
            filled_comp = [child for child in ax.get_children() if isinstance(child, PolyCollection)]
            filled_comp_label = [collec.get_label() for collec in filled_comp]

            for comp in ax.get_lines():

                self.apply_params(comp)

                # If enable change the color of the filled compound
                if self.is_filled.get():
                    indices = [index for index, value in enumerate(filled_comp_label) if value[1:] == comp.get_label()]
                    for i in indices:
                        filled_comp[i].set_facecolor(self.compound_dict[comp.get_label()][4])

            # Remove the old legend
            ax.get_legend().remove()

            # Add the updated legend
            if is_residual and self.is_residuals.get():
                ax.legend(loc = "upper left")
                is_residual = False
            else:
                legend_properties = {'weight': 'bold', 'style': 'italic'}
                ax.legend(loc='best', title_fontproperties = legend_properties)
                is_residual = True
            self.update_axes()

    def load_params(self, orbit, comp_name = None):

        """ Update the color, shape... of the elements according
        to the modifications done to the displayed axe """

        if not comp_name:
            comp_name = orbit.get_label()

        # Create the array in case of
        self.compound_dict[comp_name] = [None]*8

        # Get all the data from the line
        self.compound_dict[comp_name][0] = orbit.get_linestyle()
        self.compound_dict[comp_name][1] = orbit.get_drawstyle()
        self.compound_dict[comp_name][2] = orbit.get_marker()
        self.compound_dict[comp_name][3] = orbit.get_lw()
        self.compound_dict[comp_name][4] = orbit.get_color()
        self.compound_dict[comp_name][5] = orbit.get_ms()
        self.compound_dict[comp_name][6] = orbit.get_mfc()
        self.compound_dict[comp_name][7] = orbit.get_mec()

    def apply_params(self,orbit, comp_name = None):

        """ Update the color, shape... of the elements according
        to the modifications done to the displayed axe """

        if not comp_name:
            comp_name = orbit.get_label()

        # Apply all the data from the dictionnary
        if not comp_name[:3] == 'STD':
            orbit.set_linestyle(self.compound_dict[comp_name][0])
            orbit.set_drawstyle(self.compound_dict[comp_name][1])
            orbit.set_marker(self.compound_dict[comp_name][2])
            orbit.set_lw(self.compound_dict[comp_name][3])
            orbit.set_color(self.compound_dict[comp_name][4])
            orbit.set_ms(self.compound_dict[comp_name][5])
            orbit.set_mfc(self.compound_dict[comp_name][6])
            orbit.set_mec(self.compound_dict[comp_name][7])


    def save_config(self):

        """ Save the config for all orbitals in a txt file with a json format """

        # Ask the file path
        file_path = asksaveasfilename(defaultextension=".txt",
                                      filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        # Remove fake STD orbitals
        dict_without_STD = {key: value for key, value in self.compound_dict.items() if not key.startswith('STD')}

        # Convert dictionnary to a JSON string
        dict_string = json.dumps(dict_without_STD, indent=4)

        if file_path != '':
            # Write the string to a text file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(dict_string)
