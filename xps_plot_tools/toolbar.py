"""Necessary imports for the toolbar"""

import re
from tkinter import Tk, Frame, TOP, Label, LEFT, Button, Entry, RIGHT, DISABLED, NORMAL, W
from tkinter.ttk import Combobox, Notebook
from tkinter.messagebox import showerror
from tkinter.colorchooser import askcolor
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.patches import Rectangle
from matplotlib.pyplot import Axes
import matplotlib.colors as mcolors
from matplotlib import ticker

class ExpendedToolbar(NavigationToolbar2Tk):
    """Extension of the tkinter matplotlib toolbar"""

    def __init__(self, canvas, parent, fig):

        # List of all the buttons in the toolbar
        self.toolitems = (
            ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
            ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
            ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),

            # Pipe display
            (None, None, None, None),
            ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),

            # new button in toolbar
            ("Customize", "Edit axis, curve and image parameters", "subplots", "edit_parameters"),

            # Pipe display
            (None, None, None, None),
            ('Subplots', 'Ajust borders', 'subplots', 'configure_subplots'),
            ('Save', 'Save the current figure', 'filesave', 'save_figure'),
        )
        super().__init__(canvas, parent)

        # Get the axes and the canvas to have access in the class
        self.fig = fig
        self.ax = self.fig.get_axes()
        self.canvas = canvas

    def edit_parameters(self):
        """
        Callback funtion for the new button

        Parameters
        ----------

        Returns
        -------

        """
        # Create and display the edit graph window
        if isinstance(self.ax,Axes) :
            EditGraph(self.fig, self.canvas)
        else:
            SelectAxes(self.fig, self.canvas)

