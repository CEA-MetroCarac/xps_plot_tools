""" Necessary imports for the display """

import csv
import re
from tkinter import Frame, Button, LabelFrame, Label, StringVar, Entry, Listbox, IntVar, \
    Radiobutton, Checkbutton
from tkinter import RIGHT, LEFT, TOP, BROWSE, END, EXTENDED
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.text as TXT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from xps_plot_tools.toolbar import ExpendedToolbar


class DisplayFrame(Frame):
    """Class representing the frame used to display quantification"""

    def __init__(self, master=None, **kw):

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
        self.master = master

        ################
        # DATA STORAGE #
        ################

        # Quanti
        self.LABEL_SAMPLES = []
        self.LABEL_ORBIT = []
        self.QUANTI = []
        self.REF = []

        # Store Sevral Colors
        self.color_bar = np.append([np.array(plt.colormaps["tab20c"](i * 4)) for i in range(4)],
                                   [np.array([250 / 255, 169 / 255, 17 / 255, 0.90]),
                                    np.array([1, 4 / 255, 43 / 255, 0.9]),
                                    np.array([219 / 255, 9 / 255, 199 / 255, 0.9]),
                                    np.array([99 / 255, 44 / 255, 15 / 255, 0.85]),
                                    np.array([144 / 255, 121 / 255, 4 / 255, 0.9])], axis=0)

        ################
        # DISPLAY FRAME #
        ################

        # Create and display the frame
        self.display_FRAME = LabelFrame(self, text="Display", height=20, width=20)
        self.display_FRAME.pack(side=RIGHT, padx=5, pady=2)

        # Create the figure and link it to the canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_FRAME)

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
        self.config_FRAME.pack(side=LEFT)

        ##############
        # PATH FRAME #
        ##############

        # Frame
        self.path_FRAME = LabelFrame(self.config_FRAME, borderwidth=2, text="Chose the files")
        self.path_FRAME.pack(side=TOP, padx=5, pady=5)

        # Side labels
        Label(self.path_FRAME, text="Casa file").grid(row=1, column=1)
        Label(self.path_FRAME, text="RSF file").grid(row=2, column=1)

        # Variable for each path
        self.data_path = StringVar()
        self.rsf_path = StringVar()

        # Entry for each path
        self.data_ENTRY = Entry(self.path_FRAME, textvariable=self.data_path, width=30)
        self.rsf_ENTRY = Entry(self.path_FRAME, textvariable=self.rsf_path, width=30)
        self.data_ENTRY.grid(row=1, column=2, padx=5)
        self.rsf_ENTRY.grid(row=2, column=2, padx=5)

        # Browse button for each path
        Button(master=self.path_FRAME,
               height=1,
               width=1,
               text="...",
               command=lambda: self.ask_path('data')) \
            .grid(row=1, column=3, padx=5, pady=1)

        Button(master=self.path_FRAME,
               height=1,
               width=1,
               text="...",
               command=lambda: self.ask_path('rsf')) \
            .grid(row=2, column=3, padx=5, pady=1)

        ################
        # SELECT FRAME #
        ################

        # Load frame
        self.select_FRAME = LabelFrame(self.config_FRAME, borderwidth=2, text="Select data")
        self.select_FRAME.pack(side=TOP, padx=5, pady=2)

        # Frame for the load button
        self.load_FRAME = Frame(self.select_FRAME)
        self.load_FRAME.pack(side=TOP, padx=5, pady=5)

        # Load button
        Button(master=self.load_FRAME,
               height=1,
               width=10,
               text="Load files",
               command=self.load_data) \
            .pack(side=TOP)

        # Selection frame
        self.select_FRAME = Frame(self.select_FRAME)
        self.select_FRAME.pack(side=TOP, padx=5, pady=5)

        # Labels for the lists
        Label(self.select_FRAME, text="Samples").grid(row=1, column=1)
        Label(self.select_FRAME, text="Atomic orbitals").grid(row=1, column=2)

        # List of samples and orbits
        self.sample_LIST = Listbox(master=self.select_FRAME,
                                   selectmode=BROWSE,
                                   height=15,
                                   exportselection=False)

        self.orbit_LIST = Listbox(master=self.select_FRAME,
                                  selectmode=EXTENDED,
                                  height=15,
                                  exportselection=False)

        self.sample_LIST.bind("<<ListboxSelect>>", lambda event: self.update_orbit_list_and_ref())
        self.sample_LIST.grid(row=2, column=1, padx=5, pady=1)
        self.orbit_LIST.grid(row=2, column=2, padx=5, pady=1)

        # Calcul frame
        self.calc_FRAME = LabelFrame(master=self.config_FRAME, text='Select display mode')
        self.calc_FRAME.pack(side=TOP, padx=5, pady=5)

        # Variable for checkbox and function
        self.function_var = StringVar()
        self.calc_type = IntVar()
        self.is_curve = IntVar()
        self.is_label_data = IntVar()
        self.is_grid = IntVar()
        self.is_error = IntVar()
        self.xtick_var = StringVar()

        # Component for relative quantification
        Radiobutton(master=self.calc_FRAME,
                    text='Relative',
                    variable=self.calc_type,
                    value=1,
                    command=self.update_entries) \
            .pack(side=TOP)

        # Component for absolute quantification
        Radiobutton(master=self.calc_FRAME,
                    text='Absolute',
                    variable=self.calc_type,
                    value=0,
                    command=self.update_entries) \
            .pack(side=TOP)

        self.ref_COMBOBOX = Combobox(master=self.calc_FRAME, width=15)
        self.ref_COMBOBOX.pack(side=TOP)

        # Component for the function part
        Radiobutton(master=self.calc_FRAME,
                    text='Function',
                    variable=self.calc_type,
                    value=2,
                    command=self.update_entries) \
            .pack(side=TOP)

        self.function_ENTRY = Entry(master=self.calc_FRAME,
                                    textvariable=self.function_var,
                                    width=30,
                                    state='disabled')
        self.function_ENTRY.pack(side=TOP, padx=3, pady=3)

        # Frame for the checkboxes
        self.CB_FRAME = Frame(self.calc_FRAME)
        self.CB_FRAME.pack(side=TOP, padx=3, pady=3)

        self.function_CB = Checkbutton(master=self.CB_FRAME,
                                       text='Curves',
                                       variable=self.is_curve,
                                       onvalue=1,
                                       offvalue=0,
                                       command=self.update_entries)

        self.label_CB = Checkbutton(master=self.CB_FRAME,
                                    text='Label Data',
                                    variable=self.is_label_data,
                                    onvalue=1,
                                    offvalue=0)

        self.grid_CB = Checkbutton(master=self.CB_FRAME,
                                   text='Grid',
                                   variable=self.is_grid,
                                   onvalue=1,
                                   offvalue=0)

        self.error_CB = Checkbutton(master=self.CB_FRAME,
                                    text='Error Bars',
                                    variable=self.is_error,
                                    onvalue=1,
                                    offvalue=0)

        self.function_CB.grid(row=1, column=1, padx=3, pady=3)
        self.label_CB.grid(row=2, column=1, padx=3, pady=3)
        self.grid_CB.grid(row=1, column=2, padx=3, pady=3)
        self.error_CB.grid(row=2, column=2, padx=3, pady=3)

        self.xtick_ENTRY = Entry(master=self.calc_FRAME,
                                 textvariable=self.xtick_var,
                                 width=30,
                                 state='disabled')

        self.xtick_ENTRY.pack(side=TOP, padx=3, pady=3)

        # Plot Button
        Button(master=self.config_FRAME,
               height=1,
               width=10,
               text="Plot",
               command=self.plot_figure) \
            .pack(side=TOP)

    def update_entries(self):
        """
    Enable or disable the function entry

    Parameters
    ----------

    Returns
    -------

    """
        # Enable or disable writting in the function entry, the combobox and the list selectmode
        if self.calc_type.get() == 0:
            self.function_ENTRY.config(state='readonly')
            self.ref_COMBOBOX.configure(state='normal')
            self.sample_LIST.configure(selectmode='browse')
            self.function_CB.config(state='disable')
            self.grid_CB.config(state='disable')
            self.label_CB.config(state='disable')
            self.xtick_ENTRY.config(state='readonly')

        elif self.calc_type.get() == 1:
            self.function_ENTRY.config(state='readonly')
            self.ref_COMBOBOX.configure(state='disabled')
            self.sample_LIST.configure(selectmode='extended')
            self.function_CB.config(state='disable')
            self.grid_CB.config(state='disable')
            self.label_CB.config(state='disable')
            self.xtick_ENTRY.config(state='readonly')
        else:
            self.function_ENTRY.config(state='normal')
            self.ref_COMBOBOX.configure(state='disabled')
            self.sample_LIST.configure(selectmode='extended')
            self.function_CB.config(state='normal')

            # If the curve display is enable for the function, enable the x tick modifier
            if self.is_curve.get():
                self.xtick_ENTRY.config(state='normal')
                self.grid_CB.config(state='normal')
                self.label_CB.config(state='disabled')
            else:
                self.xtick_ENTRY.config(state='readonly')
                self.label_CB.config(state='normal')

        # Reset the sample list selection and update the values in the references and orbitals
        if self.QUANTI:
            self.update_orbit_list_and_ref()

    def ask_path(self, val):

        """
    Open a windows explorer to get the location of the file containing
    the required data and store it into the associtated entry

    Parameters
    ----------
    val: string
        'data' or 'rsf' according to which file you refer

    Returns
    -------

    """

        # Open the window
        filepath = askopenfilename(title="Select " + val + " file ",
                                   filetypes=[('txt files', '.txt'), ('all files', '.*')])

        # Update the variable
        if val == 'data':
            self.data_path.set(filepath)
        else:
            self.rsf_path.set(filepath)

    def load_data(self):

        """
   Load the data (rsf and orbital area) from the two files
   previously selected and perform the quantification

    Parameters
    ----------

    Returns
    -------

    """

        # Check if the path is valid
        if self.data_ENTRY.get() == '' or self.rsf_ENTRY.get() == '':
            showerror('No path detected', 'Please select a path for the data file and the RSF file')
            return None

        # Temporary data storage
        VALUE_TAB = []
        SPECTRUMS = []
        RSF = {}

        # Reset all previous import
        self.LABEL_SAMPLES = []
        self.LABEL_ORBIT = []
        self.QUANTI = []
        self.REF = []
        self.ref_COMBOBOX.set('')

        # Reset the lists
        self.sample_LIST.delete(0, self.sample_LIST.size())
        self.orbit_LIST.delete(0, self.orbit_LIST.size())

        # Read data file and extract each orbitals of each sample
        with open(self.data_ENTRY.get(), newline='\n', encoding='ascii',
                  errors='ignore') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t')
            t_off = 0
            buffer = []
            for row in spamreader:
                if t_off >= 3:  # We don't care of the first 3 lines of the file
                    if row == []:  # End of the file we stop reading
                        VALUE_TAB.append(buffer)
                        break
                    elif row[0] == '':  # Still in the same sample
                        buffer.append([row[k + 1] for k in range(6)])
                    else:  # Sample changement
                        VALUE_TAB.append(buffer)
                        buffer = []
                        buffer.append([row[k + 1] for k in range(6)])
                        self.LABEL_SAMPLES.append(row[0])
                t_off += 1
        csvfile.close()

        # Extract RSF from the rsf file
        with open(self.rsf_ENTRY.get(), newline='', encoding='ascii', errors='ignore') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            t_off = 0
            for row in spamreader:
                if t_off >= 11:  # We don't care of the first lines of the file
                    if t_off == 11:  # Line of the orbital name
                        orbit = [row[i] for i in range(len(row)) if row[i] != '']
                        t_off += 1
                    elif t_off == 12:  # Line of the rsf
                        rsf = [row[i] for i in range(len(row)) if row[i] != '']
                        t_off += 1
                    elif t_off == 13:  # Line of the corrected rsf
                        rsf_corrected = [row[i] for i in range(len(row)) if row[i] != '']
                        t_off += 1
                    else:  # We stop reading
                        break
                else:
                    t_off += 1
        csvfile.close()

        # Put RSF value in a dictionary
        for orb, r, r_c in zip(orbit, rsf, rsf_corrected):
            RSF[orb] = [float(r), float(r_c)]

        # Format each orbital data => Combine the compounds with the same
        # denomination and put everything in a dictionary
        # Also check that all Orbitals have a RSF
        temp_bool = True
        missing_orb = []
        for sample in VALUE_TAB[1:]:  # The first item is empty
            dict_orbit = {}
            for orbit in sample:

                # Get the name of the orbital
                prefix = ''.join(orbit[0].split()[:2])
                name = prefix + orbit[0][len(prefix) + 1:]
                if prefix not in RSF:
                    missing_orb.append(prefix)
                    temp_bool = False

                # Convert data
                raw_area = float(orbit[5])
                energy = float(orbit[1])

                # Add the value to the dictionary
                if name in dict_orbit:  # If the orbit is already register take the mean
                    e, a, i = dict_orbit[name]
                    dict_orbit[name] = [(e * i + energy) / (i + 1), a + raw_area, i + 1]
                else:
                    dict_orbit[name] = [energy, raw_area, 1]

            SPECTRUMS.append(dict_orbit)

        # Check all the RSF are present
        if not temp_bool:
            showerror('RSF error',
                      'Please make sure that a rsf is specified for all orbitals analyzed '
                      + str(set(missing_orb)))
            return None

        # Calculate all the quatifications and add the sample to the list
        for i, spect in enumerate(SPECTRUMS):

            # Add the sample to the list:
            self.sample_LIST.insert(END, self.LABEL_SAMPLES[i])

            # For each orbital, compute the quantification
            dict_buffer = {}
            for orbit in spect.items():
                i_corr = orbit[1][1] / RSF[orbit[0].split()[0]][1]
                dict_buffer[orbit[0]] = i_corr
            self.QUANTI.append(dict_buffer)

    def plot_absolute(self):

        """
        Plot the absolute quantification according the orbits selected
        Parameters
        ----------
        
        Returns
        -------

        """

        # Get the number of compounds to plot
        nb_compounds = len(self.orbit_LIST.curselection())

        infos = {}  # [bottom, number of orbital, color]
        color_max = 0  # keep track of the colors used
        tempo = False
        dict_displayed = {}

        # Init total
        total = 0

        # Wait fot the combox to update
        self.master.update_idletasks()

        # Compute the total
        for orbit in self.LABEL_ORBIT:
            element = re.match(r'([A-Za-z]+)(\d.*)', orbit.split()[0]).group(1)
            if element in self.REF:
                if orbit.split()[0] in self.ref_COMBOBOX.get():
                    total += self.QUANTI[self.sample_LIST.curselection()[0]][orbit]
            else:
                total += self.QUANTI[self.sample_LIST.curselection()[0]][orbit]

        # Compute the quantification
        for j, label in enumerate(self.LABEL_ORBIT):

            # Check if the orbit is selected to be plotted
            is_selected = (j in self.orbit_LIST.curselection() or nb_compounds == 0)

            # Check if the orbit is a potential reference
            is_not_a_ref = not re.match(r'([A-Za-z]+)(\d.*)', label.split()[0]).group(1) in self.REF

            # Check if the orbit is in the references selected
            is_in_selected_ref = label.split()[0] in self.ref_COMBOBOX.get()

            if is_selected and (is_not_a_ref or is_in_selected_ref):
                dict_displayed[label] = round(
                    self.QUANTI[self.sample_LIST.curselection()[0]][label] / total * 100, 1)

        # Get the orbit labels, number and position
        labels = list(set(orbit.split()[0] for orbit, _ in dict_displayed.items()))
        nb_orbits = len(labels)
        position = [j / (nb_orbits + 1) for j in range(nb_orbits)]

        # Sort the dictionnary to plot in the good order
        sorted_dict = sorted(dict_displayed.items(),
                             key=lambda x: [x[0][:len(x[0].split()[0])], x[1]], reverse=True)

        # Check if the dict is not empty
        if sorted_dict == []:
            showerror('No valide orbitals', "Please select relevent orbitals")
            return None

        for orbit, percent in sorted_dict:
            #  Get the orbital prefix
            prefix = orbit.split()[0]

            # Register the orbital
            if prefix not in infos:
                infos[prefix] = [0, 0, color_max]
                color_max += 1

            # Display the total label above the bar (disable if it's the first bar)
            if infos[prefix][0] == 0 and tempo:
                self.ax.bar_label(orbit_bar, fmt='{:.1f}', padding=5, fontweight='bold',
                                  fontsize='12')
                if self.is_error.get():
                    self.ax.errorbar(orbit_bar[-1].get_x() + orbit_bar[-1].get_width() / 2,
                                     orbit_bar[0].get_y() + orbit_bar[-1].get_height(),
                                     yerr=0.1 * (orbit_bar[0].get_y() + orbit_bar[-1].get_height()),
                                     fmt='none',
                                     ecolor='black',
                                     capsize=5)

            # Display the bar
            orbit_bar = self.ax.bar(position[(len(infos) - 1)],
                                    percent,
                                    width=1 / (nb_orbits + 1),
                                    label=[orbit], bottom=infos[prefix][0],
                                    color=self.color_bar[infos[prefix][2]] * np.array(
                                        [1, 1, 1, (3 / 4) ** infos[prefix][1]]))

            # Update the info dictionary
            infos[prefix] = [infos[prefix][0] + percent, infos[prefix][1] + 1, infos[prefix][2]]

            # Enable the labeling
            tempo = True

            # Ajust the font regarding the value
            if percent > 1.5:
                label = orbit[len(prefix) + 1:] if len(orbit[len(prefix) + 1:]) > 0 else ""
                self.ax.bar_label(orbit_bar,
                                  label_type='center',
                                  fontsize=self.get_top_label_size(1 / (nb_orbits + 1), label, 1),
                                  labels=[label])

        # For the last one put the top label
        self.ax.bar_label(orbit_bar,
                          fmt='{:.1f}',
                          padding=5,
                          fontweight='bold',
                          fontsize=12)

        # Place the error bar if needed
        if self.is_error.get():
            self.ax.errorbar(orbit_bar[0].get_x() + orbit_bar[0].get_width() / 2,
                             orbit_bar[0].get_height(),
                             yerr=0.1 * orbit_bar[0].get_height(),
                             fmt='none',
                             ecolor='black',
                             capsize=5)

        # Set size, title and global label
        self.ax.set_ylabel('Percentage (%)')
        self.ax.set_ylim(0, 5 + max(data[0] for _, data in infos.items()))
        self.ax.set_title(self.LABEL_SAMPLES[self.sample_LIST.curselection()[0]])
        self.ax.set_xticks(position)
        self.ax.set_xticklabels(sorted(labels, reverse=True), fontweight='bold')

    def plot_relative(self):

        """
        Plot the relative quantification according the samples and orbits selected
        Parameters
        ----------
        
        Returns
        -------

        """

        # Determine the selection size
        nb_sample = len(self.sample_LIST.curselection())
        nb_compounds = len(self.orbit_LIST.curselection())

        # Check if at least one orbit is selected
        if nb_compounds == 0:
            showerror('No orbit', 'Please select several orbitals')
            return None

        # Get the number of different orbitals et create the different positions
        nb_orbits = len(
            list(set([self.LABEL_ORBIT[i].split()[0] for i in self.orbit_LIST.curselection()])))
        position = [i + j / (nb_orbits + 1) for i in range(nb_sample) for j in range(nb_orbits)]

        # Init maximum
        maxi = 0

        # For each sample selected
        for i in range(nb_sample):

            # Compute the sum of all orbitals selected and the quantification
            dict_displayed = {}
            total = sum([self.QUANTI[self.sample_LIST.curselection()[i]][self.LABEL_ORBIT[j]]
                         for j in self.orbit_LIST.curselection()])
            for j in self.orbit_LIST.curselection():
                dict_displayed[self.LABEL_ORBIT[j]] = \
                    round(self.QUANTI[self.sample_LIST.curselection()[i]][
                              self.LABEL_ORBIT[j]] / total * 100, 1)

            infos = {}  # [bottom, number of orbital, color]
            color_max = 0  # keep track of the colors used

            # Init the temporisation for the first bar
            tempo = False

            # Sort the dictionnary to plot in the good order
            sorted_dict = sorted(dict_displayed.items(),
                                 key=lambda x: [x[0][:len(x[0].split()[0])], x[1]], reverse=True)

            for orbit, percent in sorted_dict:
                #  Get the orbital prefix
                prefix = orbit.split()[0]

                # Register the orbital
                if prefix not in infos:
                    # Display the total label above the bar (disable if it's the first bar)
                    if tempo:
                        lab = [txt for txt, _ in infos.items()][-1]

                        percentage_font_size = self.get_top_label_size(orbit_bar[0].get_width(),
                                                                       str(round(
                                                                           orbit_bar[0].get_height()
                                                                           + orbit_bar[0].get_y(),
                                                                           1)),
                                                                       nb_sample)

                        name_font_size = self.get_top_label_size(orbit_bar[0].get_width(),
                                                                 lab,
                                                                 nb_sample)
                        # The percentage
                        self.ax.bar_label(orbit_bar,
                                          labels=[str(round(
                                              orbit_bar[0].get_height() + orbit_bar[0].get_y(),
                                              1))],
                                          padding=2,
                                          fontsize=percentage_font_size)

                        # The name of the orbital
                        self.ax.bar_label(orbit_bar,
                                          labels=[lab],
                                          padding=16,
                                          fontweight='bold',
                                          fontsize=name_font_size)

                        if self.is_error.get():
                            self.ax.errorbar(orbit_bar[-1].get_x() + orbit_bar[-1].get_width() / 2,
                                             orbit_bar[0].get_y() + orbit_bar[-1].get_height(),
                                             yerr=0.1 * (orbit_bar[0].get_y() + orbit_bar[
                                                 -1].get_height()),
                                             fmt='none',
                                             ecolor='black',
                                             capsize=5)

                    # Update the color and info handler
                    infos[prefix] = [0, 0, color_max]
                    color_max += 1

                # Display the bar
                orbit_bar = self.ax.bar(position[(len(infos) - 1) + i * nb_orbits],
                                        percent,
                                        width=1 / (nb_orbits + 1),
                                        label=[orbit + " - " + self.LABEL_SAMPLES[
                                            self.sample_LIST.curselection()[i]]],
                                        bottom=infos[prefix][0],
                                        color=self.color_bar[infos[prefix][2]] * np.array(
                                            [1, 1, 1, (3 / 4) ** infos[prefix][1]]))

                # Update the info dictionary
                infos[prefix] = [infos[prefix][0] + percent, infos[prefix][1] + 1, infos[prefix][2]]

                # Enable the labeling
                tempo = True

                # Ajust the font regarding the value
                if percent > 1.5:
                    label = orbit[len(prefix) + 1:] if len(orbit[len(prefix) + 1:]) > 0 else ""
                    self.ax.bar_label(orbit_bar,
                                      label_type='center',
                                      fontsize=self.get_top_label_size(orbit_bar[0].get_width(),
                                                                       label, nb_sample),
                                      labels=[label])

            # For the last one put the top label

            # The percentage
            self.ax.bar_label(orbit_bar,
                              labels=[
                                  str(round(orbit_bar[0].get_height() + orbit_bar[0].get_y(), 1))],
                              padding=2,
                              fontsize=self.get_top_label_size(orbit_bar[0].get_width(),
                                                               str(round(orbit_bar[0].get_height()
                                                                         + orbit_bar[0].get_y(),
                                                                         1)),
                                                               nb_sample))
            # The name of the orbital
            self.ax.bar_label(orbit_bar,
                              labels=[prefix],
                              padding=16,
                              fontweight='bold',
                              fontsize=self.get_top_label_size(orbit_bar[0].get_width(),
                                                               prefix,
                                                               nb_sample))
            if self.is_error.get():
                self.ax.errorbar(orbit_bar[-1].get_x() + orbit_bar[-1].get_width() / 2,
                                 orbit_bar[0].get_y() + orbit_bar[-1].get_height(),
                                 yerr=0.1 * (orbit_bar[0].get_y() + orbit_bar[-1].get_height()),
                                 fmt='none',
                                 ecolor='black',
                                 capsize=5)

            # Update maxi
            maxi = max(max(data[0] for _, data in infos.items()), maxi)

        # Set size, title and global label
        self.ax.set_ylabel('Percentage (%)')
        self.ax.set_ylim(0, 9 + maxi)

        # Put x_ticks
        self.ax.set_xticks([i + 0.5 / (nb_orbits + 1) * (nb_orbits - 1) for i in range(nb_sample)])
        self.ax.set_xticklabels([self.LABEL_SAMPLES[self.sample_LIST.curselection()[i]]
                                 for i in range(nb_sample)],
                                rotation=45,
                                fontsize=13,
                                fontweight='bold')

    def plot_function(self):

        """
        Plot the result of the function for the different samples
        Parameters
        ----------
        
        Returns
        -------

        """

        nb_sample = len(self.sample_LIST.curselection())

        # Split the function around each parameter
        spliter = re.findall(r'\[[^\]]*\]|[^[]+', self.function_var.get()
                             .replace('exp', 'np.exp')
                             .replace('log', 'np.log'))

        # If the function is not empty
        if spliter != []:

            # Get the results of the function
            results = [self.interpreter(spliter, i) for i in self.sample_LIST.curselection()]

            # If the curve option is not selected
            if self.is_curve.get() == 0:
                # X position
                position = list(range(nb_sample))

                # Get the sample labels associated
                xticks = [self.LABEL_SAMPLES[i] for i in self.sample_LIST.curselection()]

                # Plot the figure
                bars = self.ax.bar(position, results, label=xticks)

                # Plot the bar label if needed
                if self.is_label_data.get():
                    # Compute the font size
                    label_size = self.get_top_label_size(bars[0].get_width(),
                                                         str(round(
                                                             bars[0].get_height() + bars[0].get_y(),
                                                             1)),
                                                         len(bars))
                    # Plot the label
                    self.ax.bar_label(bars,
                                      labels=[str(round(e, 1)) for e in results],
                                      padding=2,
                                      fontweight='bold',
                                      fontsize=label_size,
                                      label_type='center' if self.is_error.get() else 'edge')

                # Plot the bar label if needed
                if self.is_error.get():
                    for b in bars:
                        self.ax.errorbar(b.get_x() + b.get_width() / 2,
                                         b.get_y() + b.get_height(),
                                         yerr=0.1 * (b.get_y() + b.get_height()),
                                         fmt='none',
                                         ecolor='black',
                                         capsize=5)

                # Set the x_ticks position and labels
                self.ax.set_xticks(position)
                self.ax.set_xticklabels(xticks, rotation=45, fontsize=13, fontweight='bold')

            else:

                # Get the modification instruction
                xtick_mod = self.xtick_var.get()

                # Check the validity of the instruction
                if xtick_mod is None or xtick_mod == "":
                    showerror('Syntax error', "Please enter a valid formula for x axis")
                else:
                    # Get the labels from the sample list and replace "-"" and "_" by " "
                    previous_labels = [
                        self.LABEL_SAMPLES[i].replace('_', ' ').replace('-', ' ').split()
                        for i in self.sample_LIST.curselection()]

                    # Replace each [%d] by its value in the previous label
                    expressions = [re.sub(r'\[(\d+)\]',
                                          lambda match: refs[int(match.group(1))],
                                          xtick_mod.replace('exp', 'np.exp').replace('log',
                                                                                     'np.log'))
                                   for refs in previous_labels]

                    # Evaluate the expression for each x_tick
                    xticks = [float(eval(expr)) for expr in expressions]

                    # Plot the result and add the grid
                    self.ax.plot(xticks, results, label='Plot 1')

                    # Plot the grid if enable
                    if self.is_grid.get():
                        self.ax.grid()
        else:
            showerror('No function', 'Please write a valid function')

    def plot_figure(self):

        """
        Plot the different quantities according to the selection and display mode
        Parameters
        ----------
        
        Returns
        -------

        """
        # Clear the previous figure
        self.ax.clear()

        if len(self.sample_LIST.curselection()) == 0:  # No selection
            showerror('No selection', 'Please select a sample')

        # Display the corresponding graph

        if self.calc_type.get() == 2:  # Function
            self.plot_function()

        elif self.calc_type.get() == 1:  # Relative
            self.plot_relative()

        else:  # Absolute
            self.plot_absolute()

        # Update the canvas
        self.canvas.draw()

    def interpreter(self, cacl, index_sample):

        """
        Return the evalutation of the function cacl replacing the variable by the index_sample
        experimental result

        Parameters
        ----------
        cacl: list of string
            string of the function splitted around the different variables
        index_sample: int
            Index of the sample to use to perform the calculation

        Returns
        -------
         : foat
            Result of the calculation of the function 

        """
        # Store the result string splited
        result = []

        # For each items
        for exp in cacl:

            # If it's a paramter
            if exp[0] == '[':

                # If it's an adder
                if ':' in exp:

                    # Get the two indices
                    n1, n2 = exp[1:-1].split(':')

                    # Get all the values
                    values = [str(self.QUANTI[index_sample][self.LABEL_ORBIT[k]]) for k in
                              range(int(n1), int(n2) + 1)]

                    # Add the sum of the parameter's value to the string
                    result.append('(' + '+'.join(values) + ')')
                else:
                    # Add total value of the string in case of an empty bracket
                    if exp == '[]':
                        result.append('('
                                      + '+'.join(
                            [str(self.QUANTI[index_sample][orb]) for orb in self.LABEL_ORBIT])
                                      + ')')
                    else:

                        # Split every orbitals
                        orbs = exp[1:-1].split(';')

                        # Add the parameter's value to the string
                        result.append('('
                                      + '+'.join(
                            [str(self.QUANTI[index_sample][self.LABEL_ORBIT[int(orb)]]) for orb in
                             orbs])
                                      + ')')
            else:
                # In other cases just copy the string
                result.append(exp)

        # return the evalutation of the string
        return eval(''.join(result))

    def get_top_label_size(self, wid, text, nb_sample):

        """
        Return the size of the label according to the number of bar and the size of text
        Parameters
        ----------
        wid: float
        The width of the bar wich need the label

        text: string
        The text to be displayed

        nb_sample: int
        Number of sample displayed on the same axes

        Returns
        -------
         : int
        Maximum size of the label which fit into the bar
        """
        # Create a array of text with different font sizes
        text_samples = [TXT.Text(x=0, y=0, text=text, fontsize=size, figure=self.fig) for size in
                        range(13)]

        # Compute the width of the text
        text_size = [text.get_window_extent().width / 500 for text in text_samples]

        # Return the maximum size which makes the label smaller than the bar
        return max(size * (int(text_size[size]) < (wid / nb_sample)) for size in range(13))

    def update_orbit_list_and_ref(self):

        """
        Update the list of orbits and references according to the selected mode and the sample
        Parameters
        ----------
    
        Returns
        -------

        """

        # Reset the list and labels of orbits
        self.orbit_LIST.delete(0, self.orbit_LIST.size())
        self.LABEL_ORBIT = []

        # If we are in absolute mode
        if self.calc_type.get() == 0 and len(self.sample_LIST.curselection()):

            # Add all the orbitals to the list and check the different references
            orbit_dict_buffer = {}
            for orbit, _ in self.QUANTI[self.sample_LIST.curselection()[0]].items():
                # Assess if the orbital has the good format
                try:
                    element = re.match(r'([A-Za-z]+)(\d.*)', orbit.split()[0]).group(1)
                    # Add to the list
                    self.orbit_LIST.insert(END, orbit + ' [' + str(self.orbit_LIST.size()) + ']')
                    self.LABEL_ORBIT.append(orbit)

                    # Extract the element and add the orbital to a dict structure
                    if element in orbit_dict_buffer:
                        orbit_dict_buffer[element].add(orbit.split()[0])
                    else:
                        orbit_dict_buffer[element] = {orbit.split()[0]}
                except AttributeError:
                    pass

            # Remove element if there is only one orbit
            for elt, orbits in orbit_dict_buffer.items():
                orbit_dict_buffer[elt] = sorted(list(orbits)) if len(orbits) > 1 else []

            # Update references
            self.REF = [elt for elt, orbits in orbit_dict_buffer.items() if len(orbits) > 1]
            if len(self.REF) >= 1:
                self.ref_COMBOBOX['values'] = list(
                    product(*[orbits for _, orbits in orbit_dict_buffer.items()
                              if orbits != []]))
            else:
                self.ref_COMBOBOX['values'] = ['Default']
            self.ref_COMBOBOX.current(0)

        else:

            # Get the different orbits of all samples
            orbit_list = {orbit
                          for samples in [self.QUANTI[i] for i in self.sample_LIST.curselection()]
                          for orbit, _ in samples.items()}

            # Get the selection
            quanti_selected = [self.QUANTI[i] for i in self.sample_LIST.curselection()]

            # Add orbit to the list only if it's in all samples
            for orbit in sorted(orbit_list, reverse=True):
                if not (sum(not (orbit in sample_orbit)
                            for sample_orbit in [[orb for orb, _ in samples.items()]
                                                 for samples in quanti_selected])):
                    self.orbit_LIST.insert(END, orbit + ' [' + str(self.orbit_LIST.size()) + ']')
                    self.LABEL_ORBIT.append(orbit)

            # Reset the combobox entry
            self.ref_COMBOBOX['values'] = ['Default']
            self.ref_COMBOBOX.current(0)


if __name__ == "__main__":
    pass