class SelectAxes(Tk):
    """ Class enableling the user to chose which axes to consider if there are severals axes"""
    def __init__(self, fig, canvas):

        """
        Initialize the window, place the elements

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
        self.title('Select Axes')

        # Set the dimensions of the main window
        self.geometry("200x50")

        # Store the matplotlib variable
        self.ax = fig.get_axes()
        self.canvas = canvas

        # Main frame
        self.main_Frame = Frame(self)
        self.main_Frame.pack(side = TOP)

        # Element fo the window
        Label(master = self.main_Frame,
              text = 'Select axes :',
              font = ('Arial', 10, 'bold'),
              anchor = "w", width = 10)\
              .grid(row = 1, column=1)

        self.axes_CB = Combobox(self.main_Frame, width= 13, justify = LEFT)
        self.axes_CB.grid(row = 1, column=2)
        self.axes_CB['values'] = [ax for ax in self.ax]

        Button(master = self.main_Frame,
               text = 'Cancel',
               font=('Arial', 10, 'bold'),
               command=self.destroy,
               width = 7)\
               .grid(row=2, column=1, padx= 1)

        Button(master = self.main_Frame,
               text = 'Select',
               font=('Arial', 10, 'bold'),
               command=self.process,
               width = 7)\
               .grid(row=2, column=2, padx= 1)

    def process(self):
        """
        Launch the parameter window and close itself

        Parameters
        ----------

        Returns
        -------
        
        """
        EditGraph(self.ax[self.axes_CB.current()], self.canvas)
        self.destroy()




class EditGraph(Tk):
    """Class representing the parameter window used to modify the graph"""

    def __init__(self, ax, canvas):

        """
        Initialize the edit graph window, place the parameters

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
        self.title('Edit graph')

        # Set the dimensions of the main window
        self.geometry("250x600")

        # Link the figure
        self.ax = ax
        self.canvas = canvas

        ############
        # NoteBook #
        ############

        self.tabs = Notebook(self)
        self.tabs.pack()

        ############
        # Axes TAB #
        ############

        self.axes_tab = Frame(self.tabs)

        # Labels
        ########

        Label(master = self.axes_tab,
              text='Title',
              font=('Arial', 10, 'bold'),
              anchor="w", width = 15)\
            .grid(column=1, row=1, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Title size',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=2, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='X-Axis',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 15)\
            .grid(column=1, row=3, padx= 1, pady = 5)

        Label(master = self.axes_tab,
              text='Min', font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=4, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Max', font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=5, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Label',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=6, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Label size',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=7, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='X-Ticks',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 15)\
            .grid(column=1, row=8, padx= 1, pady = 5)

        Label(master = self.axes_tab,
              text='Modifier X_tick',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=9, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Tick size',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=10, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Tick rotation',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=11, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Y-Axis',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 15)\
            .grid(column=1, row=12, padx= 1, pady = 5)

        Label(master = self.axes_tab,
              text='Min',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=13, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Max',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=14, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Label',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=15, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Label size',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=16, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Y-Ticks',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 15)\
            .grid(column=1, row=17, padx= 1, pady = 5)

        Label(master = self.axes_tab,
              text='Major Locator',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=18, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Minor Locator',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=19, padx= 1, pady = 2)

        Label(master = self.axes_tab,
              text='Tick size',
              font=('Arial', 9),
              anchor="w",
              width = 15)\
            .grid(column=1, row=20, padx= 1, pady = 2)

        # Entries
        #########

        # Main Title

        self.e_title = Entry(self.axes_tab, width=20)
        self.e_title.grid(column=2, row=1, pady = 0, sticky='E')
        self.e_title.insert(0,self.ax.get_title())

        self.e_titlesize = Entry(self.axes_tab, width=20)
        self.e_titlesize.grid(column=2, row=2, pady = 0, sticky='E')
        self.e_titlesize.insert(0,self.ax.title.get_fontsize())

        # X AXIS

        self.e_xmax = Entry(self.axes_tab, width=20)
        self.e_xmax.grid(column=2, row=4, sticky='E')
        self.e_xmax.insert(0,str(self.ax.get_xlim()[0]))

        self.e_xmin = Entry(self.axes_tab, width=20)
        self.e_xmin.grid(column=2, row=5, sticky='E')
        self.e_xmin.insert(0,str(self.ax.get_xlim()[1]))

        self.e_xlabel = Entry(self.axes_tab, width=20)
        self.e_xlabel.grid(column=2, row=6, sticky='E')
        self.e_xlabel.insert(0,self.ax.get_xlabel())

        self.e_xlabelsize = Entry(self.axes_tab, width=20)
        self.e_xlabelsize.grid(column=2, row=7, sticky='E')
        self.e_xlabelsize.insert(0,self.ax.xaxis.label.get_fontsize())

        self.e_modifier = Entry(self.axes_tab, width=20)
        self.e_modifier.grid(column=2, row=9, sticky='E')
        self.e_modifier.insert(0,'')

        self.e_xtick_size = Entry(self.axes_tab, width=20)
        self.e_xtick_size.grid(column=2, row=10, sticky='E')
        self.e_xtick_size.insert(0,str(self.ax.get_xticklabels()[0].get_fontsize()))

        self.e_xtick_rotation = Entry(self.axes_tab, width=20)
        self.e_xtick_rotation.grid(column=2, row=11, sticky='E')
        self.e_xtick_rotation.insert(0,str(self.ax.get_xticklabels()[0].get_rotation()))

        # Y AXIS

        self.e_ymax = Entry(self.axes_tab, width=20)
        self.e_ymax.grid(column=2, row=13, sticky='E')
        self.e_ymax.insert(0,str(self.ax.get_ylim()[0]))

        self.e_ymin = Entry(self.axes_tab, width=20)
        self.e_ymin.grid(column=2, row=14, sticky='E')
        self.e_ymin.insert(0,str(self.ax.get_ylim()[1]))

        self.e_ylabel = Entry(self.axes_tab, width=20)
        self.e_ylabel.grid(column=2, row=15, sticky='E')
        self.e_ylabel.insert(0,self.ax.get_ylabel())

        self.e_ylabelsize = Entry(self.axes_tab, width=20)
        self.e_ylabelsize.grid(column=2, row=16, sticky='E')
        self.e_ylabelsize.insert(0,self.ax.yaxis.label.get_fontsize())

        self.e_major_loc = Entry(self.axes_tab, width=20)
        self.e_major_loc.grid(column=2, row=18, sticky='E')
        self.e_major_loc.insert(0,str(self.ax.yaxis.get_major_locator()()[1]))

        self.e_minor_loc = Entry(self.axes_tab, width=20)
        self.e_minor_loc.grid(column=2, row=19, sticky='E')

        # Handle the case when the minor locator is not used
        try:
            self.e_minor_loc.insert(0,str(self.ax.yaxis.get_minor_locator()()[1]))
        except IndexError:
            pass

        self.e_ytick_size = Entry(self.axes_tab, width=20)
        self.e_ytick_size.grid(column=2, row=20, sticky='E')
        self.e_ytick_size.insert(0,str(self.ax.yaxis.get_major_ticks()[0].label1.get_fontsize()))

        # Buttons
        Button(master = self.axes_tab,
               text = 'Close',
               font=('Arial', 10, 'bold'),
               command = self.destroy, width = 7)\
            .grid(row=21, column=1, padx= 1, pady = 10)

        Button(master = self.axes_tab,
               text = 'Apply',
               font=('Arial', 10, 'bold'),
               command = self.apply_axes,
               width = 7)\
            .grid(row=21, column=2, padx= 1, pady = 10)

        self.tabs.add(self.axes_tab, text='Axes')

        ############
        # Data TAB #
        ############

        # Global frame
        self.data_tab = Frame(self.tabs)
        self.tabs.add(self.data_tab, text='Data')

        # All the labels
        Label(master = self.data_tab,
              text='Label',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 17)\
            .grid(column=1, row=2, padx= 1, pady = 5)

        Label(master = self.data_tab,
              text='Line',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 17)\
            .grid(column=1, row=3, padx= 1, pady = 5)

        Label(master = self.data_tab,
              text='Line style',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=4, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Draw style',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=5, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Width',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=6, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Color (RBGA)',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=7, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Marker',
              font=('Arial', 10, 'bold'),
              anchor="w",
              width = 17)\
            .grid(column=1, row=8, padx= 1, pady = 5, sticky='NW')

        Label(master = self.data_tab,
              text='Style',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=9, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Size',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=10, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Face color (RGBA)',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=11, padx= 1, pady = 2, sticky='NW')

        Label(master = self.data_tab,
              text='Edge color (RBGA)',
              font=('Arial', 10),
              anchor="w",
              width = 17)\
            .grid(column=1, row=12, padx= 1, pady = 2, sticky='NW')

        # Combobox to select the plot to modify
        self.orbit_COMBOBOX = Combobox(self.data_tab, width=13)
        self.orbit_COMBOBOX .bind("<<ComboboxSelected>>", lambda _ : self.update_data_params())
        self.orbit_COMBOBOX.grid(row=1, column=2, pady = 10, sticky='E')
        self.orbit_COMBOBOX['values'] = [plot.get_label() for plot in self.ax.get_lines()] + \
                                        [plot.get_label() for plot in self.ax.patches]
        self.orbit_COMBOBOX.current(0)
        self.plots = [plot for plot in self.ax.get_lines()] + [plot for plot in self.ax.patches]

        # Line style combobox
        self.linestyles =  {'-' : 'solid', ':' : 'dotted', '--' : 'dashed',
                            '-.' : 'dashdot', 'None' : 'None'}
        self.linestyle_COMBOBOX = Combobox(self.data_tab, width= 10)
        self.linestyle_COMBOBOX.grid(row=4, column=2, sticky='E')
        self.linestyle_COMBOBOX['values'] = [label for _,label in self.linestyles.items()]

        # Draw style combobox
        self.drawstyle_COMBOBOX = Combobox(self.data_tab, width= 10)
        self.drawstyle_COMBOBOX.grid(row=5, column=2,sticky='E')
        self.drawstyle_COMBOBOX['values'] = ['default', 'steps', 'steps-pre',
                                             'steps-mid', 'steps-post']

        # Marker style combobox
        self.markers = {' ': 'nothing', '': 'nothing', '*': 'star',
                        '+': 'plus', ',': 'pixel', '.': 'point',
                        '1': 'tri_down', '2': 'tri_up', '3': 'tri_left',
                        '4': 'tri_right', '8': 'octagon', '<': 'triangle_left',
                        '>': 'triangle_right', 'D': 'diamond', 'H': 'hexagon2',
                        'None': 'nothing', 'P': 'plus_filled', 'X': 'x_filled',
                        '^': 'triangle_up', '_': 'hline', 'd': 'thin_diamond',
                        'h': 'hexagon1', 'none': 'nothing', 'o': 'circle',
                        'p': 'pentagon', 's': 'square', 'v': 'triangle_down',
                        'x': 'x', '|': 'vline', 0: 'tickleft',
                        1: 'tickright', 10: 'caretupbase', 11: 'caretdownbase',
                        2: 'tickup', 3: 'tickdown', 4: 'caretleft',
                        5: 'caretright', 6: 'caretup', 7: 'caretdown',
                        8: 'caretleftbase', 9: 'caretrightbase'}

        self.markerstyle_COMBOBOX = Combobox(self.data_tab, width= 13, justify = LEFT)
        self.markerstyle_COMBOBOX.grid(row=9, column=2, sticky='E')
        self.markerstyle_COMBOBOX['values'] = [label for _,label in self.markers.items()]

        # Buttons and frames to chose the colors

        self.color_sel_FRAME = Frame(self.data_tab)
        self.color_sel_FRAME.grid(row = 7, column = 2, sticky='E')

        self.color_BUTTON = Button(self.color_sel_FRAME,
                                   width = 1,
                                   height= 1,
                                   command = lambda : self.chose_color(0))
        self.color_BUTTON.pack(side = RIGHT)

        self.Fcolor_sel_FRAME = Frame(self.data_tab)
        self.Fcolor_sel_FRAME.grid(row = 11, column = 2, sticky='E')

        self.Fcolor_BUTTON = Button(self.Fcolor_sel_FRAME,
                                    width = 1,
                                    height= 1,
                                    command = lambda : self.chose_color(1))
        self.Fcolor_BUTTON.pack(side = RIGHT)

        self.Ecolor_sel_FRAME = Frame(self.data_tab)
        self.Ecolor_sel_FRAME.grid(row = 12, column = 2, sticky='E')

        self.Ecolor_BUTTON = Button(self.Ecolor_sel_FRAME,
                                    width = 1,
                                    height= 1,
                                    command = lambda : self.chose_color(2))
        self.Ecolor_BUTTON.pack(side = RIGHT)

        # All the entries
        self.label_ENTRY = Entry(self.data_tab, width= 10,)
        self.label_ENTRY.grid(row=2, column=2, sticky='E')

        self.width_ENTRY = Entry(self.data_tab, width= 10)
        self.width_ENTRY.grid(row=6, column=2, sticky='E')

        self.color_ENTRY = Entry(self.color_sel_FRAME, width= 10)
        self.color_ENTRY.pack(side = RIGHT)

        self.size_ENTRY = Entry(self.data_tab, width= 10)
        self.size_ENTRY.grid(row=10, column=2, sticky='E')

        self.Fcolor_ENTRY = Entry(self.Fcolor_sel_FRAME, width= 10)
        self.Fcolor_ENTRY.pack(side = RIGHT)

        self.Ecolor_ENTRY = Entry(self.Ecolor_sel_FRAME, width= 10)
        self.Ecolor_ENTRY.pack(side = RIGHT)

        # Action Buttons
        Button(self.data_tab,
                text='Apply',
                font=('Arial', 10, 'bold'),
                width = 7,
                command=self.apply_params)\
                .grid(row = 13, column = 2, padx = 1, pady = 10, sticky=W)

        Button(self.data_tab,
               text='Close',
               font=('Arial', 10, 'bold'),
               width = 7,
               command=self.destroy)\
               .grid(row = 13, column=1, padx = 1, pady = 10)

        self.update_data_params()

    def apply_axes(self):

        """
        Apply the parameters to the axes
        Parameters
        ----------
        Returns
        -------

        """
        # Set the axes parameters
        self.ax.set_title(self.e_title.get(), fontsize = float(self.e_titlesize.get()))
        self.ax.set_xlabel(self.e_xlabel.get(), fontsize = float(self.e_xlabelsize.get()))
        self.ax.set_ylabel(self.e_ylabel.get(), fontsize = float(self.e_ylabelsize.get()))
        self.ax.set_xlim((float(self.e_xmax.get()), float(self.e_xmin.get())))
        self.ax.set_ylim((float(self.e_ymax.get()), float(self.e_ymin.get())))

        # Check if the locators are used and their values validity
        if self.e_major_loc.get() != '' and float(self.e_major_loc.get()) > 0:
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(float(self.e_major_loc.get())))
        if self.e_minor_loc.get() != '' and float(self.e_minor_loc.get()) > 0:
            self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(float(self.e_minor_loc.get())))
        else:
            self.ax.minorticks_off()

        # Set the tick parameters
        self.ax.tick_params(axis = 'x', labelrotation = float(self.e_xtick_rotation.get()))
        self.ax.tick_params(axis = 'y', labelsize = self.e_ytick_size.get())
        self.ax.tick_params(axis = 'x', labelsize = self.e_xtick_size.get())

        # If the x tick modifier label is enable compute the modification
        if self.e_modifier.get() != '':

            # Load the instructions
            mod = self.e_modifier.get()

            # Check if the modifier is a list of tick
            if mod[0] == '[' and mod[-1] == ']' and len(mod[1:len(mod)-1].split(',')) == len(self.ax.get_xticklabels()):
                self.ax.set_xticklabels(mod[1:len(mod)-1].split(','))

            # Else treate the modification
            else:
                # Get the previous labels
                previous_labels = [t.get_text()
                                    .replace('_',' ')
                                    .replace('-', ' ')
                                    .split()
                                    for t in self.ax.get_xticklabels()]

                try:
                    # Replace the bracket expressions by their values
                    expressions = [re.sub(r'\[(\d+)\]',
                                          lambda match:
                                                        refs[int(match.group(1))], mod.replace('exp','np.exp')
                                                                                      .replace('log','np.log')
                                         )
                                    for refs in previous_labels]

                    # Compute the expression within {}
                    res = [re.sub(r'\{([^{}]*)\}',
                                  lambda match:
                                                str(eval(match.group(1))), expr
                                    )
                            for expr in expressions]

                    # Set the ticks
                    self.ax.set_xticklabels(res)
                except IndexError:
                    showerror('Syntax error', "Please enter a valid formula for x axis")

        # Update the canvas
        self.canvas.draw()

    def update_data_params(self):

        """
        Get the parameters from the plots
        Parameters
        ----------
        Returns
        -------

        """

        if isinstance(self.plots[self.orbit_COMBOBOX.current()], Rectangle):
            # Select the good values in the combobox
            self.linestyle_COMBOBOX.current(self.linestyle_COMBOBOX['values']
                                            .index(self.plots[self.orbit_COMBOBOX.current()].get_linestyle()))
            self.drawstyle_COMBOBOX.config(state= DISABLED)
            self.markerstyle_COMBOBOX.config(state= DISABLED)

            # Delete all the previous entries
            self.label_ENTRY.delete(0, 'end')
            self.width_ENTRY.delete(0, 'end')
            self.color_ENTRY.delete(0, 'end')
            self.size_ENTRY.delete(0, 'end')
            self.Fcolor_ENTRY.delete(0, 'end')
            self.Ecolor_ENTRY.delete(0, 'end')

            # Place the good parameters in the entries
            self.label_ENTRY.insert(0,self.plots[self.orbit_COMBOBOX.current()].get_label())
            self.width_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_width()))
            self.color_ENTRY.insert(0,str(mcolors.to_hex(self.plots[self.orbit_COMBOBOX.current()].get_facecolor())))
            self.size_ENTRY.config(state= DISABLED)
            self.Fcolor_ENTRY.config(state= DISABLED)
            self.Ecolor_ENTRY.config(state= DISABLED)

            # Ajust the state and the colors of the buttons
            self.color_BUTTON.config(bg = mcolors.to_hex(self.plots[self.orbit_COMBOBOX.current()].get_facecolor()))
            self.Fcolor_BUTTON.config(state=DISABLED)
            self.Ecolor_BUTTON.config(state=DISABLED)

        else :

            # Select the good values in the combobox according to the plot's parameters
            self.drawstyle_COMBOBOX.config(state= NORMAL)
            self.markerstyle_COMBOBOX.config(state= NORMAL)
            self.linestyle_COMBOBOX.current(self.linestyle_COMBOBOX['values'].index(
                                            self.linestyles[self.plots[self.orbit_COMBOBOX.current()].get_linestyle()]))
            self.drawstyle_COMBOBOX.current(self.drawstyle_COMBOBOX['values'].index(
                                            self.plots[self.orbit_COMBOBOX.current()].get_drawstyle()))
            self.markerstyle_COMBOBOX.current(self.markerstyle_COMBOBOX['values'].index(
                                            self.markers[self.plots[self.orbit_COMBOBOX.current()].get_marker()]))

            # Delete all the previous entries
            self.label_ENTRY.delete(0, 'end')
            self.width_ENTRY.delete(0, 'end')
            self.color_ENTRY.delete(0, 'end')
            self.size_ENTRY.delete(0, 'end')
            self.Fcolor_ENTRY.delete(0, 'end')
            self.Ecolor_ENTRY.delete(0, 'end')

            # Place the good parameters in the entries
            self.size_ENTRY.config(state= NORMAL)
            self.Fcolor_ENTRY.config(state= NORMAL)
            self.Ecolor_ENTRY.config(state= NORMAL)
            self.label_ENTRY.insert(0,self.plots[self.orbit_COMBOBOX.current()].get_label())
            self.width_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_lw()))
            self.color_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_color()))
            self.size_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_ms()))
            self.Fcolor_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_mfc()))
            self.Ecolor_ENTRY.insert(0,str(self.plots[self.orbit_COMBOBOX.current()].get_mec()))

            # Ajust the colors of the buttons
            self.Fcolor_BUTTON.config(state= NORMAL)
            self.Ecolor_BUTTON.config(state= NORMAL)
            self.color_BUTTON.config(bg = mcolors.to_hex(self.plots[self.orbit_COMBOBOX.current()].get_color()))
            self.Fcolor_BUTTON.config(bg = mcolors.to_hex(self.plots[self.orbit_COMBOBOX.current()].get_mfc()))
            self.Ecolor_BUTTON.config(bg = mcolors.to_hex(self.plots[self.orbit_COMBOBOX.current()].get_mec()))

    def chose_color(self,index):

        """
        Enable the choice of the colors for the different elements
        Parameters
        ----------
        index: int
        0 : global color / 1 : Front color / 2 : Edge color
        Returns
        -------

        """
        # Create the window to chose the color
        color_code = askcolor(title="Choose a color")

        # Ajuste the color according to the user's choice
        if index == 0:
            self.color_ENTRY.delete(0, 'end')
            self.color_ENTRY.insert(0,str(color_code[1]))
            self.color_BUTTON.config(bg = color_code[1])
        elif index == 1:
            self.Fcolor_ENTRY.delete(0, 'end')
            self.Fcolor_ENTRY.insert(0,str(color_code[1]))
            self.Fcolor_BUTTON.config(bg = color_code[1])
        else :
            self.Ecolor_ENTRY.delete(0, 'end')
            self.Ecolor_ENTRY.insert(0,str(color_code[1]))
            self.Ecolor_BUTTON.config(bg = color_code[1])

    def apply_params(self):

        """
        Apply the parameters to the datas
        Parameters
        ----------
        Returns
        -------

        """

        # Split the case of the bar plot which owns less parameters
        orb = self.orbit_COMBOBOX.current()
        if isinstance(self.plots[self.orbit_COMBOBOX.current()], Rectangle):
            self.plots[orb].set_label(self.label_ENTRY.get())
            self.plots[orb].set_width(float(self.width_ENTRY.get()))
            self.plots[orb].set_facecolor(self.color_ENTRY.get())
            self.plots[orb].set_linestyle(self.linestyle_COMBOBOX.get())
        else:
            self.plots[orb].set_label(self.label_ENTRY.get())
            self.plots[orb].set_lw(self.width_ENTRY.get())
            self.plots[orb].set_color(self.color_ENTRY.get())
            self.plots[orb].set_ms(self.size_ENTRY.get())
            self.plots[orb].set_mfc(self.Fcolor_ENTRY.get())
            self.plots[orb].set_mec(self.Ecolor_ENTRY.get())
            self.plots[orb].set_linestyle({v: k for k, v in self.linestyles.items()}[self.linestyle_COMBOBOX.get()])
            self.plots[orb].set_drawstyle(self.drawstyle_COMBOBOX.get())
            self.plots[orb].set_marker({v: k for k, v in self.markers.items()}[self.markerstyle_COMBOBOX.get()])

        # Update the label value of the plot in the combobox
        self.orbit_COMBOBOX['values'] = [plot.get_label() for plot in self.ax.get_lines()] +\
                                        [plot.get_label() for plot in self.ax.patches]
        self.orbit_COMBOBOX.current(orb)

        # Update the canvas
        self.canvas.draw()
